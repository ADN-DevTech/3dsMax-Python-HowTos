# HowTo: pyconsole

This example integrates the nice [pyqtconsole](https://github.com/marcus-oscarsson/pyqtconsole)
as an alternative to the 3ds Max Listener.

This console behaves a lot more like a normal python console and 
provides syntax highlighting and autocomplete on top of that. Because
the console uses Qt, integrating it in 3ds Max is really easy.

## Understanding the code

The nice stuff is in [pyqtconsole](https://github.com/marcus-oscarsson/pyqtconsole). Here
I show how it is integrated to max.

The new\_console function:

```
def new_console():
    """
    Creates a new console and float it as a
    max widget
    """
```


Retrieves the main 3dsMax windows. This is a Qt window.

```
    main_window = GetQMaxMainWindow()
```

It then instanciates a new console:
```
    # create and setup a console
    console = PythonConsole(formats=HUGOS_THEME)
    console.setStyleSheet("background-color: #333333;")
```

And creates a QDockWidget as a container for the console. This
dock widget can be docked in the main max window.

```
    # create a dock widget for the console
    dock_widget = QDockWidget(main_window)
    dock_widget.setWidget(console)
    dock_widget.setObjectName("pyconsole")
    dock_widget.setWindowTitle("Python Console")
    main_window.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock_widget)
    dock_widget.setFloating(True)
    dock_widget.show()
```

Finally, the console is hooked to the qt event processing mechanism.
This is pretty awesome, no 3dsMax specific code is needed!

```
    # make the console do stuff
    console.eval_queued()
```

The awesomeness here is really that pymxs (or any other 3ds Max specific
thing) is not even needed!

