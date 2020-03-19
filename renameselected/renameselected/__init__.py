"""
    renameselected example
"""
import menuhook
from pymxs import runtime as rt
from renameselected import ui

def renameselected(text):
    '''Rename all elements in selection'''
    if text != "":
        for i in rt.selection:
            i.name = rt.uniquename(text)

def showdialog():
    """
    Show the rename dialog.
    """
    dialog = ui.PyMaxDialog(renameselected)
    dialog.show()

def startup():
    """
    Hook the function to a menu item.
    """
    menuhook.register(
        "renameselected",
        "howtos",
        showdialog,
        menu=["&Scripting", "Python3 Development", "How To"],
        text="Rename all elements in selection",
        tooltip="renameselected sample")
