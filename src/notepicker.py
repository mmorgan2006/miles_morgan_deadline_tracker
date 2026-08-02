import PySide6.QtCore as Qt
import PySide6.QtWidgets as qt


class NotePicker(qt.QWidget):
    def __init__(self, all_notes: dict, linked_ids: set[str]):
        super().__init__()
        self.all_notes = all_notes
        self.checked_ids = set(linked_ids)

        layout = qt.QVBoxLayout(self)

        self.search = qt.QLineEdit()
        self.search.setPlaceholderText("Search notes...")
        self.search.textChanged.connect(self.filter_list)
        layout.addWidget(self.search)

        self.list_widget = qt.QListWidget()
        self.list_widget.setMaximumHeight(180)
        self.list_widget.itemChanged.connect(self.on_item_changed)
        layout.addWidget(self.list_widget)

        self.populate()

    def populate(self):
        self.list_widget.clear()
        for note_id, note_data in self.all_notes.items():
            item = qt.QListWidgetItem(note_data["name"])
            item.setData(Qt.Qt.ItemDataRole.UserRole, note_id)
            item.setFlags(item.flags() | Qt.Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(
                Qt.Qt.CheckState.Checked if note_id in self.checked_ids
                else Qt.Qt.CheckState.Unchecked
            )
            self.list_widget.addItem(item)

    def on_item_changed(self, item):
        id = item.data(Qt.Qt.ItemDataRole.UserRole)
        if item.checkState() == Qt.Qt.CheckState.Checked:
            self.checked_ids.add(id)
        else:
            self.checked_ids.discard(id)
    def filter_list(self, text):
        text = text.lower().strip()
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            item.setHidden(text not in item.text().lower())

    def selected_ids(self):
        return list(self.checked_ids)
