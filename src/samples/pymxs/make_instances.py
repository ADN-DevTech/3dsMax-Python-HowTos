'''
    Demonstrates creating instances of a node hierarchy.
'''
import pymxs # pylint: disable=import-error
from pymxs import runtime as rt # pylint: disable=import-error

INST = rt.Name("instance")

def create_instance_clones(obj, count, offset):
    """Create count clones of obj setting the parent of each clone to the
    previous clone."""
    for _ in range(count):
        # the maxscript CloneNodes method accepts a named argument called 'newNodes'
        # the argument must be sent by reference as it serves as an output argument
        # since the argument is not also an input argument, we can simply initialize
        # the byref() object as 'None'
        # the output argument along with the call result is then returned in a tuple
        # note: 'newNodes' returns an array of cloned nodes
        #       in the current case, only one element is cloned
        result, cloned = rt.MaxOps.CloneNodes(obj, cloneType=INST, offset=offset, newNodes=pymxs.byref(None))
        cloned[0].parent = obj
        obj = cloned[0]

def main():
    """Demonstrate cloning"""
    rt.resetMaxFile(rt.Name('noPrompt'))
    
    obj = rt.sphere(radius=3)
    create_instance_clones(obj, 10, rt.Point3(5, 0, 0))
    rt.MaxOps.CloneNodes(
        obj,
        cloneType=INST,
        offset=rt.Point3(0, 25, 0),
        expandHierarchy=True)

main()
