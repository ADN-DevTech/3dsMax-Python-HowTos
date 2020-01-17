"""
    renameselected example
"""
import menuhook
from pymxs import runtime as rt
from renameselected import ui as ui

def renameselected(text):
    '''Rename all elements in selection'''
    if text != "":
        for i in rt.selection:
            i.name = rt.uniquename(text)

def showdialog():
    dialog = ui.PyMaxDialog(renameselected)
    dialog.show()

def startup():
    """
    Hook the funtion to a menu item.
    """
    menuhook.register(
        "howtos",
        "renameselected",
        showdialog,
        menu="&Scripting",
        text="renameselected sample",
        tooltip="renameselected sample")
