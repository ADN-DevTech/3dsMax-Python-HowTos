"""
    inbrowserhelp example: inbrowserhelp sample
"""
import webbrowser
import menuhook
from pymxs import runtime as rt
MAX_VERSION = rt.maxversion()[7]
MAX_HELP = f"help.autodesk.com/view/MAXDEV/{MAX_VERSION}/ENU"

TOPICS = [
    ("gettingstarted", 
     "Getting Started With Python in 3ds Max",
     f"{MAX_HELP}/?guid=Max_Python_API_tutorials_creating_the_dialog_html",
     "64651C48-F4F1-42F9-8C8A-FF5D0AA031A2"),
    ("howtos", 
     "Python HowTos Github Repo",
     "github.com/ADN-DevTech/3dsMax-Python-HowTos",
     "2504EEA5-27D6-4EA0-A7A3-B3C058777ADC"),
    ("samples", 
     "Python samples (Github Repo)",
     "github.com/ADN-DevTech/3dsMax-Python-HowTos/tree/master/src/samples",
     "8ED9D9CC-3799-435D-8016-0F8F16D84004"),
    ("pymxs", 
     "Pymxs Online Documentation",
     f"{MAX_HELP}/?guid=Max_Python_API_using_pymxs_html",
     "44985F87-C175-4F3D-B70F-9FA0B6242AE1"),
    ("pyside2", 
     "Qt for Python Documentation (PySide2)",
     "doc.qt.io/qtforpython/contents.html",
     "13EEE11E-1BBB-470E-B757-F536D91215A9"),
    ("python", 
     "Python 3.7 Documentation",
     "docs.python.org/3.7/",
     "B51BCC07-D9E3-439C-AC88-85BD64B97912")
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
            tooltip=topic[1],
            in2025_menuid=menuhook.BROWSE_DOCUMENTATION,
            id_2025=topic[3])
        
