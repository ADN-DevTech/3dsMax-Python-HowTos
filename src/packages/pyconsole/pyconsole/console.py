from qtmax import GetQMaxMainWindow
from pyqtconsole.console import PythonConsole
import pyqtconsole.highlighter as hl
from PySide2.QtWidgets import QWidget, QMainWindow, QDockWidget, QToolButton, QToolBar, QAction
from PySide2 import QtCore

# My personal choice of colors
HUGOS_THEME =  {
    'keyword': hl.format('#7bd5d2', 'italic'),
    'operator': hl.format('#6ab6ba'),
    'brace': hl.format('#668799'),
    'defclass': hl.format('#b86e1e', 'bold'),
    'string': hl.format('#9fba4d'),
    'string2': hl.format('#9fba4d', 'italic'),
    'comment': hl.format('#585858', 'italic'),
    'self': hl.format('#ffb964', 'italic'),
    'numbers': hl.format('#cf6a4c'),
    'inprompt': hl.format('#7bd5d2', 'bold'),
    'outprompt': hl.format('#d5d07b')
    }

def new_console(tabto = None, floating = False, dockingarea = QtCore.Qt.RightDockWidgetArea):
    """
    Create a new console and float it as a max widget
    tabto: name of a widget on top of which the console should be tabbed
    """
    main_window = GetQMaxMainWindow()

    # create and setup a console
    console = PythonConsole(formats=HUGOS_THEME)
    console.setStyleSheet("background-color: #333333;")

    # create a dock widget for the console
    dock_widget = QDockWidget(main_window)
    dock_widget.setWidget(console)
    dock_widget.setObjectName("pyconsole")
    dock_widget.setWindowTitle("Python Console")
    main_window.addDockWidget(dockingarea, dock_widget)
    if (not tabto is None):
        tabw = main_window.findChild(QWidget, tabto)
        main_window.tabifyDockWidget(tabw, dock_widget)
    dock_widget.setFloating(floating)
    dock_widget.show()

    # make the console do stuff
    console.eval_queued()
    return console
