import PySide6.QtCore as Qt
import PySide6.QtGui as qtg
import PySide6.QtWidgets as qt

import load_data


class NotePage(qt.QDialog):
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle(data["name"])
        self.resize(800,600)
        self.setWindowFlags(
                self.windowFlags()
                | Qt.Qt.WindowMaximizeButtonHint #type: ignore
                | Qt.Qt.WindowMinimizeButtonHint #type: ignore
            )

        self.textbox = qt.QTextEdit()

        self.bold_button = qt.QPushButton("B")
        self.bold_button.setCheckable(True)
        self.bold_button.setFixedWidth(30)

        self.italic_button = qt.QPushButton("I")
        self.italic_button.setCheckable(True)
        self.italic_button.setFixedWidth(30)

        self.underline_button = qt.QPushButton("U")
        self.underline_button.setCheckable(True)
        self.underline_button.setFixedWidth(30)

        tools = qt.QHBoxLayout()
        tools.addWidget(self.bold_button)
        tools.addWidget(self.italic_button)
        tools.addWidget(self.underline_button)
        tools.addStretch()

        layout = qt.QVBoxLayout(self)
        layout.addLayout(tools)
        layout.addWidget(self.textbox)

        if data is not None:
            self.textbox.setHtml(data["text"])

        self.textbox.cursorPositionChanged.connect(self.update_toolbar)
        self.bold_button.clicked.connect(self.toggle_bold)
        self.italic_button.clicked.connect(self.toggle_italic)
        self.underline_button.clicked.connect(self.toggle_underline)
    def toggle_bold(self):
        format = qtg.QTextCharFormat()
        weight = qtg.QFont.Bold if self.bold_button.isChecked() else qtg.QFont.Normal #type: ignore
        format.setFontWeight(weight)
        self.merge_format(format)
    def toggle_italic(self):
        format = qtg.QTextCharFormat()
        format.setFontItalic(self.italic_button.isChecked())
        self.merge_format(format)
    def toggle_underline(self):
        format = qtg.QTextCharFormat()
        format.setFontUnderline(self.underline_button.isChecked())
        self.merge_format(format)

    def merge_format(self, format):
        cursor = self.textbox.textCursor()
        if not cursor.hasSelection():
            cursor.select(qtg.QTextCursor.SelectionType.WordUnderCursor)
        cursor.mergeCharFormat(format)
        self.textbox.mergeCurrentCharFormat(format)

    def update_toolbar(self):
        format = self.textbox.currentCharFormat()
        self.bold_button.setChecked(format.fontWeight() == qtg.QFont.Bold) #type: ignore
        self.italic_button.setChecked(format.fontItalic())
        self.underline_button.setChecked(format.fontUnderline())

class NoteSettings(qt.QDialog):
    def __init__(self,data=None ,parent=None):
        super().__init__(parent)
        classes = load_data.get_json("user.json")["classes_order_notes"]
        self.notebooks = load_data.get_json("notebooks.json")

        self.setWindowTitle("Note Page")
        self.setMinimumWidth(350)
        self.setMinimumHeight(140)

        self.name = qt.QLineEdit()
        self.name.setPlaceholderText("e.g. Monday Notes")

        self.class_choice = qt.QComboBox()
        self.class_choice.addItem("None")
        self.class_choice.addItems(classes)

        self.notebook_choice = qt.QComboBox()
        self.notebook_choice.addItem("None")

        form = qt.QFormLayout()
        form.addRow("Name: ",self.name)
        form.addRow("Class: ",self.class_choice)
        form.addRow("Notebook: ",self.notebook_choice)
        buttons = qt.QDialogButtonBox(
            qt.QDialogButtonBox.StandardButton.Ok
            | qt.QDialogButtonBox.StandardButton.Cancel
        )

        self.toggle_notebooks()
        if data != None:
            self.name.setText(data["name"])
            self.class_choice.setCurrentText(data["class"])
            self.toggle_notebooks()
            if data["notebook_id"] != "-1": self.notebook_choice.setCurrentText(self.notebooks[data["notebook_id"]]["name"])

        layout = qt.QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(buttons)
        layout.addStretch()

        buttons.accepted.connect(self.validate)
        buttons.rejected.connect(self.reject)

        self.class_choice.currentTextChanged.connect(self.toggle_notebooks)
    def validate(self):
        if not self.name.text().strip():
            self.name.setStyleSheet("border: 1px solid red;")
            return
        self.accept()
    def toggle_notebooks(self):
        notebooks = [f["name"] for f in self.notebooks.values() if f["class"] == self.class_choice.currentText()]
        self.notebook_ids = [f["id"] for f in self.notebooks.values() if f["class"] == self.class_choice.currentText()]
        self.notebook_choice.clear()
        self.notebook_choice.addItem("None")
        self.notebook_choice.addItems(notebooks)
    def get_data(self):
        if self.notebook_choice.currentIndex() - 1 < 0:
            id = "-1"
        else:
            id = str(self.notebook_ids[self.notebook_choice.currentIndex() - 1])
        return {
            "name": self.name.text().strip(),
            "class": self.class_choice.currentText(),
            "notebook_id": id
        }
