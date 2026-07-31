import PySide6.QtCore as Qt
import PySide6.QtWidgets as qt

import load_data
import save_data
import utilities
from assignment import Assignment, NewAssignment
from class_list import ClassList
from classes import Class, NewClass


class AssignmentsTab(qt.QWidget):
    classAddedAssignments = Qt.Signal(str)

    def __init__(self):
        super().__init__()
        self.user = load_data.get_json("user.json")
        self.classes = self.user["classes_order_assignments"]

        self.NewAssignmentButton = qt.QPushButton("+ Assignment")
        self.NewClassButton = qt.QPushButton("+ Class")
        self.AssignmentsList = ClassList()

        layout = qt.QVBoxLayout()
        buttons = qt.QHBoxLayout()
        buttons.addWidget(self.NewAssignmentButton)
        buttons.addWidget(self.NewClassButton)
        layout.addLayout(buttons)
        layout.addWidget(self.AssignmentsList)
        self.setLayout(layout)

        self.assignments = {}
        for class_name in self.user["classes_order_assignments"]:
            self.AddClassWidget(class_name)
        self.AddClassWidget("Unordered")
        for assignment in load_data.load_assignments("assignments"):
            self.AddAssignmentWidget(assignment)

        self.AssignmentsList.sort()
        self.NewAssignmentButton.clicked.connect(self.AddAssignment)
        self.NewClassButton.clicked.connect(self.AddClass)


    def AddAssignment(self):
        dialog = NewAssignment(None, self.classes)
        if dialog.exec() == qt.QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            id = utilities.generate_id("assignments")
            data["id"] = str(id)
            path = f"assignments/{id}.json"
            save_data.save_json(path,data)
            self.AddAssignmentWidget(data)
            self.AssignmentsList.sort()

    def AddClass(self):
        dialog = NewClass()
        if dialog.exec() == qt.QDialog.DialogCode.Accepted:
            name = dialog.class_name.text().strip()
            if name in self.user["classes_order_assignments"]:
                qt.QMessageBox.warning(self,"Error","That class already exists.")
                return
            self.user["classes_order_assignments"].append(name)
            self.user["classes_order_notes"].append(name)
            save_data.save_json("user.json",self.user)
            self.classes.append(name)
            self.AddClassWidget(name)

    def AddAssignmentWidget(self,data):
        widget = Assignment(data)
        widget.delete_requested.connect(self.RemoveAssignmentWidget)
        widget.edit_requested.connect(self.Edit)
        self.AssignmentsList.addItem(widget)

    def RemoveAssignmentWidget(self,widget):
        name = widget.data["id"]
        self.AssignmentsList.removeItem(widget)
        path = f"assignments/{name}.json"
        save_data.delete_file(path)

    def RemoveClassWidget(self,widget):
        self.user["classes_order_assignments"].remove(widget.class_name)
        self.user["classes_order_notes"].remove(widget.class_name)
        self.AssignmentsList.removeItem(widget)
        save_data.save_json("user.json",self.user)

    def Edit(self, widget):
        self.RemoveAssignmentWidget(widget)
        data = widget.dialog.get_data()
        data["id"] = widget.data["id"]
        path = f"assignments/{data["id"]}.json"
        save_data.save_json(path,data)
        self.AddAssignmentWidget(data)
        self.AssignmentsList.sort()

    def AddClassWidget(self,name):
        widget = Class(name)
        widget.delete_requested.connect(self.RemoveClassWidget)
        self.AssignmentsList.addItem(widget)
