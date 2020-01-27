import menuhook
from pymxs import runtime as rt
from reloadmod import reload

def python_reload():
    reload.reload_many(reload.DEV_ONLY)

def startup():
    """
    Hook the funtion to a menu item.
    """
    menuhook.register(
        "Reload Python Modules",
        "python3devtools",
        python_reload,
        menu=[ "&Scripting", "Python3 Development"],
        text="Reload Python Modules",
        tooltip="Reload Python Modules")
