'''
    Applies a standard material to all nodes in the scene.
    Also shows the use of generator functions in Python.
'''
from pymxs import runtime as rt # pylint: disable=import-error

def create_sphere():
    """Create a sphere of radius 5."""
    return rt.sphere(radius=5)

def solid_material(color):
    """Create a material."""
    material = rt.StandardMaterial()
    material.Ambient = color
    material.Diffuse = color
    material.Specular = rt.Color(255, 255, 255)
    material.Shininess = 50.0
    material.ShinyStrength = 70.0
    material.SpecularLevel = 70.0
    return material

def apply_material_to_nodes(material, nodes=rt.rootnode.children):
    """Apply a material to multiple nodes."""
    for node in nodes:
        node.Material = material

create_sphere()
MAT = solid_material(rt.Color(0, 0, 255))
apply_material_to_nodes(MAT)
