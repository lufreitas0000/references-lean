import sys
import importlib
import os

# Ensure oracle/src is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
# Also add mutants dir so we can import them
sys.path.insert(0, os.path.dirname(__file__))

mutants = [
    "mutant_1",
    "mutant_2",
    "mutant_3",
    "mutant_4",
    "mutant_5"
]

failed = False
for m in mutants:
    mod = importlib.import_module(m)
    res = mod.check()
    print(f"{m}: {'SURVIVED' if res else 'KILLED'}")
    if res:
        failed = True

if failed:
    sys.exit(1)
else:
    sys.exit(0)
