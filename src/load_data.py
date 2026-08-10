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

def get_json(path) -> dict:
    dir = get_data_dir() / path
    if not dir.exists():
        initialize()
    try:
        with open(dir,"r") as file:
            data = json.load(file)
            return data
    except Exception:  # noqa: BLE001
        if path == "user.json": return {"classes_order_assignments": [], "classes_order_notes": []}
        else: return {}


def initialize():
    dir = get_data_dir()
    path = dir / "user.json"
    if not path.exists():
        user = {"classes_order_assignments": [],"classes_order_notes":[]}
        save_data.save_json(path,user)
    path = dir / "assignments.json"
    if not path.exists():
        data = {}
        save_data.save_json(path, data)
    path = dir / "notes.json"
    if not path.exists():
        data = {}
        save_data.save_json(path, data)
    path = dir / "notebooks.json"
    if not path.exists():
        data = {}
        save_data.save_json(path, data)
