import PySide6.QtCore as Qt
import PySide6.QtWidgets as qt

import load_data
import save_data
from notepage import NotePage, NoteSettings


class Note(qt.QPushButton):
    edit_requested = Qt.Signal(object)
    delete_requested = Qt.Signal(object)
    def __init__(self,data):
        super().__init__()
        self.setObjectName("NoteCard")
        self.setFixedHeight(40)
        self.data = data
        self.id = data["id"]

        self.name = qt.QLabel(data["name"])
        self.edit_button = qt.QPushButton("Edit")
        self.edit_button.setFixedWidth(40)
        self.delete_button = qt.QPushButton("Delete")
        self.delete_button.setFixedWidth(55)
        self.export_button = qt.QPushButton("Export")
        self.export_button.setFixedWidth(55)

        layout = qt.QHBoxLayout(self)
        layout.addWidget(self.name)
        layout.addStretch()
        layout.addWidget(self.export_button)
        layout.addWidget(self.edit_button)
        layout.addWidget(self.delete_button)

        self.clicked.connect(self.open_note)
        self.edit_button.clicked.connect(self.edit_note)
        self.delete_button.clicked.connect(self.delete_note)
    def open_note(self):
        notes = load_data.get_json("notes.json")
        data = notes[self.id]
        dialog = NotePage(data)
        dialog.exec()
        data["text"] = dialog.textbox.toHtml()
        notes[data["id"]] = data
        save_data.save_json("notes.json",notes)
    def edit_note(self):
        notes = load_data.get_json("notes.json")
        self.data = notes[self.id]
        self.dialog = NoteSettings(self.data)
        if self.dialog.exec() == qt.QDialog.DialogCode.Accepted:
            self.newdata = self.dialog.get_data()
            self.newdata["id"] = self.data["id"]
            self.newdata["text"] = self.data["text"]
            notes[self.id] = self.newdata
            save_data.save_json("notes.json", notes)
            self.edit_requested.emit(self)
    def delete_note(self):
        reply = qt.QMessageBox.question(
            self,
            "Delete Notepage",
            "Are you sure you want to permanently delete this note?",
            qt.QMessageBox.StandardButton.Yes | qt.QMessageBox.StandardButton.No
        )
        if reply == qt.QMessageBox.StandardButton.Yes:
            self.delete_requested.emit(self)

class MiniNote(qt.QPushButton):
    def __init__(self,id):
        super().__init__()
        self.data = load_data.get_json("notes.json")[id]
        self.id = id
        self.setText(self.data["name"])
        self.setSizePolicy(qt.QSizePolicy.Fixed, qt.QSizePolicy.Fixed) #type: ignore

        self.setStyleSheet("""
            QPushButton {
                border-radius:10px;
                padding: 6px 16px;
                background-color: #3b82f6;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
        """)
        self.clicked.connect(self.open_note)
    def open_note(self):
        notes = load_data.get_json("notes.json")
        notebooks = load_data.get_json("notebooks.json")
        if self.id not in notes or (self.data["notebook_id"] not in notebooks and self.data["notebook_id"] != "-1"):
            qt.QMessageBox.warning(self,"Error","These notes are missing or deleted.")
            self.deleteLater()
        else:
            if self.text() != notes[self.id]["name"]:
                self.setText(notes[self.id]["name"])
            data = notes[self.id]
            dialog = NotePage(data)
            dialog.exec()
            data["text"] = dialog.textbox.toHtml()
            notes[data["id"]] = data
            save_data.save_json("notes.json",notes)
