import json

import PySide6.QtCore as Qt

import load_data


def convert_date(date):
    if isinstance(date, str):
        date = Qt.QDate.fromString(date,"MM-dd-yyyy")
    date = date.dayOfWeek()
    match date:
        case 1: return "Monday"
        case 2: return "Tuesday"
        case 3: return "Wednesday"
        case 4: return "Thursday"
        case 5: return "Friday"
        case 6: return "Saturday"
        case 7: return "Sunday"
def generate_id(path):
    path = load_data.get_data_dir() / path
    with open(path, "r") as file:
        data = json.load(file)
    ids = {int(id) for id in data}
    if len(ids) > 0:
        return max(ids)+1
    else:
        return 0
