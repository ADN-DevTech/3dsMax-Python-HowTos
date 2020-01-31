"""
    inbrowserhelp example: inbrowserhelp sample
"""
import webbrowser
import menuhook

TOPICS = [
    ("gettingstarted", "Getting Started With Python in 3ds Max",
     "git.autodesk.com/windish/maxpythontutorials"),
    ("howtos", "Python HowTos Github Repo",
     "git.autodesk.com/windish/pythonhowtos"),
    ("pymxs", "Pymxs Online Documentation",
     "help-beta.autodesk.com/view/MAXDEV/2021/ENU/?guid=__developer_using_pymxs_html"),
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
            "inbrowserhelp_{}".format(topic[0]),
            "howtos",
            lambda topic=topic: webbrowser.open("https://{}".format(topic[2])),
            MENU_LOCATION,
            text=topic[1],
            tooltip=topic[1])
