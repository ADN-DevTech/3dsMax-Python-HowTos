"""
    PySide2 modeless dialog that will not be started more than once
    at the same time
"""
#pylint: disable=no-name-in-module
#pylint: disable=too-few-public-methods
from PySide2.QtWidgets import QWidget, QDialog, QVBoxLayout, QPushButton
from pymxs import runtime as rt

MAIN_WINDOW = QWidget.find(rt.windows.getMAXHWND())

class PyMaxDialog(QDialog):
    """
    Custom dialog attached to the 3ds Max main window
    """
    unique_name = __file__
    def __init__(self, parent):
        super(PyMaxDialog, self).__init__(parent)
        self.setWindowTitle('Single Instance Dialog')

        # keep track of being unique
        self.setObjectName(PyMaxDialog.unique_name)

        main_layout = QVBoxLayout()

        btn = QPushButton("Dummy Button")
        main_layout.addWidget(btn)

        self.setLayout(main_layout)
        self.resize(250, 100)

def show_dialog():
    '''Show the dialog without duplicating it'''
    dialog = MAIN_WINDOW.findChild(QDialog, PyMaxDialog.unique_name)
    if dialog is None:
        dialog = PyMaxDialog(MAIN_WINDOW)
    dialog.show()
