import PySide6.QtCore as Qt
import PySide6.QtWidgets as qt

import load_data
import save_data
import utilities
from class_list import ClassList
from classes import Class, NewClass
from notebook import NewNoteBook, NoteBook
from notepage import NotePage, NoteSettings


class NotesTab(qt.QWidget):
    classAdded = Qt.Signal(str)
    classRemoved = Qt.Signal(str)
    def __init__(self):
        super().__init__()
        self.user = load_data.get_json("user.json")
        self.classes = list(self.user["classes_order_notes"])
        self.notebooks = load_data.get_json("notebooks.json")

        self.NewNoteButton = qt.QPushButton("+ Note Page")
        self.NewClassButton = qt.QPushButton("+ Class")
        self.NewNotebookButton = qt.QPushButton("+ Notebook")
        self.NotesList = ClassList()

        for class_name in self.classes:
            self.AddClassWidget(class_name)
        self.AddClassWidget("Unordered")
        notebooks = self.notebooks.copy()
        for notebook,data in notebooks.items():
            if data["class"] not in self.classes and data["class"] != "None":
                del self.notebooks[notebook]
            self.AddNotebookWidget(data)
        save_data.save_json("notebooks.json",self.notebooks)

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
        self.NewNotebookButton.clicked.connect(self.AddNoteBook)
    def AddClass(self):
        dialog = NewClass()
        if dialog.exec() == qt.QDialog.DialogCode.Accepted:
            name = dialog.class_name.text().strip()
            self.user = load_data.get_json("user.json")
            if name in self.user["classes_order_assignments"]:
                qt.QMessageBox.warning(self,"Error","That class already exists.")
                return
            self.user["classes_order_assignments"].append(name)
            self.user["classes_order_notes"].append(name)
            save_data.save_json("user.json",self.user)
            self.AddClassWidget(name)
            self.classAdded.emit(name)
            self.classes.append(name)

    def AddClassWidget(self,name):
        widget = Class(name)
        widget.delete_requested.connect(self.RemoveClassWidget)
        self.NotesList.addItem(widget)
    def AcceptClass(self,name):
        self.classes.append(name)
        self.AddClassWidget(name)
    def RemoveClass(self, name):
        self.classes.remove(name)
        if name in self.NotesList.classes:
            widget = self.NotesList.classes[name]["widget"]
            self.RemoveClassWidget(widget)
            self.NotesList.removeItem(widget)
    def RemoveClassWidget(self,widget):
        self.user = load_data.get_json("user.json")
        if widget.class_name in self.user["classes_order_assignments"]: self.user["classes_order_assignments"].remove(widget.class_name)
        if widget.class_name in self.user["classes_order_notes"]: self.user["classes_order_notes"].remove(widget.class_name)
        self.NotesList.removeItem(widget)
        save_data.save_json("user.json",self.user)
        self.classRemoved.emit(widget.class_name)
    def AddNote(self):
        dialog = NoteSettings()
        if dialog.exec() == qt.QDialog.DialogCode.Accepted:
            notes = load_data.get_json("notes.json")
            data = dialog.get_data()
            id = str(utilities.generate_id("notes.json"))
            data["id"] = id
            data["text"] = ""
            notes[id] = data
            save_data.save_json("notes.json", notes)


            dialog = NotePage(data)

            dialog.setModal(False)
            dialog.exec()
            data["text"] = dialog.textbox.toHtml()
            notes[id] = data
            save_data.save_json("notes.json",notes)
    def AddNoteBook(self):
        dialog = NewNoteBook()
        if dialog.exec() == qt.QDialog.DialogCode.Accepted:
            name = dialog.name.text().strip()
            self.notebooks = load_data.get_json("notebooks.json")
            id = utilities.generate_id("notebooks.json")
            data = {
                "name": name,
                "class": dialog.class_choice.currentText(),
                "index": len(self.notebooks),
                "id": id
            }

            self.notebooks[id] = data
            self.AddNotebookWidget(data)
            save_data.save_json("notebooks.json",self.notebooks)
    def AddNotebookWidget(self,data):
        notebook = NoteBook(data)
        #widget.delete_requested.connect(self.RemoveNotebook)
        #widget.edit_requested.connect(self.EditNotebook)
        self.NotesList.addItem(notebook)
