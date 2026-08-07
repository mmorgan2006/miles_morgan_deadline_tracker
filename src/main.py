import PySide6.QtWidgets as qt

import load_data
from style_update import apply_theme
from tabs.assignments_tab import AssignmentsTab
from tabs.notes_tab import NotesTab


class MainWindow(qt.QMainWindow):
    def __init__(self):
        super().__init__()
        tabs = qt.QTabWidget()
        assignments_tab = AssignmentsTab()
        notes_tab = NotesTab()
        tabs.addTab(assignments_tab,"Assignments")
        tabs.addTab(notes_tab,"Notes")
        self.setCentralWidget(tabs)
        self.setWindowTitle("Unnamed Deadline Tracker")
        self.setMinimumHeight(500)
        self.setMinimumWidth(400)
        self.resize(600,700)
        assignments_tab.classAdded.connect(notes_tab.AcceptClass)
        assignments_tab.classRemoved.connect(notes_tab.RemoveClass)
        assignments_tab.classEdit.connect(notes_tab.AcceptEdit)
        notes_tab.classAdded.connect(assignments_tab.AcceptClass)
        notes_tab.classRemoved.connect(assignments_tab.RemoveClass)
        notes_tab.classEdit.connect(assignments_tab.AcceptEdit)

if __name__ == "__main__":
    load_data.initialize()
    app = qt.QApplication()
    window = MainWindow()
    window.show()
    app.styleHints().colorSchemeChanged.connect(lambda: apply_theme(app))
    apply_theme(app)
    app.exec()
