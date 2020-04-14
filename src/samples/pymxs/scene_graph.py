'''
    Creates a simple text representation of the scene graph
'''
from pymxs import runtime as rt # pylint: disable=import-error

def output_node(node, indent=''):
    """Print the scene graph as text to stdout."""
    print(indent, node.Name)
    for child in node.Children:
        output_node(child, indent + '--')

output_node(rt.rootnode)
