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
    Hook the funtion to a menu item.
    """
    menuhook.register(
        "threadprogressbar",
        "howtos",
        threadprogressbar,
        menu=["&Scripting", "Python3 Development", "Other Samples"],
        text="Update a progress bar from a thread",
        tooltip="Update a progress bar from a thread")
