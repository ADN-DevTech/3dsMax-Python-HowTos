"""
    singleinstancedlg example: Single instance modeless dialog
"""
import menuhook
from pymxs import runtime as rt
from singleinstancedlg import ui

def singleinstancedlg():
    '''Show a dialog if not already there'''
    ui.show_dialog()

def startup():
    """
    Hook the function to a menu item.
    """
    menuhook.register(
        "singleinstancedlg",
        "howtos",
        singleinstancedlg,
        menu=["&Scripting", "Python3 Development", "Other Samples"],
        text="Single instance modeless dialog",
        tooltip="Single instance modeless dialog",
        in2025_menuid=menuhook.OTHER_SAMPLES,
        id_2025="AF515BBA-E826-4DA8-B097-FA9A2C917A91")
