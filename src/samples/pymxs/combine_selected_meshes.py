'''
Demonstrates combining multipe scene nodes to an editable mesh.
'''
from pymxs import runtime as rt # pylint: disable=import-error

def combine_objects(*args):
    """
    Convert the two provided objects to meshes and merges them as a single mesh.
    """
    first = rt.convertToMesh(args[0])
    for obj in args[1:]:
        rt.attach(first, rt.convertToMesh(obj))

    return first

def combine_selected_objects():
    """
    Convert the selected objects into an editable mesh. The selections needs to contain
    at least 2 objects to combine.
    """
    if len(rt.selection) < 2:
        msg = "Please select at least 2 nodes to combine."
        print(msg)
        rt.messageBox(msg)
    else:
        # combine all the selected nodes into one editable mesh
        combine_objects(*rt.selection)

combine_selected_objects()
