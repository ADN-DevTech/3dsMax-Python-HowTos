# HowTo: singleinstancedlg

This sample shows how to create a single instance modeless dialog.

*Goal:*
- learn how how to use findChild in PySide to create a single instance
dialog

## Explanations

The sample creates a custom PySide dialog and calls `setObjectName`
on it with a unique name. The `show_dialog()` function only creates
a new dialog if `findChild` cannot find the QDialog with the name
specified in `setObjectName`. The dialog (either found or created) is
then shown by calling `dialog.show()`.

# Understanding the code


In [ui.py](singleinstancedlg/ui.py), we first create a new
custom dialog class.

```python
from qtpy.QtWidgets import QWidget, QDialog, QVBoxLayout, QPushButton
from pymxs import runtime as rt

MAIN_WINDOW = QWidget.find(rt.windows.getMAXHWND())

class PyMaxDialog(QDialog):
    """
    Custom dialog attached to the 3ds Max main window
    """
```

We define a class variable that will be the unique name of this
dialog. We use the filename as a unique name:

```python
    unique_name = __file__
```

In the constructor we assign a unique name to the dialog:

```python
    def __init__(self, parent):
        super(PyMaxDialog, self).__init__(parent)
        self.setWindowTitle('Single Instance Dialog')

        # keep track of being unique
        self.setObjectName(PyMaxDialog.unique_name)
```

We then define a show\_dialog function that only creates
a dialog if an existing one cannot be found:

```python
def show_dialog():
    '''Show the dialog without duplicating it'''
    dialog = MAIN_WINDOW.findChild(QDialog, PyMaxDialog.unique_name)
    if dialog is None:
        dialog = PyMaxDialog(MAIN_WINDOW)
    dialog.show()
```
