import PySide6.QtWidgets as qt
from PySide6.QtCore import QDate


class Assignment(qt.QWidget):
    def __init__(self):
        pass
class NewAssignment(qt.QDialog):
    def __init__(self, classes, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Assignment")
        self.setMinimumWidth(350)
        self.setMinimumHeight(200)

        self.assignment_name = qt.QLineEdit()
        self.assignment_name.setPlaceholderText("e.g. 'Chapter 1 Homework'")

        self.due = qt.QDateEdit()
        self.due.setCalendarPopup(True)
        self.due.setDate(QDate.currentDate())
        self.due.setMinimumDate(QDate.currentDate())

        self.class_choice = qt.QComboBox()
        self.class_choice.addItem("None")
        self.class_choice.addItems(classes)

        self.notes = qt.QTextEdit()
        self.notes.setPlaceholderText("Optional notes...")
        self.notes.setMaximumHeight(100)

        form = qt.QFormLayout()
        form.addRow("Name: ",self.assignment_name)
        form.addRow("Class: ", self.class_choice)
        form.addRow("Due Date: ",self.due)
        form.addRow("Notes: ",self.notes)

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
        if not self.assignment_name.text().strip():
            self.assignment_name.setStyleSheet("border: 1px solid red;")
            return
        self.accept()

    def get_data(self):
        return {
            "name": self.assignment_name.text().strip(),
            "due_date": self.due.date().toString("yyyy-MM-dd"),
            "notes": self.notes.toPlainText().strip()
        }, self.class_choice.currentText()
