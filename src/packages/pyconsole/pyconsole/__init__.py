"""
    pyconsole example: pyconsole sample
"""
import menuhook
from pyconsole import console

def pyconsole():
    '''pyconsole sample'''
    console.new_console()

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
