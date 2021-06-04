"""
    pyconsole example: pyconsole sample
"""
import menuhook
from pyconsole import console

def pyconsole():
    '''pyconsole sample'''
    # Create a console and float it
    console.new_console(floating=True)

def startup():
    """
    Hook the function to a menu item.
    """
    menuhook.register(
        "pyconsole",
        "howtos",
        pyconsole,
        menu=["&Scripting", "Python3 Development", "How To"],
        text="Python Console",
        tooltip="Python Console")
    # Create a python console in the command panel
    # automatically
    console.new_console(tabto="CommandPanel")
