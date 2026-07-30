import PySide6.QtWidgets as qt

import load_data
import save_data
from assingment import Assignment, NewAssignment
from classes import NewClass


class AssignmentsTab(qt.QWidget):
    def __init__(self):
        super().__init__()
        self.NewAssignmentButton = qt.QPushButton("+ Assignment")
        self.NewClassButton = qt.QPushButton("+ Class")
        self.AssignmentsList = AssignmentList()

        layout = qt.QVBoxLayout()
        buttons = qt.QHBoxLayout()
        buttons.addWidget(self.NewAssignmentButton)
        buttons.addWidget(self.NewClassButton)
        layout.addLayout(buttons)
        layout.addWidget(self.AssignmentsList)
        self.setLayout(layout)

        self.assignments = {}
        self.classes = load_data.load_classes()
        for class_name in self.classes:
            for assignment in load_data.load_assignments(class_name):
                self.AddAssignmentWidget(assignment)
        self.NewAssignmentButton.clicked.connect(self.AddAssignment)
        self.NewClassButton.clicked.connect(self.AddClass)


    def AddAssignment(self):
        dialog = NewAssignment(self.classes)
        if dialog.exec() == qt.QDialog.DialogCode.Accepted:
            data,class_name = dialog.get_data()
            if class_name == "None":
                path = f"assignments/{data["name"]}.json"
            else:
                path = f"assignments/classes/{class_name}/{data["name"]}.json"
            save_data.save_json(path,data)
            self.AddAssignmentWidget(data)

    def AddClass(self):
        dialog = NewClass()
        if dialog.exec() == qt.QDialog.DialogCode.Accepted:
            name = dialog.class_name.text().strip()
            path = f"assignments/classes/{name}"
            if save_data.create_dir(path):
                qt.QMessageBox.warning(self,"Error","That class already exists.")
                return
            self.classes.append(name)
    def AddAssignmentWidget(self,data):
        widget = Assignment(data)
        widget.delete_requested.connect(self.RemoveAssignmentWidget)
        self.AssignmentsList.addItem(widget)
    def RemoveAssignmentWidget(self,widget):
        name,class_name = widget.data["name"],widget.data["class"]
        reply = qt.QMessageBox.question(
            self,
            "Delete Assignment",
            "Are you sure you want to permanently delete this assignment?",
            qt.QMessageBox.StandardButton.Yes | qt.QMessageBox.StandardButton.No
        )
        if reply == qt.QMessageBox.StandardButton.Yes:
            self.AssignmentsList.removeItem(widget)
            save_data.delete_file(f"assignments/classes/{class_name}/{name}.json")
class AssignmentList(qt.QWidget):
    def __init__(self):
        super().__init__()
        scroll = qt.QScrollArea()
        scroll.setWidgetResizable(True)
        content = qt.QWidget()
        self.content_layout = qt.QVBoxLayout(content)
        scroll.setWidget(content)
        layout = qt.QVBoxLayout(self)
        layout.addWidget(scroll)
    def addItem(self, widget):
        self.content_layout.addWidget(widget)
    def removeItem(self, widget):
        self.content_layout.removeWidget(widget)
        widget.deleteLater()
