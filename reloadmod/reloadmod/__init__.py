from pymxs import runtime as rt
from reloadmod import reload
def startup():
    """
        Give the developers a way to reload all their dev modules in
        one shot.
    """
    menu="&Scripting"
    category= "PythonDev"
    action = "python_reloadmod"
    tooltip = "Reload Python Modules"
    button_text = "Reload"
    rt.macros.new(category, action, tooltip, button_text, "( macro_python_reloadmod() )")
    rt.macro_python_reloadmod = python_reload
    hook_menu_item(menu, category, action)

def hook_menu_item(menu, category, action):
    """This will create a menu item if noone is already there. This really
    clashes with the idea of creating the ui during the startup,
    but the register MenuContext thing is a workaround"""
    if rt.menuman.registerMenuContext(2546011):
        targetmenu = rt.menuman.findMenu(menu)
        if targetmenu:
            newaction = rt.menuman.createActionItem(action, category)
            if newaction:
                targetmenu.addItem(newaction, -1)
                rt.menuman.updateMenuBar()

def python_reload():
    reload.reload_many(reload.DEV_ONLY)
