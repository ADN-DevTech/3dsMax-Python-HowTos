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
        tooltip="Python Console",
        in2025_menuid=menuhook.HOW_TO,
        id_2025="0F52AF28-D7EE-4A04-AC9D-56C126FE9373")
    # Create a python console in the command panel
    # automatically
    console.new_console(tabto="CommandPanel")
