import PySide6.QtWidgets as qt

from assignment import Assignment
from classes import Class
from due_date_sort import sort


class ClassList(qt.QWidget):
    def __init__(self):
        super().__init__()
        self.classes = {}
        scroll = qt.QScrollArea()
        scroll.setWidgetResizable(True)
        content = qt.QWidget()
        self.content_layout = qt.QVBoxLayout(content)
        scroll.setWidget(content)
        layout = qt.QVBoxLayout(self)
        layout.addWidget(scroll)
        self.content_layout.addStretch()
    def addItem(self, widget):
        if isinstance(widget,Class):
            if widget.name.text() in self.classes:
                return
            self.classes[widget.name.text()] = {"widget": widget,"assignments": []}
            self.content_layout.insertWidget(self.content_layout.count() - 1, widget)
            if "Unordered" in self.classes:
                self.content_layout.insertWidget(self.content_layout.count() - 1, self.classes["Unordered"]["widget"])


        elif isinstance(widget,Assignment):
            class_name = widget.data["class"]
            if widget.data["class"] == "None":
                class_name = "Unordered"
            self.classes[class_name]["widget"].addAssignment(widget)
            self.classes[class_name]["assignments"].append(widget)
    def removeItem(self, widget):
        self.content_layout.removeWidget(widget)
        if isinstance(widget,Assignment):
            if widget.data["class"] == "None":
                self.classes["Unordered"]["assignments"].remove(widget)
            else:
                self.classes[widget.data["class"]]["assignments"].remove(widget)
        else:
            self.classes.pop(widget.class_name)
        widget.deleteLater()
    def sort(self):
        for class_name in self.classes:
            arr = self.classes[class_name]["assignments"]
            if len(arr) > 1:
                class_widget = self.classes[class_name]["widget"]
                self.classes[class_name]["assignments"] = sort(arr,0,len(arr)-1)
                for i in range(len(arr)):
                    class_widget.content_layout.insertWidget(i, self.classes[class_name]["assignments"][i])
