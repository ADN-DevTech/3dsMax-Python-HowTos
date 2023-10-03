"""
    quickpreview example: Create a quick preview
"""
from os import path
import menuhook
from pymxs import runtime as rt

def quickpreview():
    '''Create a quick preview'''
    preview_name = path.join(rt.getDir(rt.Name("preview")), "quickpreview.avi")
    view_size = rt.getViewSize()
    anim_bmp = rt.bitmap(view_size.x, view_size.y, filename=preview_name)
    for t in range(int(rt.animationRange.start), int(rt.animationRange.end)):
        rt.sliderTime = t
        dib = rt.gw.getViewportDib()
        rt.copy(dib, anim_bmp)
        rt.save(anim_bmp)
    rt.close(anim_bmp)
    rt.gc()
    rt.ramplayer(preview_name, "")

def startup():
    """
    Hook the function to a menu item.
    """
    menuhook.register(
        "quickpreview",
        "howtos",
        quickpreview,
        menu=["&Scripting", "Python3 Development", "How To"],
        text="Create a quick preview",
        tooltip="Create a quick preview",
        in2025_menuid=menuhook.HOW_TO,
        id_2025="E30C825C-E4CD-48FD-A1C7-A75A91B2E9C2")
