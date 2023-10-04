'''
 Demonstrates loading .ui files with PySide
'''
import os
from qtpy.QtWidgets import QMainWindow
from qtpy.QtCore import QFile
from qtpy.QtUiTools import QUiLoader
from pymxs import runtime as rt
from qtmax import GetQMaxMainWindow

class MyWindow(QMainWindow):
    """
    Main window class object loading a .ui file
    """
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setWindowTitle('Pyside2 Qt Window')
        self.init_ui()

    def init_ui(self):
        """ Prepare Qt UI layout for main window content """
        ui_file = QFile(os.path.dirname(os.path.realpath(__file__)) + "\\test_ui.ui")
        ui_file.open(QFile.ReadOnly)
        self.loaded_ui = QUiLoader().load(ui_file, self)
        ui_file.close()

def demo_ui_loader():
    """
    Entry point to demonstrate how to load a .ui file
    """
    win = MyWindow(GetQMaxMainWindow())
    win.show()

demo_ui_loader()
