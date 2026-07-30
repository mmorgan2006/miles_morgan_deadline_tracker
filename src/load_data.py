import json
import os
from pathlib import Path


def get_data_dir():
    if os.name == "nt":  # Windows
        base = Path(os.environ["APPDATA"])
    else:  # macOS/Linux
        base = Path.home() / ".local" / "share"
    data_dir = base / "deadline-tracker"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir

def load_classes():
    dir = get_data_dir() / "assignments/classes"
    if not dir.exists():
        dir.mkdir(parents=True,exist_ok=True)
        return []
    return [f.name for f in dir.iterdir() if f.is_dir()]
def get_json(path):
    dir = get_data_dir() / path
    with open(dir,"r") as file:
        return json.load(file)
