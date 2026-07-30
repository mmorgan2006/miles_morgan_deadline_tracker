import PySide6.QtWidgets as qt


class NewClass(qt.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Class")
        self.setMinimumWidth(350)
        self.setMinimumHeight(90)

        self.class_name = qt.QLineEdit()
        self.class_name.setPlaceholderText("e.g. CS 120")

        form = qt.QFormLayout()
        form.addRow("Class: ",self.class_name)

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
        if not self.class_name.text().strip():
            self.class_name.setStyleSheet("border: 1px solid red;")
            return
        self.accept()
