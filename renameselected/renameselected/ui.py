"""
    Provide a PySide2 dialog for the tool.
"""
from PySide2.QtWidgets import QWidget, QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton
from pymxs import runtime as rt

class PyMaxDialog(QDialog):
    """
    Custom dialog attached to the 3ds Max main window
    """
    def __init__(self, click, parent=QWidget.find(rt.windows.getMAXHWND())):
        super(PyMaxDialog, self).__init__(parent)
        self.setWindowTitle('Rename')

        main_layout = QVBoxLayout()
        label = QLabel("Enter new base name")
        main_layout.addWidget(label)

        edit = QLineEdit()
        main_layout.addWidget(edit)

        btn = QPushButton("Rename selected objects")
        btn.clicked.connect(lambda : click(edit.text()))
        main_layout.addWidget(btn)

        self.setLayout(main_layout)
        self.resize(250, 100)
