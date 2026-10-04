#!/usr/bin/env python3
"""gworker.py — autonomous Gemini worker for BOSONIZE-LEAN.

Runs an OpenAI-style tool-calling loop against the local LiteLLM proxy
(http://localhost:4000), i.e. billed to the user's own Gemini API key.

Usage:  scripts/gworker.py tasks/<wave>/<id>.toml [--dry-run]

Task card (TOML):
  id = "A2"
  model = "gemini-3.8-flash"          # starting model
  escalate_model = "gemini-3.1-pro"   # optional
  escalate_after = 12                 # turns without success before escalation
  max_turns = 40
  max_cost_brl = 3.0                  # hard stop (estimated, see scripts/prices.toml)
  write = ["docs/MATHLIB_AUDIT.md", "Bosonize/Audit/MathlibAudit.lean"]   # fnmatch globs
  read = ["phase01.md"]               # files preloaded into the prompt
  accept = "bash scripts/accept/A2.sh"   # must exit 0 for the task to be DONE
  goal = '''...'''

Outputs: logs/tasks/<id>.json (status summary), logs/tasks/<id>.transcript.jsonl,
         rows appended to logs/llm_usage.csv.
"""
from __future__ import annotations

import fnmatch
import json
import os
import subprocess
import sys
import time
import tomllib
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROXY = os.environ.get("LITELLM_URL", "http://localhost:4000/v1/chat/completions")
MAX_TOOL_OUT = 6000
ENV = dict(os.environ)
ENV["PATH"] = f"{Path.home()}/.elan/bin:{Path.home()}/.local/bin:" + ENV.get("PATH", "")

SHELL_PREFIXES = (
    "lake env lean ", "lake build", "uv run ", "python3 scripts/", "bash scripts/",
    "latexmk ", "rg ", "ls ", "cat ", "head ", "wc ", "grep ",
)
SHELL_FORBIDDEN = (";", "&&", "||", "|", ">", "<", "`", "$(", "rm ", "sudo", "git ", "curl", "wget")

SYSTEM = """You are an autonomous worker on BOSONIZE-LEAN: a Lean 4 + Mathlib formalization of 1+1D
bosonization on a lattice-regularized AQFT, using umbral (finite-difference) calculus. No unbounded
operators, no analysis/limits in Bosonize/Core.

Hard rules (violations are detected automatically and the task FAILS):
- Never use sorry, admit, axiom, native_decide, opaque, unsafe, implemented_by, extern,
  set_option maxHeartbeats, Filter.Tendsto, tsum, integrals, deriv, MeasureTheory in Bosonize/Core.
- Never change a statement copied from Bosonize/Stubs (statements are hash-locked).
- Never invent Mathlib names: confirm with grep_mathlib or by compiling a `#check`.
- You may only write the files allowed by the task. Keep files complete (write_file overwrites).
- Lean toolchain is pinned (Lean 4.35, recent Mathlib). Mathlib paths: Mathlib/Algebra/Polynomial/*,
  Mathlib/Algebra/MvPolynomial/*, etc. (not Mathlib/Data/Polynomial).
- Work in small steps: write, lean_check, fix. When the acceptance criterion should pass, call
  finish(summary). finish runs the acceptance command; if it fails you get the output and continue.
- Be economical: tool outputs are truncated; avoid dumping huge files.
"""

TOOLS = [
    {"type": "function", "function": {"name": "read_file", "description": "Read a repo file (optionally a line range).",
        "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "start": {"type": "integer"}, "end": {"type": "integer"}}, "required": ["path"]}}},
    {"type": "function", "function": {"name": "write_file", "description": "Create/overwrite an allowed file with full content.",
        "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}}},
    {"type": "function", "function": {"name": "lean_check", "description": "Compile one Lean file with `lake env lean`; returns errors/warnings (or OK).",
        "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}},
    {"type": "function", "function": {"name": "grep_mathlib", "description": "ripgrep a regex over the pinned Mathlib sources; returns file:line:text (max 40 hits).",
        "parameters": {"type": "object", "properties": {"pattern": {"type": "string"}, "path_glob": {"type": "string", "description": "optional sub-path, e.g. Mathlib/Algebra/Polynomial"}}, "required": ["pattern"]}}},
    {"type": "function", "function": {"name": "shell", "description": "Run a whitelisted command (lake env lean, lake build, uv run, python3 scripts/, bash scripts/, latexmk, rg, ls, cat, head, wc, grep). No pipes/redirection.",
        "parameters": {"type": "object", "properties": {"cmd": {"type": "string"}, "cwd": {"type": "string", "description": "repo-relative dir"}}, "required": ["cmd"]}}},
    {"type": "function", "function": {"name": "finish", "description": "Claim the task is done. Runs the acceptance command.",
        "parameters": {"type": "object", "properties": {"summary": {"type": "string"}}, "required": ["summary"]}}},
]


def trunc(s: str, n: int = MAX_TOOL_OUT) -> str:
    return s if len(s) <= n else s[: n // 2] + f"\n...[truncated {len(s) - n} chars]...\n" + s[-n // 2:]


def run(cmd: str, cwd: Path = ROOT, timeout: int = 1200) -> tuple[int, str]:
    try:
        p = subprocess.run(cmd, shell=True, cwd=cwd, env=ENV, capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout + p.stderr)
    except subprocess.TimeoutExpired:
        return 124, f"TIMEOUT after {timeout}s"


def load_prices() -> dict:
    f = ROOT / "scripts" / "prices.toml"
    return tomllib.loads(f.read_text()) if f.exists() else {}


class Worker:
    def __init__(self, card_path: Path):
        self.card = tomllib.loads(card_path.read_text())
        self.id = self.card["id"]
        self.model = self.card.get("model", "gemini-3.8-flash")
        self.prices = load_prices()
        self.cost_brl = 0.0
        self.tokens_in = self.tokens_out = 0
        self.turn = 0
        self.failed_finishes = 0
        self.escalated = False
        self.logdir = ROOT / "logs" / "tasks"
        self.logdir.mkdir(parents=True, exist_ok=True)
        self.transcript = (self.logdir / f"{self.id}.transcript.jsonl").open("a")

    # ---------------- tools ----------------
    def _safe(self, rel: str) -> Path:
        p = (ROOT / rel).resolve()
        if ROOT not in p.parents and p != ROOT:
            raise ValueError("path outside repository")
        return p

    def t_read_file(self, path, start=None, end=None):
        lines = self._safe(path).read_text().splitlines()
        s = (start or 1) - 1
        e = end or len(lines)
        return trunc("\n".join(f"{i + 1}: {l}" for i, l in enumerate(lines[s:e], start=s)), 12000)

    def t_write_file(self, path, content):
        rel = str(self._safe(path).relative_to(ROOT))
        if not any(fnmatch.fnmatch(rel, g) for g in self.card.get("write", [])):
            return f"DENIED: {rel} is not in the allowed write list {self.card.get('write')}"
        p = ROOT / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
        return f"wrote {rel} ({len(content)} chars)"

    def t_lean_check(self, path):
        rel = str(self._safe(path).relative_to(ROOT))
        code, out = run(f"lake env lean {rel}", timeout=900)
        return "OK (no errors)" + (f"\n{trunc(out)}" if out.strip() else "") if code == 0 else trunc(out)

    def t_grep_mathlib(self, pattern, path_glob=None):
        base = ROOT / ".lake/packages/mathlib" / (path_glob or "Mathlib")
        try:
            p = subprocess.run(["rg", "-n", "--max-count", "5", "-e", pattern, str(base)], capture_output=True, text=True, timeout=120)
            out = p.stdout.replace(str(ROOT / ".lake/packages/mathlib") + "/", "")
        except FileNotFoundError:
            p = subprocess.run(["grep", "-rnE", pattern, str(base)], capture_output=True, text=True, timeout=120)
            out = p.stdout.replace(str(ROOT / ".lake/packages/mathlib") + "/", "")
        lines = out.splitlines()
        return "\n".join(lines[:40]) + (f"\n... {len(lines) - 40} more" if len(lines) > 40 else "") or "no matches"

    def t_shell(self, cmd, cwd=None):
        c = cmd.strip()
        if not c.startswith(SHELL_PREFIXES) or any(f in c for f in SHELL_FORBIDDEN):
            return f"DENIED: command not whitelisted: {c!r}"
        code, out = run(c, cwd=self._safe(cwd) if cwd else ROOT)
        return f"exit={code}\n{trunc(out)}"

    def t_finish(self, summary):
        cmd = self.card["accept"]
        code, out = run(f"flock /tmp/bosonize-lake.lock {cmd}", timeout=2400)
        if code == 0:
            self.done_summary = summary
            return "ACCEPTED"
        self.failed_finishes += 1
        return f"ACCEPTANCE FAILED (exit {code}). Fix and call finish again.\n{trunc(out)}"

    # ---------------- llm ----------------
    def call(self, messages):
        body = json.dumps({"model": self.model, "messages": messages, "tools": TOOLS, "tool_choice": "auto"}).encode()
        headers = {"Content-Type": "application/json"}
        if os.environ.get("LITELLM_MASTER_KEY"):
            headers["Authorization"] = f"Bearer {os.environ['LITELLM_MASTER_KEY']}"
        for attempt in range(5):
            try:
                req = urllib.request.Request(PROXY, data=body, headers=headers)
                with urllib.request.urlopen(req, timeout=900) as r:
                    res = json.loads(r.read())
                break
            except urllib.error.HTTPError as e:
                err = e.read().decode()[:500]
                if e.code in (429, 500, 502, 503, 504) and attempt < 4:
                    time.sleep(15 * (attempt + 1))
                    continue
                raise RuntimeError(f"HTTP {e.code}: {err}")
            except (urllib.error.URLError, TimeoutError) as e:
                if attempt < 4:
                    time.sleep(15 * (attempt + 1))
                    continue
                raise
        u = res.get("usage", {}) or {}
        ti, to = u.get("prompt_tokens", 0), u.get("completion_tokens", 0)
        self.tokens_in += ti
        self.tokens_out += to
        pr = self.prices.get(self.model, {})
        fx = self.prices.get("fx", {}).get("brl_per_usd", 5.5)
        cost = (ti * pr.get("usd_in_per_m", 2.0) + to * pr.get("usd_out_per_m", 12.0)) / 1e6 * fx
        self.cost_brl += cost
        with (ROOT / "logs" / "llm_usage.csv").open("a") as f:
            f.write(f"{datetime.now(timezone.utc).isoformat()},{self.id},{self.model},{ti},{to},{cost:.4f}\n")
        return res["choices"][0]["message"]

    # ---------------- loop ----------------
    def initial_messages(self):
        ctx = []
        for rel in self.card.get("read", []):
            p = ROOT / rel
            if p.exists():
                ctx.append(f"=== {rel} ===\n{trunc(p.read_text(), 20000)}")
        user = (f"TASK {self.id}\n\nGOAL:\n{self.card['goal']}\n\nALLOWED WRITES: {self.card.get('write')}\n"
                f"ACCEPTANCE COMMAND (run by finish): {self.card['accept']}\n\nCONTEXT FILES:\n" + "\n\n".join(ctx))
        return [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}]

    def log(self, obj):
        self.transcript.write(json.dumps(obj)[:20000] + "\n")
        self.transcript.flush()

    def result(self, status, note=""):
        out = {"id": self.id, "status": status, "model_final": self.model, "escalated": self.escalated,
               "turns": self.turn, "tokens_in": self.tokens_in, "tokens_out": self.tokens_out,
               "est_cost_brl": round(self.cost_brl, 3), "failed_finishes": self.failed_finishes,
               "summary": (getattr(self, "done_summary", "") or note)[:800],
               "finished_at": datetime.now(timezone.utc).isoformat()}
        (self.logdir / f"{self.id}.json").write_text(json.dumps(out, indent=2))
        print(json.dumps(out))
        return 0 if status == "DONE" else 1

    def run(self):
        msgs = self.initial_messages()
        max_turns = self.card.get("max_turns", 40)
        cap = self.card.get("max_cost_brl", 3.0)
        esc_after = self.card.get("escalate_after", 15)
        last_err = ""
        while self.turn < max_turns:
            if self.cost_brl >= cap:
                return self.result("BUDGET", f"cost cap {cap} BRL reached. Last error: {last_err[:300]}")
            if (not self.escalated and self.card.get("escalate_model") and self.turn >= esc_after):
                self.escalated = True
                self.model = self.card["escalate_model"]
                msgs.append({"role": "user", "content": f"[orchestrator] Escalated to {self.model}. Re-assess the approach; previous attempts failed."})
            self.turn += 1
            try:
                m = self.call(msgs)
            except Exception as e:  # noqa: BLE001
                return self.result("ERROR", str(e)[:500])
            msgs.append({k: v for k, v in m.items() if v is not None})
            self.log({"turn": self.turn, "model": self.model, "assistant": m.get("content"), "tool_calls": m.get("tool_calls")})
            calls = m.get("tool_calls") or []
            if not calls:
                msgs.append({"role": "user", "content": "Use the tools to make progress; call finish(summary) when the acceptance criterion passes."})
                continue
            for tc in calls:
                name = tc["function"]["name"]
                try:
                    args = json.loads(tc["function"].get("arguments") or "{}")
                    out = getattr(self, f"t_{name}")(**args)
                except Exception as e:  # noqa: BLE001
                    out = f"TOOL ERROR: {type(e).__name__}: {e}"
                if name in ("lean_check", "finish") and "OK" not in out[:20] and out != "ACCEPTED":
                    last_err = out
                self.log({"turn": self.turn, "tool": name, "result": out[:3000]})
                msgs.append({"role": "tool", "tool_call_id": tc["id"], "content": out})
                if out == "ACCEPTED":
                    return self.result("DONE")
        return self.result("BLOCKED", f"max_turns reached. Last error: {last_err[:400]}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    w = Worker(Path(sys.argv[1]))
    if "--dry-run" in sys.argv:
        print(json.dumps(w.initial_messages()[1]["content"][:2000]))
        sys.exit(0)
    sys.exit(w.run())
