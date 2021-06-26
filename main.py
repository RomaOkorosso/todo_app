import os
import sys
from typing import Optional

from todo.todo import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class NewTaskWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Task")
        self.setLayout(QVBoxLayout())
        title = QLineEdit()
        title.setObjectName("title")
        self.layout().addWidget(title)
        btn = QPushButton("Save", clicked=lambda: save_info())
        btn.setObjectName("save")
        self.layout().addWidget(btn)

        def save_info():
            txt = title.text()
            if txt != '':
                create_item(txt)

            self.close()
            w = Window()
            w.show()
            pass


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ToDo App")
        # self.resize(350, 550)
        layout = QVBoxLayout()
        self.setLayout(layout)
        btn = QPushButton("Add task", clicked=lambda: add_task())
        btn.setObjectName("change btn")
        self.layout().addWidget(btn)

        tasks: List[TODOItem] = get_all()
        for task in tasks:
            elem = self.create_elem(task.id, task.title, task.is_done)
            self.layout().addWidget(elem)

        def add_task():
            new_win = NewTaskWindow()
            new_win.show()
            self.close()

    def create_elem(self, e_id, e_title, e_is_done):
        topleft = QLabel(self)
        topleft.setText(f"{e_title}")
        if e_is_done:
            f = topleft.font()
            f.setStrikeOut(True)
            topleft.setFont(f)

        topright = QCheckBox(topleft, clicked=lambda: checker())
        topright.setObjectName(f"{e_id}")
        topright.setChecked((True if e_is_done != 0 else False))

        splitter1 = QSplitter(Qt.Horizontal, self)
        splitter1.addWidget(topleft)
        splitter1.addWidget(topright)

        def checker():
            now_state = topright.checkState()

            set_item_done(int(topright.objectName()), now_state.__bool__())
            f = topleft.font()
            f.setStrikeOut(now_state)
            topleft.setFont(f)

        return splitter1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    init()
    window = Window()
    window.show()
    sys.exit(app.exec_())
