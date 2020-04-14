'''
    Demonstrates how to create a QDialog with PySide2 and attach it to the 3ds Max main window.
'''

from PySide2.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton
from pymxs import runtime as rt
from qtmax import GetQMaxMainWindow

def create_cylinder():
    """
    Create a cylinder node with predetermined radius and height values.
    """
    rt.Cylinder(radius=10, height=30)
    # force a viewport update for the node to appear
    rt.redrawViews()

class PyMaxDialog(QDialog):
    """
    Custom dialog attached to the 3ds Max main window
    Message label and action push button to create a cylinder in the 3ds Max scene graph
    """
    def __init__(self, parent=None):
        super(PyMaxDialog, self).__init__(parent)
        self.setWindowTitle('Pyside2 Qt Window')
        self.init_ui()

    def init_ui(self):
        """ Prepare Qt UI layout for custom dialog """
        main_layout = QVBoxLayout()
        label = QLabel("Click button to create a cylinder in the scene")
        main_layout.addWidget(label)

        cylinder_btn = QPushButton("Cylinder")
        cylinder_btn.clicked.connect(create_cylinder)
        main_layout.addWidget(cylinder_btn)

        self.setLayout(main_layout)
        self.resize(250, 100)

def demo_simple_dialog():
    """
    Entry point for QDialog demo making use of PySide2 and pymxs
    """
    # reset 3ds Max
    rt.resetMaxFile(rt.Name('noPrompt'))

    dialog = PyMaxDialog(GetQMaxMainWindow())
    dialog.show()

demo_simple_dialog()
