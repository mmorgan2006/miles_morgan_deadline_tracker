import json
import os
from pathlib import Path


def get_data_dir():
    if os.name == "nt":  # Windows
        base = Path(os.environ["APPDATA"])
    else:  # macOS/Linux
        base = Path.home() / ".local" / "share"
    data_dir = base / "mmorgan-deadline-tracker"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir
def save_json(path,data):
    dir = get_data_dir()
    with open(dir / path, "w") as file:
        json.dump(data, file, indent=4)

def create_dir(path):
    dir = get_data_dir()
    folder = dir / path
    if folder.exists():
        return True #already exists = true
    folder.mkdir(parents=True, exist_ok=True)
    return False

def delete_file(path):
    dir = get_data_dir() / path
    if dir.is_file():
        os.remove(dir)
    elif dir.is_dir():
        os.rmdir(dir)
