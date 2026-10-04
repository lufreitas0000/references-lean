#!/usr/bin/env python3
import sys, os, subprocess, json, hashlib

DOCS_DIR = "docs"
LOCK_FILE = os.path.join(DOCS_DIR, "statement_lock.json")

def get_locks(prefix):
    with open("TempLockDump.lean", "w", encoding="utf-8") as f:
        f.write(f"import Bosonize\nimport Bosonize.Stubs.Lattice\nimport Bosonize.Stubs.Umbral\nimport Bosonize.Stubs.Fourier\nimport Bosonize.Stubs.CAR\nimport Bosonize.Stubs.Net\nimport Bosonize.Stubs.LatticeFermion\nimport Bosonize.Stubs.Vacuum\nimport Bosonize.Stubs.Budget\nimport Bosonize.Stubs.BosonFock\nimport Bosonize.Stubs.Params\nimport Bosonize.Audit.LockDump\n\n#dump_locks {prefix}\n")
    
    subprocess.run(["/home/lucas/.elan/bin/lake", "build"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    res = subprocess.run(["/home/lucas/.elan/bin/lake", "env", "lean", "TempLockDump.lean"], capture_output=True, text=True)
    if os.path.exists("TempLockDump.lean"): os.remove("TempLockDump.lean")
    
    out = res.stdout
    locks = {}
    lines = out.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("LOCK: "):
            name = line[len("LOCK: "):].strip()
            type_lines = []
            i += 1
            while i < len(lines) and not lines[i].startswith("---END_LOCK---"):
                type_lines.append(lines[i])
                i += 1
            type_str = "\n".join(type_lines).strip()
            if name.startswith("Bosonize.Stubs."):
                name = "Bosonize.Core." + name[len("Bosonize.Stubs."):]
            h = hashlib.sha256(type_str.encode('utf-8')).hexdigest()
            locks[name] = h
        i += 1
    return locks

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: lock_statements.py --write | --check | --selftest")
        sys.exit(1)
        
    cmd = sys.argv[1]
    os.makedirs(DOCS_DIR, exist_ok=True)
    
    if cmd == "--write":
        locks = get_locks("Bosonize.Stubs")
        with open(LOCK_FILE, "w", encoding="utf-8") as f:
            json.dump(locks, f, indent=2, sort_keys=True)
        print("Wrote locks.")
        
    elif cmd == "--check":
        if not os.path.exists(LOCK_FILE):
            print("No lock file, nothing to check.")
            sys.exit(0)
        with open(LOCK_FILE, "r", encoding="utf-8") as f:
            expected = json.load(f)
        if not expected:
            print("Empty lock file, OK.")
            sys.exit(0)
            
        actual = get_locks("Bosonize.Core")
        failed = False
        for name, expected_hash in expected.items():
            if name not in actual:
                print(f"MISSING in Core: {name}")
                failed = True
            elif actual[name] != expected_hash:
                print(f"MISMATCH in Core: {name}")
                failed = True
        if failed:
            sys.exit(1)
        print("Check OK.")
        
    elif cmd == "--selftest":
        def run_custom(stub_code, core_code):
            with open("TempLockDumpStubs.lean", "w") as f:
                f.write(f"import Bosonize.Audit.LockDump\n{stub_code}\n#dump_locks Bosonize.Stubs\n")
            with open("TempLockDumpCore.lean", "w") as f:
                f.write(f"import Bosonize.Audit.LockDump\n{core_code}\n#dump_locks Bosonize.Core\n")
            
            subprocess.run(["/home/lucas/.elan/bin/lake", "build", "Bosonize.Audit.LockDump"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            out_stub = subprocess.run(["/home/lucas/.elan/bin/lake", "env", "lean", "TempLockDumpStubs.lean"], capture_output=True, text=True).stdout
            out_core = subprocess.run(["/home/lucas/.elan/bin/lake", "env", "lean", "TempLockDumpCore.lean"], capture_output=True, text=True).stdout
            
            locks_expected = {}
            lines = out_stub.split("\n")
            i = 0
            while i < len(lines):
                if lines[i].startswith("LOCK: "):
                    name = lines[i][len("LOCK: "):].strip()
                    name = "Bosonize.Core." + name[len("Bosonize.Stubs."):]
                    i += 1
                    t = []
                    while i < len(lines) and not lines[i].startswith("---END_LOCK---"):
                        t.append(lines[i]); i += 1
                    locks_expected[name] = hashlib.sha256(("\n".join(t).strip()).encode('utf-8')).hexdigest()
                i += 1
                
            locks_actual = {}
            lines = out_core.split("\n")
            i = 0
            while i < len(lines):
                if lines[i].startswith("LOCK: "):
                    name = lines[i][len("LOCK: "):].strip()
                    i += 1
                    t = []
                    while i < len(lines) and not lines[i].startswith("---END_LOCK---"):
                        t.append(lines[i]); i += 1
                    locks_actual[name] = hashlib.sha256(("\n".join(t).strip()).encode('utf-8')).hexdigest()
                i += 1
                
            return locks_expected, locks_actual
            
        sc = "namespace Bosonize.Stubs\ndef my_thm (x : Nat) : Nat := x\nend Bosonize.Stubs\n"
        cc = "namespace Bosonize.Core\ndef my_thm (x : Nat) (y : Nat) : Nat := x\nend Bosonize.Core\n"
        ex, ac = run_custom(sc, cc)
        
        if ex.get("Bosonize.Core.my_thm") == ac.get("Bosonize.Core.my_thm"):
            print("Selftest failed: mismatch not detected")
            sys.exit(1)
            
        cc2 = "namespace Bosonize.Core\ndef my_thm (x : Nat) : Nat := x\nend Bosonize.Core\n"
        ex, ac = run_custom(sc, cc2)
        if ex.get("Bosonize.Core.my_thm") != ac.get("Bosonize.Core.my_thm"):
            print("Selftest failed: match not detected")
            sys.exit(1)
            
        print("Selftest passed.")
        for f in ["TempLockDumpStubs.lean", "TempLockDumpCore.lean"]:
            if os.path.exists(f): os.remove(f)
        sys.exit(0)
