import threading

import PySide6.QtCore as Qt
import PySide6.QtWidgets as qt

import load_data
import save_data
from class_list import ClassList
from classes import Class, NewClass
from notepage import NotePage


class NotesTab(qt.QWidget):
    classAdded = Qt.Signal(str, dict)
    classRemoved = Qt.Signal(str, dict)
    def __init__(self):
        super().__init__()
        self.user = load_data.get_json("user.json")
        self.classes = list(self.user["classes_order_notes"])

        self.NewNoteButton = qt.QPushButton("+ Note Page")
        self.NewClassButton = qt.QPushButton("+ Class")
        self.NewNotebookButton = qt.QPushButton("+ Notebook")
        self.NotesList = ClassList()

        for class_name in self.classes:
            self.AddClassWidget(class_name)
        self.AddClassWidget("Unordered")


        layout = qt.QVBoxLayout()
        buttons = qt.QHBoxLayout()
        buttons.addWidget(self.NewNoteButton)
        buttons.addWidget(self.NewNotebookButton)
        buttons.addWidget(self.NewClassButton)
        layout.addLayout(buttons)
        layout.addWidget(self.NotesList)
        self.setLayout(layout)



        self.NewClassButton.clicked.connect(self.AddClass)
        self.NewNoteButton.clicked.connect(self.AddNote)
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
            self.AddClassWidget(name)
            self.classAdded.emit(name, self.user)
            self.classes.append(name)

    def AddClassWidget(self,name):
        widget = Class(name)
        widget.delete_requested.connect(self.RemoveClassWidget)
        self.NotesList.addItem(widget)
    def AcceptClass(self,name,user):
        if user != self.user:
            self.user = user
            self.classes.append(name)
        self.AddClassWidget(name)
    def RemoveClass(self, name, user):
        if user != self.user:
            self.user = user
            self.classes.remove(name)
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
    def AddNote(self):
        note = load_data.get_json("notes.json")
        if len(note) > 0:
            dialog = NotePage(note)
        else:
            dialog = NotePage(None)
        dialog.setModal(False)
        dialog.exec()
        data = {"id": "0",
            "class": "none",
            "text": dialog.textbox.toHtml()}
        save_data.save_json("notes.json",data)
