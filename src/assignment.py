import PySide6.QtCore as Qt
import PySide6.QtWidgets as qt

import load_data
from flowlayout import FlowLayout
from note import MiniNote
from notepicker import NotePicker
from utilities import convert_date


class Assignment(qt.QFrame):
    delete_requested = Qt.Signal(object)
    edit_requested = Qt.Signal(object, bool)
    def __init__(self, data):
        super().__init__()

        self.setObjectName("AssignmentCard")
        #self.setStyleSheet("""
        #    #AssignmentCard {
        #        background-color: #2b2b2b;
        #        border: 1px solid #3f3f3f;
        #       border-radius: 8px;
        #    }
        #""")


        self.data = data
        due_date = Qt.QDate.fromString(self.data["due_date"],"MM-dd-yyyy")
        days_until_due = Qt.QDate.currentDate().daysTo(due_date)

        name = qt.QLabel(data["name"])

        self.edit_button = qt.QPushButton("Edit")
        self.edit_button.setFixedWidth(50)

        self.delete_button = qt.QPushButton("delete")
        self.delete_button.setFixedWidth(80)

        self.details_button = qt.QPushButton("▼")
        self.details_button.setFixedWidth(30)
        self.details_button.setCheckable(True)
        self.details_button.setChecked(False)

        layout = qt.QVBoxLayout(self)
        top = qt.QHBoxLayout()
        top.addWidget(name)
        top.addWidget(self.edit_button)
        top.addWidget(self.details_button)
        layout.addLayout(top)

        bottom = qt.QHBoxLayout()
        due_date_label = qt.QLabel(f"Due in {days_until_due} days")
        if days_until_due < 0:
            due_date_label = qt.QLabel("Overdue")
            due_date_label.setStyleSheet("color: #FF0000;")
        if days_until_due == 0:
            due_date_label = qt.QLabel("Due Today")
            due_date_label.setStyleSheet("color: #FF0000;")
        if days_until_due == 1:
            due_date_label = qt.QLabel("Due Tomorrow")
            due_date_label.setStyleSheet("color: #FF0000;")
        if 7 > days_until_due >= 2: due_date_label.setStyleSheet("color: #FF9600;")
        bottom.addWidget(due_date_label)
        bottom.addWidget(self.delete_button)
        layout.addLayout(bottom)

        self.delete_button.setVisible(False)
        self.details = qt.QWidget()
        self.details.setVisible(False)




        due_date_label = qt.QLabel(f"Due Date: {convert_date(due_date)} {self.data["due_date"].replace("-","/")}")
        if days_until_due < 2: due_date_label.setStyleSheet("color: #FF0000;")
        if 7 > days_until_due >= 2: due_date_label.setStyleSheet("color: #FF9600;")



        details_top = qt.QHBoxLayout()
        details_top.addWidget(due_date_label)
        details_top.addStretch()


        details_layout = qt.QVBoxLayout(self.details)
        details_layout.addLayout(details_top)

        notes = load_data.get_json("notes.json")
        notebooks = load_data.get_json("notebooks.json")
        if "notes" in self.data:
            details_bottom = FlowLayout()
            for i in self.data["notes"]:
                if i in notes and (notes[i]["notebook_id"] in notebooks or notes[i]["notebook_id"] == "-1"):
                    note = MiniNote(i)
                    details_bottom.addWidget(note)
            details_layout.addLayout(details_bottom)
        if self.data["details"] != "":
            details_label = qt.QLabel(self.data["details"])
            details_label.setWordWrap(True)
            details_layout.addWidget(details_label)
        layout.addWidget(self.details)





        self.delete_button.clicked.connect(self.delete)
        self.edit_button.clicked.connect(self.edit)
        self.details_button.clicked.connect(self.toggle_details)
    def delete(self):
        reply = qt.QMessageBox.question(
            self,
            "Delete Assignment",
            "Are you sure you want to permanently delete this assignment?",
            qt.QMessageBox.StandardButton.Yes | qt.QMessageBox.StandardButton.No
        )
        if reply == qt.QMessageBox.StandardButton.Yes:
            self.delete_requested.emit(self)
    def edit(self):
        classes = load_data.get_json("user.json")["classes_order_assignments"]
        expanded = self.details_button.isChecked()
        self.dialog = NewAssignment(self.data, classes)
        if self.dialog.exec() == qt.QDialog.DialogCode.Accepted:
            self.edit_requested.emit(self, expanded)
    def toggle_details(self):
            expanded = self.details_button.isChecked()
            self.details.setVisible(expanded)
            self.delete_button.setVisible(expanded)

            self.details_button.setText("▲" if expanded else "▼")

class NewAssignment(qt.QDialog):
    def __init__(self, data, classes, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Assignment")
        self.setMinimumWidth(350)
        self.setMinimumHeight(200)

        self.assignment_name = qt.QLineEdit()
        self.assignment_name.setPlaceholderText("e.g. 'Chapter 1 Homework'")

        self.due = qt.QDateEdit()
        self.due.setCalendarPopup(True)
        self.due.setDate(Qt.QDate.currentDate())
        self.due.setMinimumDate(Qt.QDate.currentDate())

        self.class_choice = qt.QComboBox()
        self.class_choice.addItem("None")
        self.class_choice.addItems(classes)

        self.details = qt.QTextEdit()
        self.details.setPlaceholderText("Optional details...")
        self.details.setMaximumHeight(100)

        all_notes = load_data.get_json("notes.json")
        linked_ids = set()

        if data is not None:
            self.assignment_name.setText(data["name"])
            self.due.setDate(Qt.QDate.fromString(data["due_date"], "MM-dd-yyyy"))
            self.class_choice.setCurrentText(data["class"])
            self.details.setText(data["details"])
            linked_ids = {id for id in data.get("notes", []) if id in all_notes}

        self.note_picker = NotePicker(all_notes, linked_ids)

        form = qt.QFormLayout()
        form.addRow("Name: ",self.assignment_name)
        form.addRow("Class: ", self.class_choice)
        form.addRow("Due Date: ",self.due)
        form.addRow("Details: ",self.details)
        form.addRow("Notes: ",self.note_picker)

        buttons = qt.QDialogButtonBox(
            qt.QDialogButtonBox.StandardButton.Ok
            | qt.QDialogButtonBox.StandardButton.Cancel
        )
        layout = qt.QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(buttons)
        self.setLayout(layout)

        buttons.accepted.connect(self.validate)
        buttons.rejected.connect(self.reject)

    def validate(self):
        if not self.assignment_name.text().strip():
            self.assignment_name.setStyleSheet("border: 1px solid red;")
            return
        self.accept()

    def get_data(self):
        return {"name": self.assignment_name.text().strip(),
                "due_date": self.due.date().toString("MM-dd-yyyy"),
                "class": self.class_choice.currentText(),
                "details": self.details.toPlainText().strip(),
                "notes": list(self.note_picker.selected_ids())}
