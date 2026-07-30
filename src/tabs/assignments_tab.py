import PySide6.QtWidgets as qt

import load_data
import save_data
from assingment import Assignment, NewAssignment
from classes import Class, NewClass


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
        self.AddClassWidget("Unordered")
        for class_name in self.classes:
            self.AddClassWidget(class_name)
            for assignment in load_data.load_assignments(class_name):
                self.AddAssignmentWidget(assignment)


        self.NewAssignmentButton.clicked.connect(self.AddAssignment)
        self.NewClassButton.clicked.connect(self.AddClass)


    def AddAssignment(self):
        dialog = NewAssignment(None, self.classes)
        if dialog.exec() == qt.QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data["class"] == "None":
                path = f"assignments/{data["name"]}.json"
            else:
                path = f"assignments/classes/{data["class"]}/{data["name"]}.json"
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
            self.AddClassWidget(name)
    def AddAssignmentWidget(self,data):
        widget = Assignment(data)
        widget.delete_requested.connect(self.RemoveAssignmentWidget)
        widget.edit_requested.connect(self.Edit)
        self.AssignmentsList.addItem(widget)
    def RemoveAssignmentWidget(self,widget):
        name,class_name = widget.data["name"],widget.data["class"]
        self.AssignmentsList.removeItem(widget)
        path = f"assignments/classes/{class_name}/{name}.json"
        if class_name == "None":
            path = f"assignments/{name}.json"
        save_data.delete_file(path)
    def Edit(self, widget):
        self.RemoveAssignmentWidget(widget)
        data = widget.dialog.get_data()
        if data["class"] == "None":
            path = f"assignments/{data["name"]}.json"
        else:
            path = f"assignments/classes/{data["class"]}/{data["name"]}.json"
        save_data.save_json(path,data)
        self.AddAssignmentWidget(data)
    def AddClassWidget(self,name):
        widget = Class(name)
        #widget.delete_requested.connect(self.RemoveAssignmentWidget)
        #widget.edit_requested.connect(self.Edit)
        self.AssignmentsList.addItem(widget)
class AssignmentList(qt.QWidget):
    def __init__(self):
        super().__init__()
        self.classes = {}
        scroll = qt.QScrollArea()
        scroll.setWidgetResizable(True)
        content = qt.QWidget()
        self.content_layout = qt.QVBoxLayout(content)
        scroll.setWidget(content)
        layout = qt.QVBoxLayout(self)
        layout.addWidget(scroll)
        self.content_layout.addStretch()
    def addItem(self, widget):
        if isinstance(widget,Class):
            self.classes[widget.name.text()] = widget
            self.content_layout.insertWidget(self.content_layout.count() - 1, widget)
        elif isinstance(widget,Assignment):
            class_name = widget.data["class"]
            if widget.data["class"] == "None":
                class_name = "Unordered"
            self.classes[class_name].addAssignment(widget)
    def removeItem(self, widget):
        self.content_layout.removeWidget(widget)
        widget.deleteLater()
