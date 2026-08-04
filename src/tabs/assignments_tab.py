import PySide6.QtCore as Qt
import PySide6.QtWidgets as qt

import load_data
import save_data
import utilities
from assignment import Assignment, NewAssignment
from class_list import ClassList
from classes import Class, NewClass


class AssignmentsTab(qt.QWidget):
    classAdded = Qt.Signal(str)
    classRemoved = Qt.Signal(str)
    classEdit = Qt.Signal(str, str)
    def __init__(self):
        super().__init__()
        self.user = load_data.get_json("user.json")
        self.classes = list(self.user["classes_order_assignments"])
        self.assignments = load_data.get_json("assignments.json")

        self.NewAssignmentButton = qt.QPushButton("+ Assignment")
        self.NewClassButton = qt.QPushButton("+ Class")
        self.AssignmentsList = ClassList()
        self.reminder_label = qt.QLabel()
        self.overdue_label = qt.QLabel("")
        self.overdue_label.setStyleSheet("color: #FF0000;")
        layout = qt.QVBoxLayout()
        buttons = qt.QHBoxLayout()
        buttons.addWidget(self.NewAssignmentButton)
        buttons.addWidget(self.NewClassButton)

        reminders = qt.QHBoxLayout()
        reminders.addWidget(self.reminder_label)
        reminders.addWidget(self.overdue_label)

        layout.addLayout(buttons)
        layout.addLayout(reminders)
        layout.addWidget(self.AssignmentsList)
        self.setLayout(layout)

        self.setUpdatesEnabled(False)
        for class_name in self.classes:
            self.AddClassWidget(class_name)
        self.AddClassWidget("Unordered")
        assignments = self.assignments.copy()
        for id,assignment in assignments.items():
            if assignment["class"] not in self.classes and assignment["class"] != "None":
                del self.assignments[id]
                continue
            self.AddAssignmentWidget(assignment)
        save_data.save_json("assignments.json",self.assignments)
        self.setUpdatesEnabled(True)
        self.AssignmentsList.sortAssignments()
        self.update_reminder()

        self.NewAssignmentButton.clicked.connect(self.AddAssignment)
        self.NewClassButton.clicked.connect(self.AddClass)


    def AddAssignment(self):
        self.classes = load_data.get_json("user.json")["classes_order_assignments"]
        dialog = NewAssignment(None, self.classes)
        if dialog.exec() == qt.QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            id = utilities.generate_id("assignments.json")
            data["id"] = str(id)
            data["status"] = "incomplete"
            self.assignments[str(id)] = data
            save_data.save_json("assignments.json",self.assignments)
            self.AddAssignmentWidget(data)
            self.AssignmentsList.sortAssignments()
            self.update_reminder()
    def AddClass(self):
        dialog = NewClass()
        if dialog.exec() == qt.QDialog.DialogCode.Accepted:
            name = dialog.class_name.text().strip()
            if name in self.user["classes_order_assignments"]:
                qt.QMessageBox.warning(self,"Error","That class already exists.")
                return
            self.classes = load_data.get_json("user.json")["classes_order_assignments"]
            self.user = load_data.get_json("user.json")
            self.user["classes_order_assignments"].append(name)
            self.user["classes_order_notes"].append(name)
            save_data.save_json("user.json",self.user)
            self.AddClassWidget(name)
            self.classAdded.emit(name)
            self.classes.append(name)

    def AddAssignmentWidget(self,data,expanded=False):
        widget = Assignment(data)
        widget.details_button.setChecked(expanded)
        widget.toggle_details()
        widget.delete_requested.connect(self.RemoveAssignmentWidget)
        widget.edit_requested.connect(self.Edit)
        self.AssignmentsList.addItem(widget)

    def RemoveAssignmentWidget(self,widget):
        self.assignments = load_data.get_json("assignments.json")
        name = widget.data["id"]
        self.AssignmentsList.removeItem(widget)
        self.assignments.pop(name)
        save_data.save_json("assignments.json",self.assignments)
        self.update_reminder()
    def RemoveClass(self, name):
        self.classes = load_data.get_json("user.json")["classes_order_assignments"]
        if name in self.classes: self.classes.remove(name)
        if name in self.AssignmentsList.classes:
            widget = self.AssignmentsList.classes[name]["widget"]
            self.RemoveClassWidget(widget)
    def RemoveClassWidget(self,widget):
        self.user = load_data.get_json("user.json")
        if widget.class_name in self.user["classes_order_assignments"]: self.user["classes_order_assignments"].remove(widget.class_name)
        if widget.class_name in self.user["classes_order_notes"]: self.user["classes_order_notes"].remove(widget.class_name)
        self.AssignmentsList.removeItem(widget)
        save_data.save_json("user.json",self.user)
        self.classRemoved.emit(widget.class_name)
        self.update_reminder()
    def Edit(self, widget, expanded):
        self.RemoveAssignmentWidget(widget)
        data = widget.dialog.get_data()
        id = widget.data["id"]
        data["id"] = id
        data["status"] = widget.data["status"]
        self.assignments[str(id)] = data
        save_data.save_json("assignments.json",self.assignments)
        self.AddAssignmentWidget(data,expanded)
        self.AssignmentsList.sortAssignments()
        self.update_reminder()

    def AddClassWidget(self,name):
        widget = Class(name)
        widget.delete_requested.connect(self.RemoveClassWidget)
        widget.edit_requested.connect(self.editClass)
        widget.move_requested.connect(self.move_class)
        self.AssignmentsList.addItem(widget)
    def AcceptClass(self,name):
        self.classes = load_data.get_json("user.json")["classes_order_assignments"]
        self.classes.append(name)
        self.AddClassWidget(name)
    def editClass(self,old_name,new_name):
        contents = self.AssignmentsList.classes[old_name]
        self.AssignmentsList.classes[new_name] = contents
        self.AssignmentsList.classes[new_name]["widget"].class_name = new_name
        self.AssignmentsList.classes[new_name]["widget"].name.setText(new_name)
        self.classEdit.emit(old_name,new_name)

        assignments = load_data.get_json("assignments.json")
        for i in self.AssignmentsList.classes[new_name]["contents"]:
            if isinstance(i,Assignment):
                i.data["class"] = new_name
                assignments[i.data["id"]] = i.data
        save_data.save_json("assignments.json",assignments)


    def AcceptEdit(self,old_name,new_name):
        contents = self.AssignmentsList.classes[old_name]
        self.AssignmentsList.classes[new_name] = contents
        self.AssignmentsList.classes[new_name]["widget"].class_name = new_name
        self.AssignmentsList.classes[new_name]["widget"].name.setText(new_name)

        assignments = load_data.get_json("assignments.json")
        for i in self.AssignmentsList.classes[new_name]["contents"]:
            if isinstance(i,Assignment):
                i.data["class"] = new_name
                assignments[i.data["id"]] = i.data
        save_data.save_json("assignments.json",assignments)
    def update_reminder(self):
        count = 0
        overdue = 0
        current = Qt.QDate.currentDate()
        assignments = self.assignments.copy()
        self.classes = load_data.get_json("user.json")["classes_order_assignments"]
        for id,assignment in assignments.items():
            if assignment["class"] not in self.classes and assignment["class"] != "None":
                del self.assignments[id]
                continue
            date = Qt.QDate.fromString(assignment["due_date"], "MM-dd-yyyy")
            if 7 >= current.daysTo(date) >= 0 and assignment["status"] == "incomplete":
                count += 1
            elif current.daysTo(date) < 0 and assignment["status"] == "incomplete":
                overdue += 1
        save_data.save_json("assignments.json",self.assignments)
        if count <= 0:
            self.reminder_label.setText("No assignments due this week!")
        elif count == 1:
            self.reminder_label.setText("1 assignment due this week.")
        else:
            self.reminder_label.setText(f"{count} assignments due this week.")

        if overdue <= 0:
            self.overdue_label.setText("")
        elif overdue == 1:
            self.overdue_label.setText("1 assignment overdue.")
        else:
            self.overdue_label.setText(f"{count} assignments overdue.")
        self.reminder_label
    def move_class(self,widget,direction):
        self.user = load_data.get_json("user.json")
        self.classes = self.user["classes_order_assignments"]
        index = self.classes.index(widget.class_name)
        if index - direction < 0 or index - direction >= len(self.classes):
            return
        replaced = self.classes[index-direction]
        self.classes[index-direction] = widget.class_name
        self.classes[index] = replaced
        self.user["classes_order_assignments"] = self.classes
        save_data.save_json("user.json",self.user)
        self.AssignmentsList.content_layout.insertWidget(index-direction,widget)
