"""
    mxstranslate example: Translation window for mxs code
"""
import menuhook
from pymxs import runtime as rt
from mxstranslate import translate

def mxstranslate():
    '''Translation window for mxs code'''
    # Create a console and float it
    translate.new_editor(floating=True)

def startup():
    """
    Hook the function to a menu item.
    """
    menuhook.register(
        "mxstranslate",
        "howtos",
        mxstranslate,
        menu=["&Scripting", "Python3 Development", "How To"],
        text="Translation window for mxs code",
        tooltip="Translation window for mxs code",
        in2025_menuid=menuhook.HOW_TO,
        id_2025="004BF4E1-4AB3-42B5-979A-28662B26533C")
