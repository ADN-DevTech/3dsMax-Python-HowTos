"""
    removeallmaterials example: remove all materials from the scene
"""
import menuhook
from pymxs import runtime as rt

def remove_all_materials():
    '''Remove all materials from the scene'''
    for obj in rt.objects:
        obj.material = None

def startup():
    """
    Hook the function to a menu item.
    """
    menuhook.register(
        "removeallmaterials",
        "howtos",
        remove_all_materials,
        menu=["&Scripting", "Python3 Development", "How To"],
        text="Remove all materials from the scene",
        tooltip="Remove all materials from the scene",
        in2025_menuid=menuhook.HOW_TO,
        id_2025="1A3AE016-3E54-4856-9076-2BE491B2258C")
