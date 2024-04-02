'''
    Demonstrates how to create a QWidget with PySide and attach it to the 3dsmax main window.
    Creates two types of dockable widgets, a QDockWidget and a QToolbar
'''

import os
import ctypes

from qtpy import QtCore
from qtpy import QtGui
from qtpy.QtWidgets import QMainWindow, QDockWidget, QToolButton, QToolBar, QAction

from pymxs import runtime as rt
from qtmax import GetQMaxMainWindow

def get_pos_to_dock_toolbar(dock_widget):
    """
    Get the docking widget position based on its size
    """
    space_between_widgets = 20 # Arbritrary hard coded value
    dock_widget_rect = dock_widget.geometry()
    x_pos = dock_widget_rect.x()
    y_pos = dock_widget_rect.bottom() + space_between_widgets
    return QtCore.QPoint(x_pos, y_pos)

def make_toolbar_floating(toolbar, pos):
    """
    Set the toolbar widget properties to act as a tool floating window
    """
    toolbar.setWindowFlags(
        QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint | QtCore.Qt.X11BypassWindowManagerHint)
    toolbar.move(pos)
    toolbar.adjustSize()
    toolbar.show()
    QtCore.QMetaObject.invokeMethod(toolbar, \
                                    "topLevelChanged", \
                                    QtCore.Qt.DirectConnection, \
                                    QtCore.QGenericArgument("bool", ctypes.c_void_p(True)))

def create_cylinder():
    """
    Create a cylinder node with predetermined radius and height values.
    """
    rt.Cylinder(radius=10, height=30)
    rt.redrawViews()

def demo_docking_widgets():
    """
    Demonstrates how to create a QWidget with PySide and attach it to the 3dsmax main window.
    Creates two types of dockable widgets, a QDockWidget and a QToolbar
    """
    # Retrieve 3ds Max Main Window QWdiget
    main_window = GetQMaxMainWindow()

    # QAction reused by both dockable widgets.
    cylinder_icon_path = os.path.dirname(os.path.realpath(__file__)) + "\\cylinder_icon_48.png"
    cylinder_icon = QtGui.QIcon(cylinder_icon_path)
    create_cyl_action = QAction(cylinder_icon, u"Create Cylinder", main_window)
    create_cyl_action.triggered.connect(create_cylinder)

    # QDockWidget construction and placement over the main window
    dock_widget = QDockWidget(main_window)

    # Set for position persistence
    dock_widget.setObjectName("Creators")
    # Set to see dock widget name in toolbar customize popup
    dock_widget.setWindowTitle("Creators")
    dock_tool_button = QToolButton()
    dock_tool_button.setAutoRaise(True)
    dock_tool_button.setDefaultAction(create_cyl_action)
    dock_tool_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
    dock_widget.setWidget(dock_tool_button)

    main_window.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock_widget)
    dock_widget.setFloating(True)
    dock_widget.show()

    # QToolBar construction and attachement to main window
    toolbar_widget = QToolBar(main_window)

    # Set for position persistence
    toolbar_widget.setObjectName("Creators TB")
    # Set to see dock widget name in toolbar customize popup
    toolbar_widget.setWindowTitle("Creators TB")
    toolbar_widget.setFloatable(True)
    toolbar_widget.addAction(create_cyl_action)

    main_window.addToolBar(QtCore.Qt.BottomToolBarArea, toolbar_widget)
    toolbar_widget.show()

    toolbar_position = get_pos_to_dock_toolbar(dock_widget)
    make_toolbar_floating(toolbar_widget, toolbar_position)

demo_docking_widgets()
