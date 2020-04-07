"""
    transformlock example: lock all transforms on the selection.
"""
import menuhook
from pymxs import runtime as rt

def lock_selection():
    '''Lock all transforms on the selection'''
    rt.setTransformLockFlags(rt.selection, rt.Name("all"))

def startup():
    """
    Hook the transform lock function to a menu item.
    """
    menuhook.register(
        "transformlock",
        "howtos",
        lock_selection,
        menu=["&Scripting", "Python3 Development", "How To"],
        text="Lock transformations for the selection",
        tooltip="Lock transformations for the selection")
