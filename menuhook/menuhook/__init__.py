"""
    Utility for registering Python actions in 3ds Max menus, in a way
    that is relatively harmonious with the menu manager.
"""
import sys
import re
from pymxs import runtime as rt

REMACRO = re.compile('^[0-9]+ +"([^"]*)" +"([^"]*)"', re.M)

def function_without_docstring():
    pass

# this is to avoid macros to be ditched while reloading
# with reloadmod
#pylint: disable=E0602
if not hasattr(sys.modules[__name__], 'macros'):
    sys.modules[__name__].macros = {}

def eprint(*args):
    """
    Print and error.
    """
    print(*args, file=sys.stderr)

def macro_defined(action, category):
    """
    Search in 3ds Max by a very tortuous method if a given macro
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
        eprint(f"The macro {action} {category} is not available.")

def add_macro(action, category, text, tooltip, fcn):
    """
    Add a macro.
    """
    key = get_action_key(action, category)
    macros[key] = fcn
    # note: it is harmless to do this if it's already defined:
    #pylint: disable=line-too-long
    mxs = f"( python.execute \"import menuhook\\nmenuhook.execute_macro(\\\"{action}\\\", \\\"{category}\\\")\")"
    #pylint: enable=line-too-long
    rt.macros.new(
        category,
        action,
        tooltip,
        text,
        mxs)

def deep_menu(menu):
    """
        Finds or create a deep menu where to put our item.
        like deep_menu(["&Scripting", "Python Developer", "HowTos"]) would make sure
        there is a "Python Developer -> HowTos" sub menu item under scripting
    """
    found = rt.menuman.findMenu(menu[-1])
    name = menu[-1]
    if found is not None:
        return found
    if len(menu) == 1:
        inmenu = rt.menuman.getMainMenuBar()
    else:
        inmenu = deep_menu(menu[0:-1])
    submenu = rt.menuman.createMenu(name)
    submenuitem = rt.menuman.createSubMenuItem(name, submenu)
    index = inmenu.numItems() - 1
    inmenu.addItem(submenuitem, index)
    return submenu

def add_menu_item(menu, action, category):
    """
    Add a menu item for an action.
    The menu item will be re added even if it is already there.
    """
    if not isinstance(menu, list):
        menu = [menu]
    targetmenu = deep_menu(menu)
    if targetmenu:
        newaction = rt.menuman.createActionItem(action, category)
        if newaction:
            targetmenu.addItem(newaction, -1)
            rt.menuman.updateMenuBar()

#pylint: disable=too-many-arguments
def register(action, category, fcn, menu=None, text=None, tooltip=None):
    """
    Appends a menu item to one of the menus of the main menubar.
    If the action already exists, the menu is not added but the
    action is made available for this run of 3ds Max.

    This is an integrated way of:
        - creating a macro
        - assign the macro function if the macro is already there
        - create a menu item for the macro if it is not already there
    """
    defined = macro_defined(action, category)
    add_macro(action, category, text or action, tooltip or action, fcn)
    if not defined and not menu is None:
        add_menu_item(menu, action, category)
#pylint: enable=too-many-arguments
