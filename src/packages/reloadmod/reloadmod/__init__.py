"""
    Add a menu item for reloading all development modules.
"""
import menuhook
from pymxs import runtime as rt
from reloadmod import reload

def python_reload():
    """
    Reload all development modules.
    """
    reload.reload_many(reload.dev_only())

def startup():
    """
    Hook the function to a menu item.
    """
    menuhook.register(
        "reloadmod",
        "python3devtools",
        python_reload,
        menu=["&Scripting", "Python3 Development"],
        text="Reload Python Modules",
        tooltip="Reload Python Modules",
        in2025_menuid=menuhook.PYTHON_DEVELOPMENT,
        id_2025="7A8CFC05-0752-4501-A5BD-F5AF020D7F5F")
