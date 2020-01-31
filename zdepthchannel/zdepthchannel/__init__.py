"""
    zdepthchannel example: Access the Z-Depth Channel
"""
import re
import menuhook
from pymxs import runtime as rt

def zdepthchannel():
    '''Access the Z-Depth Channel'''
    prev_renderer = rt.renderers.current
    rt.renderers.current = rt.Default_Scanline_Renderer()
    voxelbox = re.compile("^VoxelBox")
    for tbd in filter(lambda o: voxelbox.match(o.name), list(rt.objects)):
        rt.delete(tbd)

    zdepth_name = rt.Name("zdepth")
    rbmp = rt.render(outputsize=rt.Point2(32, 32), channels=[zdepth_name], vfb=False)
    z_d = rt.getChannelAsMask(rbmp, zdepth_name)
    rt.progressStart("Rendering Voxels...")
    for y in range(1, rbmp.height):
        print("y =", y)
        rt.progressupdate(100.0 * y / rbmp.height)
        pixel_line = rt.getPixels(rbmp, rt.Point2(0, y-1), rbmp.width)
        z_line = rt.getPixels(z_d, rt.Point2(0, y-1), rbmp.width)
        for x in range(1, rbmp.width):
            print("x =", x, z_line[x].value)
            box = rt.box(width=10, length=10, height=(z_line[x].value/2))
            box.pos = rt.Point3(x*10, -y*10, 0)
            box.wirecolor = pixel_line[x]
            box.name = rt.uniqueName("VoxelBox")
    rt.progressEnd()
    rt.renderers.current = prev_renderer

def startup():
    """
    Hook the function to a menu item.
    """
    menuhook.register(
        "zdepthchannel",
        "howtos",
        zdepthchannel,
        menu=["&Scripting", "Python3 Development", "How To"],
        text="Access the Z-Depth Channel",
        tooltip="Access the Z-Depth Channel")
