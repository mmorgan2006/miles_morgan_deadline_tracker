import PySide6.QtCore as Qt
import PySide6.QtWidgets as qt

import load_data
import save_data


class Class(qt.QFrame):
    delete_requested = Qt.Signal(object)
    edit_requested = Qt.Signal(str, str)
    move_requested = Qt.Signal(object, int)
    def __init__(self,name):
        super().__init__()

        self.setObjectName("ClassContainer")
        self.setStyleSheet("""
            #ClassContainer {
                border: 1px solid #222222;
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


        self.move_up_button = qt.QPushButton("▲")
        self.move_up_button.setFixedWidth(22)
        self.move_down_button = qt.QPushButton("▼")
        self.move_down_button.setFixedWidth(22)

        details = qt.QHBoxLayout()
        if self.class_name != "Unordered":
            details.addWidget(self.move_up_button)
            details.addWidget(self.move_down_button)
        details.addWidget(self.name)
        details.addWidget(qt.QLabel("(Class)"))
        details.addStretch()
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
        self.rename.clicked.connect(self.edit)
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
            "Delete Assignment",
            "Are you sure you want to permanently delete this class?\nThis will delete ALL assignments and notes inside this class.",
            qt.QMessageBox.StandardButton.Yes | qt.QMessageBox.StandardButton.No
        )
        if reply == qt.QMessageBox.StandardButton.Yes:
            self.delete_requested.emit(self)
    def edit(self):
        dialog = NewClass(self.class_name)
        if dialog.exec() == qt.QDialog.DialogCode.Accepted:
            classes = load_data.get_json("user.json")
            old_name = self.class_name
            self.class_name = dialog.class_name.text().strip()
            self.name.setText(self.class_name)
            classes["classes_order_assignments"][classes["classes_order_assignments"].index(old_name)] = self.class_name
            classes["classes_order_notes"][classes["classes_order_notes"].index(old_name)] = self.class_name

            save_data.save_json("user.json", classes)
            self.edit_requested.emit(old_name, self.class_name)
class NewClass(qt.QDialog):
    def __init__(self, name="",parent=None):
        super().__init__(parent)
        self.setWindowTitle("Class")
        self.setMinimumWidth(350)
        self.setMinimumHeight(90)

        self.class_name = qt.QLineEdit()
        self.class_name.setPlaceholderText("e.g. CS 120")
        self.class_name.setText(name)
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
