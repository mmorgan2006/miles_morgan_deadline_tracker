import PySide6.QtWidgets as qt

from tabs.assignments_tab import AssignmentsTab
from tabs.notes_tab import NotesTab


class MainWindow(qt.QMainWindow):
    def __init__(self):
        super().__init__()
        tabs = qt.QTabWidget()
        tabs.addTab(AssignmentsTab(),"Assignments")
        tabs.addTab(NotesTab(),"Notes")
        self.setCentralWidget(tabs)
        self.setWindowTitle("Unnamed Deadline Tracker")
        self.setMinimumHeight(500)
        self.setMinimumWidth(600)

        tabs.currentChanged.connect(self.on_tab_changed)
    def on_tab_changed(self,index):
        print(f"Switched to tab index: {index}")
if __name__ == "__main__":
    app = qt.QApplication()
    window = MainWindow()
    window.show()
    app.exec()
