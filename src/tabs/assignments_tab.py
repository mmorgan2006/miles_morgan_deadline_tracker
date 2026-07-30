import PySide6.QtWidgets as qt

import load_data
import save_data
from assingment import NewAssignment
from classes import NewClass


class AssignmentsTab(qt.QWidget):
    def __init__(self):
        super().__init__()
        self.NewAssignmentButton = qt.QPushButton("+ Assignment")
        self.NewClassButton = qt.QPushButton("+ Class")
        self.AssignmentsList = qt.QListWidget()

        layout = qt.QHBoxLayout()
        layout.addWidget(self.NewAssignmentButton)
        layout.addWidget(self.NewClassButton)
        self.setLayout(layout)

        self.assignments = {}
        self.classes = load_data.load_classes()

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

    def AddClass(self):
        dialog = NewClass()
        if dialog.exec() == qt.QDialog.DialogCode.Accepted:
            name = dialog.class_name.text().strip()
            path = f"assignments/classes/{name}"
            if save_data.create_dir(path):
                qt.QMessageBox.warning(self,"Error","That class already exists.")
                return
            self.classes.append(name)
