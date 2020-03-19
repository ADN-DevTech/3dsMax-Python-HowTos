"""
    inbrowserhelp example: inbrowserhelp sample
"""
import webbrowser
import menuhook

TOPICS = [
    ("gettingstarted", "Getting Started With Python in 3ds Max",
     "help.autodesk.com/view/MAXDEV/2021/ENU/?guid=__developer_tutorials_creating_the_dialog_html"),
    ("howtos", "Python HowTos Github Repo",
     "https://github.com/ADN-DevTech/3dsMax-Python-HowTos"),
    ("pymxs", "Pymxs Online Documentation",
     "help.autodesk.com/view/MAXDEV/2021/ENU/?guid=__developer_using_pymxs_html"),
    ("pyside2", "Qt for Python Documentation (PySide2)",
     "doc.qt.io/qtforpython/contents.html"),
    ("python", "Python 3.7 Documentation",
     "docs.python.org/3.7/")
    ]

MENU_LOCATION = ["&Scripting", "Python3 Development", "Browse Documentation"]

def startup():
    """
    Hook the function to a menu item.
    """
    for topic in TOPICS:
        menuhook.register(
            f"inbrowserhelp_{topic[0]}",
            "howtos",
            lambda topic=topic: webbrowser.open(f"https://{topic[2]}"),
            MENU_LOCATION,
            text=topic[1],
            tooltip=topic[1])
