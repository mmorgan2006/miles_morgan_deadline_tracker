import json
import os
from pathlib import Path

import save_data


def get_data_dir():
    if os.name == "nt":  # Windows
        base = Path(os.environ["APPDATA"])
    else:  # macOS/Linux
        base = Path.home() / ".local" / "share"

    data_dir = base / "mmorgan-deadline-tracker"
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
def load_assignments(path):
    dir = get_data_dir() / f"{path}"
    assignments = []
    for f in dir.iterdir():
        if f.is_file():
            with open(f,"r") as file:
                assignments.append(json.load(file))
    return assignments

def initialize():
    dir = get_data_dir()
    path = dir / "user.json"
    if not path.exists():
        user = {"classes_order_assignments": [],"classes_order_notes":[],"notebooks": []}
        save_data.save_json(path,user)
    path = dir / "assignments.json"
    if not path.exists():
        data = {}
        save_data.save_json(path, data)
    path = dir / "notes.json"
    if not path.exists():
        data = {}
        save_data.save_json(path, data)
