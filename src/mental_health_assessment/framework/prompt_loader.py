from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def load(path):
    return (BASE_DIR / path).read_text(encoding="utf-8")