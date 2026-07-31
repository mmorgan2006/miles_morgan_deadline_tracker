import PySide6.QtWidgets as qt

from assignment import Assignment
from classes import Class
from due_date_sort import sort
from notebook import NoteBook


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
            self.classes[widget.name.text()] = {"widget": widget,"contents": []}
            self.content_layout.insertWidget(self.content_layout.count() - 1, widget)
            if widget.name != "Unordered" and "Unordered" in self.classes:
                    self.content_layout.insertWidget(self.content_layout.count() - 2, self.classes["Unordered"]["widget"])


        elif isinstance(widget, (Assignment, NoteBook)):
            class_name = widget.data["class"]
            if widget.data["class"] == "None":
                class_name = "Unordered"
            self.classes[class_name]["widget"].addItem(widget)
            self.classes[class_name]["contents"].append(widget)
    def removeItem(self, widget):
        self.content_layout.removeWidget(widget)
        if isinstance(widget,Assignment):
            if widget.data["class"] == "None":
                self.classes["Unordered"]["contents"].remove(widget)
            else:
                self.classes[widget.data["class"]]["contents"].remove(widget)
        else:
            if widget.class_name in self.classes: del self.classes[widget.class_name]
        widget.deleteLater()
    def sort(self):
        for class_name in self.classes:
            arr = self.classes[class_name]["contents"]
            if len(arr) > 1:
                class_widget = self.classes[class_name]["widget"]
                self.classes[class_name]["contents"] = sort(arr,0,len(arr)-1)
                for i in range(len(arr)):
                    class_widget.content_layout.insertWidget(i, self.classes[class_name]["contents"][i])
