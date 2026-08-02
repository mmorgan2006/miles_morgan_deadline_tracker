import PySide6.QtWidgets as qt

import load_data
import save_data
from notepage import NotePage


class Note(qt.QPushButton):
    def __init__(self,data):
        super().__init__()

        self.setFixedHeight(40)
        self.data = data
        self.id = data["id"]

        self.name = qt.QLabel(data["name"])
        self.edit_button = qt.QPushButton("Edit")
        self.delete_button = qt.QPushButton("Delete")

        layout = qt.QHBoxLayout(self)
        layout.addWidget(self.name)
        layout.addStretch()
        layout.addWidget(self.edit_button)
        layout.addWidget(self.delete_button)

        self.clicked.connect(self.open_note)
    def open_note(self):
        notes = load_data.get_json("notes.json")
        data = notes[self.id]
        dialog = NotePage(data)
        dialog.exec()
        data["text"] = dialog.textbox.toHtml()
        notes[data["id"]] = data
        save_data.save_json("notes.json",notes)


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
        if self.id in notes:
            if self.text() != notes[self.id]["name"]:
                self.setText(notes[self.id]["name"])
            data = notes[self.id]
            dialog = NotePage(data)
            dialog.exec()
            data["text"] = dialog.textbox.toHtml()
            notes[data["id"]] = data
            save_data.save_json("notes.json",notes)
        else:
            qt.QMessageBox.warning(self,"Error","These notes are missing or deleted.")
            self.deleteLater()
