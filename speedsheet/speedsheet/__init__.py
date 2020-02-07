"""
    speedsheet example: Output Object Data to File
"""
import menuhook
import pymxs
from pymxs import runtime as rt

def speedsheet():
    '''Output Object Data To File'''
    output_name = rt.getSaveFileName(
        caption="SpeedSheet File",
        types="SpeedSheet (*.ssh)|*.ssh|All Files (*.*)|*.*|")
    if output_name is not None:
        with open(output_name, "w+") as output_file:
            with pymxs.attime(rt.animationRange.start):
                objdump = ", ".join(map(lambda x: x.name, list(rt.selection)))
                output_file.write(
                    f"Object(s): {objdump}\n")
            average_speed = 0
            for t in range(int(rt.animationRange.start), int(rt.animationRange.end)):
                with pymxs.attime(t):
                    current_pos = rt.selection.center
                with pymxs.attime(t-1):
                    last_pos = rt.selection.center
                frame_speed = rt.distance(current_pos, last_pos) * rt.FrameRate
                average_speed += frame_speed
                output_file.write(f"Frame {t}: {frame_speed}\n")
            average_speed /= float(rt.animationRange.end - rt.animationRange.start)
            output_file.write(f"Average Speed: {average_speed}\n")
        rt.edit(output_name)

def startup():
    """
    Hook the function to a menu item.
    """
    menuhook.register(
        "speedsheet",
        "howtos",
        speedsheet,
        menu=["&Scripting", "Python3 Development", "How To"],
        text="Output Object Data to File",
        tooltip="Output Object Data to File")
