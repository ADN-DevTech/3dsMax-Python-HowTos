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
        tooltip="Lock transformations for the selection",
        in2025_menuid=menuhook.HOW_TO,
        id_2025="F9DA574D-185B-4C00-9C37-795B38719E78")
