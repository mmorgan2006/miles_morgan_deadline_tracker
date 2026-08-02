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
        dialog = NotePage(self.data)
        dialog.exec()
        self.data["text"] = dialog.textbox.toHtml()
        notes[self.data["id"]] = self.data
        save_data.save_json("notes.json",notes)
