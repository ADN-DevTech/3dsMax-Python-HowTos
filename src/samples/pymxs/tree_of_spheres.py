'''
    Creates a hierarchy of sphere objects at different relative locations.
'''
from pymxs import runtime as rt # pylint: disable=import-error

def create_sphere():
    """Create and return a single sphere of radius 5."""
    sphere = rt.sphere()
    sphere.radius = 5
    return sphere

def tree_of_spheres(parent, width, xinc, depth, maxdepth):
    """Create a tree of spheres."""
    if depth == maxdepth:
        return
    for i in range(width):
        sphere = create_sphere()
        pos = parent.pos
        sphere.pos = rt.Point3(pos.x + i * xinc, 0, pos.z + 15)
        sphere.Parent = parent
        tree_of_spheres(sphere, width, xinc * width, depth + 1, maxdepth)

tree_of_spheres(create_sphere(), 2, 10, 0, 4)
