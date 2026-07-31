import PySide6.QtGui as qtg
import PySide6.QtWidgets as qt


class NotePage(qt.QDialog):
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle("Note Page")
        self.resize(800,600)

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
    def toggle_bold(self):
        format = qtg.QTextCharFormat()
        weight = qtg.QFont.Bold if self.bold_button.isChecked() else qtg.QFont.Normal #type: ignore
        format.setFontWeight(weight)
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
