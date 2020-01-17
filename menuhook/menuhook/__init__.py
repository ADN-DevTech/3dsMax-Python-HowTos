"""
    Utility for registering python actions in 3ds Max menus, in a way
    that is relatively harmonious with the menu manager.
"""
import sys
import re
from pymxs import runtime as rt

REMACRO = re.compile('^[0-9]+ +"([^"]*)" +"([^"]*)"', re.M)
macros = {}

def eprint(*args):
    """
    Print and error.
    """
    print(*args, file=sys.stderr)

def macro_defined(action, category):
    """
    Search in max by a very tortuous method if a given macro
    exists already.
    """
    mss = rt.stringStream("")
    rt.macros.list(to=mss)
    key = get_action_key(action, category)

    try:
        if next(filter(
                lambda actcat: actcat[0] == action and actcat[1] == category,
                REMACRO.findall(str(mss)))) == key:
            return True
    except StopIteration:
        pass
    return False

def get_action_key(action, category):
    """
    Return a key for indexing an action.
    """
    return (action, category)

def execute_macro(action, category):
    """
    Execute a macro by action category.
    """
    key = get_action_key(action, category)
    if key in macros:
        macros[key]()
    else:
        eprint(
            "The macro {} {} is not available.".format(
                action,
                category))

def add_macro(action, category, text, tooltip, fcn):
    """
    Add a macro.
    """
    key = get_action_key(action, category)
    macros[key] = fcn
    # note: it is harmless to do this if it's already defined:
    mxs = "( python.execute \"import menuhook\\nmenuhook.execute_macro(\\\"{}\\\", \\\"{}\\\")\")"
    rt.macros.new(
        category,
        action,
        tooltip,
        text,
        mxs.format(action, category))

def add_menu_item(menu, action, category):
    """
    Add a menu item for an action.
    The menu item will be re added even if it is already there.
    """
    targetmenu = rt.menuman.findmenu(menu)
    if targetmenu:
        newaction = rt.menuman.createActionItem(action, category)
        if newaction:
            targetmenu.addItem(newaction, -1)
            rt.menuman.updateMenuBar()

def register(action, category, fcn, menu=None, text=None, tooltip=None):
    """
    Appends a menu item to one of the menus of the main menubar.
    If the action already exists, the menu is not added but the
    action is made available for this run of max.

    This is an integrated way of:
        - creating a macro
        - assign the macro function if the macro is already there
        - create a menu item for the macro if it is not already there
    """
    defined = macro_defined(action, category)
    add_macro(action, category, text or action, tooltip or action, fcn)
    if not defined and not menu is None:
        add_menu_item(menu, action, category)
