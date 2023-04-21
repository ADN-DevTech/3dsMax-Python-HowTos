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
        tooltip="Translation window for mxs code")
