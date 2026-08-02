from math import floor

import PySide6.QtCore as Qt

from assignment import Assignment
from notebook import NoteBook


def sort(list, lowIndex, highIndex):
    if lowIndex >= highIndex:
        try: return [list[lowIndex]]
        except Exception: return list  # noqa: BLE001
    midIndex = floor((highIndex + lowIndex)/2)
    leftHalf = sort(list,lowIndex,midIndex)
    rightHalf = sort(list, midIndex+1,highIndex)
    return merge(leftHalf, rightHalf)

def merge(leftHalf, rightHalf):
    result = []
    left,right = 0,0,
    while left < len(leftHalf) and right < len(rightHalf):
        if compare(leftHalf[left],rightHalf[right]):
            result.append(leftHalf[left])
            left += 1
        else:
            result.append(rightHalf[right])
            right += 1
    while left < len(leftHalf):
        result.append(leftHalf[left])
        left += 1
    while right < len(rightHalf):
        result.append(rightHalf[right])
        right += 1
    return result

def get_days(assignment):
    date = assignment.data["due_date"]
    date = Qt.QDate.fromString(date, "MM-dd-yyyy")
    return Qt.QDate.currentDate().daysTo(date)

def compare(first, second):
    if isinstance(first, Assignment):
        if get_days(first) != get_days(second):
            return get_days(first) < get_days(second)
        if first.data["name"] != second.data["name"]:
            return first.data["name"] < second.data["name"]
        else:
            return False
    if isinstance(first, NoteBook):
        return first.data["index"] < second.data["index"]
