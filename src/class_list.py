import PySide6.QtWidgets as qt

from assignment import Assignment
from classes import Class
from note import Note
from notebook import NoteBook
from sort import sort


class ClassList(qt.QFrame):
    def __init__(self):
        super().__init__()

        self.setObjectName("ClassList")

        self.classes = {}
        self.notebooks = {}
        scroll = qt.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(qt.QFrame.Shape.NoFrame)
        scroll.viewport().setAutoFillBackground(False)

        content = qt.QWidget()
        content.setObjectName("ClassListContent")

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
            if isinstance(widget, NoteBook):
                self.notebooks[str(widget.data["id"])] = {"widget": widget,"contents": []}
        elif isinstance(widget, Note):
            class_name = widget.data["class"]
            notebook_id = str(widget.data["notebook_id"])
            if notebook_id != "-1":
                self.notebooks[notebook_id]["widget"].addItem(widget)
                self.notebooks[notebook_id]["contents"].append(widget)
            else:
                if widget.data["class"] == "None":
                    class_name = "Unordered"
                self.classes[class_name]["widget"].addItem(widget)
                self.classes[class_name]["contents"].append(widget)
    def removeItem(self, widget):
        self.content_layout.removeWidget(widget)
        if isinstance(widget,(Assignment,NoteBook)):
            data = widget.data.copy()
            if widget.data["class"] == "None":
                self.classes["Unordered"]["contents"].remove(widget)
            else:
                self.classes[widget.data["class"]]["contents"].remove(widget)
            if isinstance(widget, NoteBook):
                del self.notebooks[data["id"]]
        elif isinstance(widget,Note):
            if widget.data["notebook_id"] == "-1":
                if widget.data["class"] == "None":
                    self.classes["Unordered"]["contents"].remove(widget)
                else:
                    self.classes[widget.data["class"]]["contents"].remove(widget)
            else:
                self.notebooks[widget.data["notebook_id"]]["contents"].remove(widget)
        else:
            if widget.class_name in self.classes: del self.classes[widget.class_name]
        widget.deleteLater()
    def sortAssignments(self):
        for class_name in self.classes:
            arr = self.classes[class_name]["contents"]
            if len(arr) > 1:
                class_widget = self.classes[class_name]["widget"]
                self.classes[class_name]["contents"] = sort(arr,0,len(arr)-1)
                for i in range(len(arr)):
                    class_widget.content_layout.insertWidget(i, self.classes[class_name]["contents"][i])
    def sortNotebooks(self):
        notebooks = [i["widget"] for i in self.notebooks.values()]
        for i in sort(notebooks,0,len(notebooks)-1):
            if i.data["class"] == "None": class_name = "Unordered"
            else: class_name = i.data["class"]
            self.classes[class_name]["widget"].content_layout.removeWidget(i)
            self.classes[class_name]["widget"].content_layout.addWidget(i)

        for list in [n["contents"] for n in self.classes.values()]:
            for i in list:
                if isinstance(i, Note):
                    if i.data["class"] == "None": class_name = "Unordered"
                    else: class_name = i.data["class"]
                    self.classes[class_name]["widget"].content_layout.removeWidget(i)
                    self.classes[class_name]["widget"].content_layout.addWidget(i)
