"""
    threadprogressbar example: Update a progress bar from a thread
"""
import menuhook
from pymxs import runtime as rt
from threadprogressbar import ui

def threadprogressbar():
    '''Update a progress bar from a thread'''
    dialog = ui.PyMaxDialog()
    dialog.show()

def startup():
    """
    Hook the function to a menu item.
    """
    menuhook.register(
        "threadprogressbar",
        "howtos",
        threadprogressbar,
        menu=["&Scripting", "Python3 Development", "Other Samples"],
        text="Update a progress bar from a thread",
        tooltip="Update a progress bar from a thread",
        in2025_menuid=menuhook.OTHER_SAMPLES,
        id_2025="AB072ECE-8665-4EC4-8D12-C0E76DA4C919")
