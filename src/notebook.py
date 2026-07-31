import PySide6.QtCore as Qt
import PySide6.QtWidgets as qt

import load_data


class NoteBook(qt.QFrame):
    delete_requested = Qt.Signal(object)
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


        details = qt.QHBoxLayout()
        details.addWidget(self.name)
        details.addWidget(qt.QLabel("(Notebook)"))
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
    def addAssignment(self,widget):
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
            self.delete_requested.emit(self)
class NewNoteBook(qt.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        classes = load_data.get_json("user.json")["classes_order_notes"]
        self.setWindowTitle("Notebook")
        self.setMinimumWidth(350)
        self.setMinimumHeight(90)

        self.name = qt.QLineEdit()
        self.name.setPlaceholderText("e.g. CS 120")

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
