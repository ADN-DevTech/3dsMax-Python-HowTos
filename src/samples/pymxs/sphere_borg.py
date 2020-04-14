'''
    Demonstrates creating objects, object instancing, and object translation.
'''
from pymxs import runtime as rt # pylint: disable=import-error

INST = rt.Name("instance")

def create_borg(obj, num, spacing):
    """Create a bunch of clones of the provided object"""
    for i in range(num):
        for j in range(num):
            for k in range(num):
                if i or j or k:
                    point = rt.Point3(i * spacing, j * spacing, k * spacing)
                    rt.MaxOps.CloneNodes(obj, cloneType=INST, offset=point)

def main():
    """Create a base object and turn it into a borg, whatever that is."""
    obj = rt.sphere()
    obj.Radius = 2.0
    create_borg(obj, 4, 5.0)

main()
