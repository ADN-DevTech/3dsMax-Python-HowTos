'''
    Demonstrates creating a cylinder and appling a bend modifier.
'''
from pymxs import runtime as rt # pylint: disable=import-error

def main():
    """Create a cylinder and add a bend modifier to it."""
    cyl = rt.cylinder()
    cyl.radius = 10
    cyl.height = 30
    bend = rt.Bend()
    bend.bendAngle = 45
    rt.addModifier(cyl, bend)

main()
