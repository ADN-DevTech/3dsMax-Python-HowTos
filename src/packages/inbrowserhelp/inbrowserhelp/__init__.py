"""
    inbrowserhelp example: inbrowserhelp sample
"""
import webbrowser
import menuhook
from sys import version_info
from pymxs import runtime as rt
MAX_VERSION = rt.maxversion()[7]
MAX_HELP = f"help.autodesk.com/view/MAXDEV/{MAX_VERSION}/ENU"

PYTHON_VERSION = f"{version_info[0]}.{version_info[1]}"

MAX_VERSION_TOPICS = {
    2021: [
        ("gettingstarted", 
         "Getting Started With Python in 3ds Max",
         "help.autodesk.com/view/MAXDEV/2021/ENU/?guid=Max_Python_API_about_the_3ds_max_python_api_html",
         "64651C48-F4F1-42F9-8C8A-FF5D0AA031A2"),
        ("pymxs", 
         "Pymxs Online Documentation",
         "help.autodesk.com/view/MAXDEV/2021/ENU/?guid=Max_Python_API_using_pymxs_pymxs_module_html",
         "44985F87-C175-4F3D-B70F-9FA0B6242AE1")
        ],
    2022: [
        ("gettingstarted", 
         "Getting Started With Python in 3ds Max",
         "help.autodesk.com/view/MAXDEV/2022/ENU/?guid=MAXDEV_Python_about_the_3ds_max_python_api_html",
         "64651C48-F4F1-42F9-8C8A-FF5D0AA031A2"),
        ("pymxs", 
         "Pymxs Online Documentation",
         "help.autodesk.com/view/MAXDEV/2022/ENU/?guid=MAXDEV_Python_using_pymxs_html",
         "44985F87-C175-4F3D-B70F-9FA0B6242AE1")
        ],
    2023: [
        ("gettingstarted", 
         "Getting Started With Python in 3ds Max",
         "help.autodesk.com/view/MAXDEV/2023/ENU/?guid=MAXDEV_Python_about_the_3ds_max_python_api_html",
         "64651C48-F4F1-42F9-8C8A-FF5D0AA031A2"),
        ("pymxs", 
         "Pymxs Online Documentation",
         "help.autodesk.com/view/MAXDEV/2023/ENU/?guid=MAXDEV_Python_using_pymxs_html",
         "44985F87-C175-4F3D-B70F-9FA0B6242AE1")
        ],
    2024: [
        ("gettingstarted", 
         "Getting Started With Python in 3ds Max",
         "help.autodesk.com/view/MAXDEV/2024/ENU/?guid=MAXDEV_Python_about_the_3ds_max_python_api_html",
         "64651C48-F4F1-42F9-8C8A-FF5D0AA031A2"),
        ("pymxs", 
         "Pymxs Online Documentation",
         "help.autodesk.com/view/MAXDEV/2024/ENU/?guid=MAXDEV_Python_using_pymxs_html",
         "44985F87-C175-4F3D-B70F-9FA0B6242AE1")
        ]
    }

def get_version_topics(version):
    """Get the version-dependent topics, defaulting on the latest
    if the requested one does not exist"""
    return MAX_VERSION_TOPICS[version if version in MAX_VERSION_TOPICS else 2024]

V_TOPICS = get_version_topics(MAX_VERSION)

PYSIDE6_DOC = ("pyside6", 
     "Qt for Python Documentation (PySide6)",
     "doc.qt.io/qtforpython-6/index.html",
     "E0E5F945-CD55-404A-840B-81540829E4C4")

PYSIDE2_DOC = ("pyside2", 
     "Qt for Python Documentation (PySide2)",
     "doc.qt.io/qtforpython-5/contents.html",
     "13EEE11E-1BBB-470E-B757-F536D91215A9")

TOPICS = V_TOPICS + [
    ("howtos", 
     "Python HowTos Github Repo",
     "github.com/ADN-DevTech/3dsMax-Python-HowTos",
     "2504EEA5-27D6-4EA0-A7A3-B3C058777ADC"),
    ("samples", 
     "Python samples (Github Repo)",
     "github.com/ADN-DevTech/3dsMax-Python-HowTos/tree/master/src/samples",
     "8ED9D9CC-3799-435D-8016-0F8F16D84004"),
    PYSIDE6_DOC if MAX_VERSION >= 2025 else PYSIDE2_DOC,
    ("python", 
     f"Python {PYTHON_VERSION} Documentation",
     f"docs.python.org/{PYTHON_VERSION}/",
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
        
