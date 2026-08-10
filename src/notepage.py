import PySide6.QtCore as Qt
import PySide6.QtGui as qtg
import PySide6.QtWidgets as qt

import load_data
from import_file import import_docx


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
        self.textbox.setPlaceholderText("Type text here! Wow!")

        self.bold_button = qt.QPushButton("B")
        self.bold_button.setCheckable(True)
        self.bold_button.setFixedWidth(30)

        self.italic_button = qt.QPushButton("I")
        self.italic_button.setCheckable(True)
        self.italic_button.setFixedWidth(30)

        self.underline_button = qt.QPushButton("U")
        self.underline_button.setCheckable(True)
        self.underline_button.setFixedWidth(30)

        self.font_combo = qt.QFontComboBox()

        self.size_spin = qt.QSpinBox()
        self.size_spin.setRange(6, 96)
        self.size_spin.setValue(12)

        self.color_btn = qt.QPushButton("Color")
        self._current_color = qtg.QColor("black")

        tools = qt.QHBoxLayout()
        tools.addWidget(self.font_combo)
        tools.addWidget(self.size_spin)
        tools.addWidget(self.bold_button)
        tools.addWidget(self.italic_button)
        tools.addWidget(self.underline_button)
        tools.addWidget(self.color_btn)
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
        self.font_combo.currentFontChanged.connect(self.change_font_family)
        self.size_spin.valueChanged.connect(self.change_font_size)
        self.color_btn.clicked.connect(self.change_font_color)
        self._update_color_btn_icon()
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
            fmt = self.textbox.currentCharFormat()
            self.bold_button.setChecked(fmt.fontWeight() == qtg.QFont.Bold) #type: ignore
            self.italic_button.setChecked(fmt.fontItalic())
            self.underline_button.setChecked(fmt.fontUnderline())

            self.font_combo.blockSignals(True)
            self.font_combo.setCurrentFont(fmt.font())
            self.font_combo.blockSignals(False)

            self.size_spin.blockSignals(True)
            size = fmt.fontPointSize()
            self.size_spin.setValue(int(size) if size > 0 else 12)
            self.size_spin.blockSignals(False)

            self._current_color = fmt.foreground().color()
            self._update_color_btn_icon()


    def change_font_family(self, font: qtg.QFont):
        fmt = qtg.QTextCharFormat()
        fmt.setFontFamilies([font.family()])
        self.merge_format(fmt)

    def change_font_size(self, size: int):
        fmt = qtg.QTextCharFormat()
        fmt.setFontPointSize(size)
        self.merge_format(fmt)

    def change_font_color(self):
        color = qt.QColorDialog.getColor(self._current_color, self, "Select Text Color")
        if color.isValid():
            self._current_color = color
            self._update_color_btn_icon()
            fmt = qtg.QTextCharFormat()
            fmt.setForeground(color)
            self.merge_format(fmt)

    def _update_color_btn_icon(self):
        pixmap = qtg.QPixmap(16, 16)
        pixmap.fill(self._current_color)
        self.color_btn.setIcon(qtg.QIcon(pixmap))

class NoteSettings(qt.QDialog):
    def __init__(self,data=None ,parent=None):
        super().__init__(parent)
        self.text = ""
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

        self.import_button = qt.QPushButton("Import")

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
        if data is None:
            layout.addWidget(self.import_button)
        layout.addWidget(buttons)
        layout.addStretch()

        buttons.accepted.connect(self.validate)
        buttons.rejected.connect(self.reject)

        self.class_choice.currentTextChanged.connect(self.toggle_notebooks)
        self.import_button.clicked.connect(self.import_notes)
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
            "notebook_id": id,
            "text": self.text
        }
    def import_notes(self):
        try:
            self.text,name = import_docx() #type: ignore
            self.name.setText(name)
        except Exception:  # noqa: BLE001
            print("Import Cancelled")
