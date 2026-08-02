import PySide6.QtCore as Qt
import PySide6.QtWidgets as qt

import load_data
import save_data
import utilities
from class_list import ClassList
from classes import Class, NewClass
from note import Note
from notebook import NewNoteBook, NoteBook
from notepage import NotePage, NoteSettings
from sort import sort


class NotesTab(qt.QWidget):
    classAdded = Qt.Signal(str)
    classRemoved = Qt.Signal(str)
    def __init__(self):
        super().__init__()
        self.user = load_data.get_json("user.json")
        self.classes = list(self.user["classes_order_notes"])
        self.notebooks = load_data.get_json("notebooks.json")
        self.notes = load_data.get_json("notes.json")

        self.NewNoteButton = qt.QPushButton("+ Note Page")
        self.NewClassButton = qt.QPushButton("+ Class")
        self.NewNotebookButton = qt.QPushButton("+ Notebook")
        self.NotesList = ClassList()

        for class_name in self.classes:
            self.AddClassWidget(class_name)
        self.AddClassWidget("Unordered")

        notebooks = self.notebooks.copy()
        notebook_widgets = []
        for notebook,data in notebooks.items():
            if data["class"] not in self.classes and data["class"] != "None":
                del self.notebooks[notebook]
                continue
            notebook = NoteBook(data)
            notebook_widgets.append(notebook)
        notebook_widgets = sort(notebook_widgets,0,len(notebook_widgets)-1)
        for notebook in notebook_widgets:
            self.AddNotebookWidget(notebook)
        notes = self.notes.copy()
        for note,data in notes.items():
            if (data["class"] not in self.classes and data["class"] != "None") or (data["notebook_id"] not in self.notebooks and data["notebook_id"] != "-1"):
                del self.notes[note]
                continue
            self.AddNoteWidget(data)
        save_data.save_json("notebooks.json",self.notebooks)
        save_data.save_json("notes.json",self.notes)


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
            dialog.exec()
            data["text"] = dialog.textbox.toHtml()
            notes[id] = data
            save_data.save_json("notes.json",notes)
            self.AddNoteWidget(data)
    def AddNoteBook(self):
        dialog = NewNoteBook()
        if dialog.exec() == qt.QDialog.DialogCode.Accepted:
            name = dialog.name.text().strip()
            self.notebooks = load_data.get_json("notebooks.json")
            id = str(utilities.generate_id("notebooks.json"))
            if dialog.class_choice.currentText() == "None": class_name = "Unordered"
            else: class_name = dialog.class_choice.currentText()
            data = {
                "name": name,
                "class": dialog.class_choice.currentText(),
                "index": len([i for i in self.NotesList.classes[class_name]["contents"] if isinstance(i, NoteBook)]),
                "id": id
            }

            self.notebooks[id] = data
            notebook = NoteBook(data)
            self.AddNotebookWidget(notebook)
            save_data.save_json("notebooks.json",self.notebooks)
            self.NotesList.sortNotebooks()
    def AddNotebookWidget(self, notebook):
        notebook.delete_requested.connect(self.RemoveNotebook)
        #notebook.edit_requested.connect(self.EditNotebook)
        notebook.move_requested.connect(self.move_notebook)
        self.NotesList.addItem(notebook)
    def AddNoteWidget(self, data):
        note = Note(data)
        self.NotesList.addItem(note)
    def RemoveNotebook(self, id):
        if id in self.NotesList.notebooks:
            self.notebooks = load_data.get_json("notebooks.json")
            index = self.notebooks[id]["index"]
            if self.notebooks[id]["class"] == "None": class_name = "Unordered"
            else: class_name = self.notebooks[id]["class"]

            for i in self.NotesList.classes[class_name]["contents"]:
                if isinstance(i, NoteBook) and self.notebooks[i.data["id"]]["index"] > index: self.notebooks[i.data["id"]]["index"] -= 1

            widget = self.NotesList.notebooks[id]["widget"]
            self.NotesList.removeItem(widget)
            del self.notebooks[id]
            save_data.save_json("notebooks.json",self.notebooks)
    def move_notebook(self, notebook, direction):
        notebooks = load_data.get_json("notebooks.json")
        if notebook.data["class"] == "None": class_name = "Unordered"
        else: class_name = notebook.data["class"]
        contents = self.NotesList.classes[class_name]["contents"]
        if notebook.data["index"] - direction < 0 or notebook.data["index"] - direction >= len(contents): return
        notebook2 = contents[notebook.data["index"]-direction]
        if isinstance(notebook2, NoteBook):
            contents[notebook.data["index"]] = notebook2
            contents[notebook.data["index"]-direction] = notebook
            notebook.data["index"] -= direction
            notebook2.data["index"] += direction

            notebooks[notebook.data["id"]] = notebook.data
            notebooks[notebook2.data["id"]] = notebook2.data
            save_data.save_json("notebooks.json",notebooks)
            self.NotesList.sortNotebooks()
        self.NotesList.classes[class_name]["contents"] = contents
