'''
    Creates a number of boxes with random scale, position, and rotation.
'''
from random import random as rnd
import math
from pymxs import runtime as rt # pylint: disable=import-error

def rnd_angle():
    """Return a random angle in radians."""
    return -math.pi + (rnd() * 2 * math.pi)

def rnd_quat():
    """Return a random quaternion."""
    return rt.Quat(rnd(), rnd(), rnd(), rnd_angle())

def rnd_dist():
    """Return a random distance."""
    return rnd() * 100.0 - 50.0

def rnd_position():
    """Return a random position."""
    return rt.Point3(rnd_dist(), rnd_dist(), 0)

def rnd_scale_amount():
    """Return a random scaling amount."""
    return rnd() * 2.0 + 0.1

def rnd_scale():
    """Return a random (x,y,z) scaling as a Point3."""
    return rt.Point3(rnd_scale_amount(), rnd_scale_amount(), rnd_scale_amount())

def random_transform_nodes(nodes):
    """Apply a random transformation (scaling, rotation, position)
    to a list of nodes."""
    for node in nodes:
        node.Scaling = rnd_scale()
        node.Rotation = rnd_quat()
        node.Position = rnd_position()

def create_nodes(count):
    """Return count nodes."""
    def make_box():
        """Create a single node, a box of (10, 10, 10)."""
        box = rt.box()
        box.length = 10.0
        box.height = 10.0
        box.width = 10.0
        return box
    return [make_box() for i in range(count)]

def main():
    """Demonstrate the generation and transformation of 25 boxes."""
    nodes = create_nodes(25)
    random_transform_nodes(nodes)

main()
