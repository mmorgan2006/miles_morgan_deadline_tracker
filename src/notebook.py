import PySide6.QtCore as Qt
import PySide6.QtWidgets as qt

import load_data


class NoteBook(qt.QFrame):
    delete_requested = Qt.Signal(object)
    move_requested = Qt.Signal(object, int)
    def __init__(self,data):
        super().__init__()
        name = data["name"]
        self.setObjectName("NoteContainer")
        self.setStyleSheet("""
            #ClassContainer {
                border: 1px solid #3f3f3f;
                border-radius: 10px;
            }
        """)
        self.data = data
        self.full_layout = qt.QVBoxLayout(self)
        self.class_name = data["class"]
        self.name = qt.QLabel(name)
        self.rename = qt.QPushButton("Edit")
        self.delete_button = qt.QPushButton("Delete")

        self.list_toggle = qt.QPushButton("▼")
        self.list_toggle.setFixedWidth(30)
        self.list_toggle.setCheckable(True)
        self.list_toggle.setChecked(False)

        self.move_up_button = qt.QPushButton("▲")
        self.move_up_button.setFixedWidth(22)
        self.move_down_button = qt.QPushButton("▼")
        self.move_down_button.setFixedWidth(22)


        details = qt.QHBoxLayout()
        details.addWidget(self.move_up_button)
        details.addWidget(self.move_down_button)
        details.addWidget(self.name)
        details.addStretch()
        if name != "Unordered":
            details.addWidget(self.rename)
            details.addWidget(self.delete_button)
        details.addWidget(self.list_toggle)
        self.full_layout.addLayout(details)
        self.container = qt.QWidget()
        self.content_layout = qt.QVBoxLayout(self.container)
        self.container.setVisible(False)
        self.full_layout.addWidget(self.container)

        self.list_toggle.clicked.connect(self.toggle_view)
        self.delete_button.clicked.connect(self.delete)
        self.move_up_button.clicked.connect(lambda: self.move_requested.emit(self, 1))
        self.move_down_button.clicked.connect(lambda: self.move_requested.emit(self, -1))
    def addItem(self,widget):
        self.content_layout.addWidget(widget)
    def removeItem(self, widget):
        self.content_layout.removeWidget(widget)
        widget.deleteLater()
    def toggle_view(self):
            expanded = self.list_toggle.isChecked()
            self.container.setVisible(expanded)
            self.list_toggle.setText("▲" if expanded else "▼")
    def delete(self):
        reply = qt.QMessageBox.question(
            self,
            "Delete Notebook",
            "Are you sure you want to permanently delete this notebook?\nThis will delete ALL notes inside this notebook.",
            qt.QMessageBox.StandardButton.Yes | qt.QMessageBox.StandardButton.No
        )
        if reply == qt.QMessageBox.StandardButton.Yes:
            self.delete_requested.emit(self.data["id"])



class NewNoteBook(qt.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        classes = load_data.get_json("user.json")["classes_order_notes"]
        self.setWindowTitle("Notebook")
        self.setMinimumWidth(350)
        self.setMinimumHeight(90)

        self.name = qt.QLineEdit()
        self.name.setPlaceholderText("e.g. Week 1 Notes")

        self.class_choice = qt.QComboBox()
        self.class_choice.addItem("None")
        self.class_choice.addItems(classes)

        form = qt.QFormLayout()
        form.addRow("Name: ",self.name)
        form.addRow("Class: ",self.class_choice)

        buttons = qt.QDialogButtonBox(
            qt.QDialogButtonBox.StandardButton.Ok
            | qt.QDialogButtonBox.StandardButton.Cancel
        )

        layout = qt.QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(buttons)
        self.setLayout(layout)

        buttons.accepted.connect(self.validate)
        buttons.rejected.connect(self.reject)
    def validate(self):
        if not self.name.text().strip() or self.name.text().strip() == "Unordered":
            self.name.setStyleSheet("border: 1px solid red;")
            return
        self.accept()
