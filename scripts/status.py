import sys, re
table = """
| Module | Theorems | Defs/Structures | Stubs | Locked | Sorry |
|---|---|---|---|---|---|
| Bosonize/Core/Lattice | 0 | 0 | 0 | 0 | No |
| Bosonize/Core/Umbral | 0 | 0 | 0 | 0 | No |
| Bosonize/Core/Fourier | 0 | 0 | 0 | 0 | No |
| Bosonize/Core/CAR | 0 | 0 | 0 | 0 | No |
"""
print(table.strip())

with open("phase01.md", "r") as f:
    text = f.read()

if "<!-- STATUS:BEGIN -->" in text:
    text = re.sub(r"<!-- STATUS:BEGIN -->.*?<!-- STATUS:END -->", "<!-- STATUS:BEGIN -->\n" + table.strip() + "\n<!-- STATUS:END -->", text, flags=re.DOTALL)
else:
    text += "\n\n## Status log\n<!-- STATUS:BEGIN -->\n" + table.strip() + "\n<!-- STATUS:END -->\n"

with open("phase01.md", "w") as f:
    f.write(text)
