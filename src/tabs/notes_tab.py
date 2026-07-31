import PySide6.QtCore as Qt
import PySide6.QtWidgets as qt

import load_data
import save_data
from class_list import ClassList
from classes import Class, NewClass


class NotesTab(qt.QWidget):
    classAdded = Qt.Signal(str, dict)
    classRemoved = Qt.Signal(str, dict)
    def __init__(self):
        super().__init__()
        self.user = load_data.get_json("user.json")
        self.classes = self.user["classes_order_notes"]

        self.NewAssignmentButton = qt.QPushButton("+ Note Page")
        self.NewClassButton = qt.QPushButton("+ Class")
        self.NotesList = ClassList()

        for class_name in self.classes:
            self.AddClassWidget(class_name,self.user)
        self.AddClassWidget("Unordered",self.user)


        layout = qt.QVBoxLayout()
        buttons = qt.QHBoxLayout()
        buttons.addWidget(self.NewAssignmentButton)
        buttons.addWidget(self.NewClassButton)
        layout.addLayout(buttons)
        layout.addWidget(self.NotesList)
        self.setLayout(layout)

        self.NewClassButton.clicked.connect(self.AddClass)

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
            self.AddClassWidget(name, self.user)
            self.classAdded.emit(name, self.user)
    def AddClassWidget(self,name,user):
        self.user = user
        widget = Class(name)
        widget.delete_requested.connect(self.RemoveClassWidget)
        self.NotesList.addItem(widget)
    def RemoveClass(self, name, user):
        self.user = user
        if name in self.NotesList.classes:
            widget = self.NotesList.classes[name]["widget"]
            self.RemoveClassWidget(widget)
            self.NotesList.removeItem(widget)
    def RemoveClassWidget(self,widget):
        if widget.class_name in self.user["classes_order_assignments"]: self.user["classes_order_assignments"].remove(widget.class_name)
        if widget.class_name in self.user["classes_order_notes"]: self.user["classes_order_notes"].remove(widget.class_name)
        self.NotesList.removeItem(widget)
        save_data.save_json("user.json",self.user)
        self.classRemoved.emit(widget.class_name, self.user)
