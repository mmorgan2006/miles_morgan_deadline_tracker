import PySide6.QtWidgets as qt

import load_data
import save_data
from assignment import Assignment, NewAssignment
from classes import Class, NewClass
from due_date_sort import sort


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
            self.AddClassWidget(class_name)
            for assignment in load_data.load_assignments(f"assignments/classes/{class_name}"):
                self.AddAssignmentWidget(assignment)
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
            if data["class"] == "None":
                path = f"assignments/{data["name"]}.json"
            else:
                path = f"assignments/classes/{data["class"]}/{data["name"]}.json"
            save_data.save_json(path,data)
            self.AddAssignmentWidget(data)
            self.AssignmentsList.sort()

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
            if widget.name.text() in self.classes:
                return
            self.classes[widget.name.text()] = {"widget": widget,"assignments": []}
            self.content_layout.insertWidget(self.content_layout.count() - 1, widget)
        elif isinstance(widget,Assignment):
            class_name = widget.data["class"]
            if widget.data["class"] == "None":
                class_name = "Unordered"
            self.classes[class_name]["widget"].addAssignment(widget)
            self.classes[class_name]["assignments"].append(widget)
    def removeItem(self, widget):
        self.content_layout.removeWidget(widget)
        if widget.data["class"] == "None":
            self.classes["Unordered"]["assignments"].remove(widget)
        else:
            self.classes[widget.data["class"]]["assignments"].remove(widget)
        widget.deleteLater()
    def sort(self):
        for class_name in self.classes:
            arr = self.classes[class_name]["assignments"]
            if len(arr) > 1:
                class_widget = self.classes[class_name]["widget"]
                self.classes[class_name]["assignments"] = sort(arr,0,len(arr)-1)
                for i in range(len(arr)):
                    class_widget.content_layout.insertWidget(i, self.classes[class_name]["assignments"][i])
