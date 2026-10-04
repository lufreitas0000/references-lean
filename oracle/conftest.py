import sys
from pathlib import Path

oracle_dir = Path(__file__).resolve().parent
src_dir = oracle_dir / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))
if str(oracle_dir) not in sys.path:
    sys.path.insert(0, str(oracle_dir))
