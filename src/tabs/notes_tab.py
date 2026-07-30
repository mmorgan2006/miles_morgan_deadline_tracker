import PySide6.QtWidgets as qt


class NotesTab(qt.QWidget):
    def __init__(self):
        super().__init__()
        full = qt.QVBoxLayout()
        full.addWidget(qt.QLabel("Temp"))
        self.setLayout(full)
