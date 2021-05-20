# HowTo: inbrowserhelp

This sample shows how to open a page in the webbrowser from Python

## Explanations

The example creates a submenu in the Scripting -> Python3 Development menu,
called Browse Documentation. Each menu item in this menu opens the platform
browser in a location that may be useful to Python developers.

# Understanding the code

The standard `webbrowser` module is imported first:

```python
import webbrowser
```

The `menuhook` module is then imported. This module makes it easier to create
menu items in the 3ds Max menu system:

```python
import menuhook
```

The topics that need to be added in the submenu are then declared in a list
of tuples. The first element is a unique name for the item, the second
element is a description to be displayed in menu items, and the third element
is the url (without https://, this will be added later, forcing https and not
http to be used for everything).

```python
from pymxs import runtime as rt
MAX_VERSION = rt.maxversion()[7]
MAX_HELP = f"help.autodesk.com/view/MAXDEV/{MAX_VERSION}/ENU"

TOPICS = [
    ("gettingstarted", "Getting Started With Python in 3ds Max",
     f"{MAX_HELP}/?guid=Max_Python_API_tutorials_creating_the_dialog_html"),
    ("howtos", "Python HowTos Github Repo",
     "github.com/ADN-DevTech/3dsMax-Python-HowTos"),
    ("samples", "Python samples (Github Repo)",
     "github.com/ADN-DevTech/3dsMax-Python-HowTos/tree/master/src/samples"),
    ("pymxs", "Pymxs Online Documentation",
     f"{MAX_HELP}/?guid=Max_Python_API_using_pymxs_html"),
    ("pyside2", "Qt for Python Documentation (PySide2)",
     "doc.qt.io/qtforpython/contents.html"),
    ("python", "Python 3.7 Documentation",
     "docs.python.org/3.7/")
    ]
```

The MENU\_LOCATION constant gives the location in the menu system where the
new items need to be added:

```python
MENU_LOCATION = ["&Scripting", "Python3 Development", "Browse Documentation"]
```

With this, it is now possible to iterate the list of TOPICS and for each
topic to create a menu item:

```python
    for topic in TOPICS:
        menuhook.register(
            f"inbrowserhelp_{topic[0]}",
            "howtos",
            lambda topic=topic: webbrowser.open(f"https://{topic[2]}",
            MENU_LOCATION,
            text=topic[1],
            tooltip=topic[1])
```

Opening a topic simply consists in calling `webbrowser.open(f"https://{topic[2]}")`
when the menu item is activated.
