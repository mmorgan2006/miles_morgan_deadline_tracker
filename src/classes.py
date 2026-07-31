import PySide6.QtCore as Qt
import PySide6.QtWidgets as qt


class Class(qt.QFrame):
    delete_requested = Qt.Signal(object)
    def __init__(self,name):
        super().__init__()

        self.setObjectName("ClassContainer")
        self.setStyleSheet("""
            #ClassContainer {
                border: 1px solid #333333;
                border-radius: 10px;
            }
        """)

        self.full_layout = qt.QVBoxLayout(self)
        self.class_name = name
        self.name = qt.QLabel(name)
        self.rename = qt.QPushButton("Rename")
        self.delete_button = qt.QPushButton("Delete")

        self.list_toggle = qt.QPushButton("▲")
        self.list_toggle.setFixedWidth(30)
        self.list_toggle.setCheckable(True)
        self.list_toggle.setChecked(True)


        details = qt.QHBoxLayout()
        details.addWidget(self.name)
        if name != "Unordered":
            details.addWidget(self.rename)
            details.addWidget(self.delete_button)
        details.addWidget(self.list_toggle)
        self.full_layout.addLayout(details)
        self.container = qt.QWidget()
        self.content_layout = qt.QVBoxLayout(self.container)
        self.container.setVisible(True)
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
            "Delete Assignment",
            "Are you sure you want to permanently delete this class?\nThis will delete ALL assignments and notes inside this class.",
            qt.QMessageBox.StandardButton.Yes | qt.QMessageBox.StandardButton.No
        )
        if reply == qt.QMessageBox.StandardButton.Yes:
            self.delete_requested.emit(self)
class NewClass(qt.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Class")
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
        if not self.class_name.text().strip() or self.class_name.text().strip() == "Unordered":
            self.class_name.setStyleSheet("border: 1px solid red;")
            return
        self.accept()
