'''
    Demonstrates how to iterate through materials and and apply them to objects.
    It shows how to open the material editor and put materials in the editor.
'''
from pymxs import runtime as rt # pylint: disable=import-error

def create_floor():
    """Create a rectangle for the floor"""
    plane = rt.Plane()
    plane.width = 120
    plane.length = 120

def print_material_properties(material_instance):
    """Print the properties of a given material"""
    print("[%s]" % material_instance.name)
    for name in rt.getPropNames(material_instance):
        print("\t" + name + " = " + str(rt.getProperty(material_instance, name)))

def create_text(xpos, ypos, rot, message):
    """Create a visible label on the ground for a given teapot"""
    tex = rt.text()
    tex.size = 10
    tex.text = message
    tex.position = rt.Point3(xpos, ypos, 0)
    tex.rotation = rot
    tex.wireColor = rt.Color(255, 128, 255)

def showcase_materials(materials):
    """Create a teapot sample and a visible label for each provided material"""
    num_materials = len(materials)
    diff = 360.0 / num_materials
    teapot_radius = 5.0
    radius = 50.0
    text_radius = 90.0
    index = 0
    i = 0

    for mat in materials:
        position = rt.Point3(radius, 0, 0)
        rot = rt.angleAxis(i, rt.Point3(0, 0, 1))

        teapot = rt.teapot()
        teapot.radius = teapot_radius
        teapot.position = position
        teapot.rotation = rot
        teapot.Material = mat
        print_material_properties(mat)

        create_text(text_radius, 0, rot, mat.name)
        if index < 24:
            rt.setMeditMaterial(index + 1, mat)
            index += 1
        i += diff

def sample():
    """Create all existing materials and showcase them."""
    def try_create(mat):
        """Try to create a given material. If not creatable return None."""
        try:
            return mat()
        except RuntimeError:
            return None
    rt.resetMaxFile(rt.Name('noPrompt'))
    # maximize the view (select a view with only the one viewport)
    rt.viewport.setLayout(rt.name("layout_1"))
    # show the material editor in basic mode
    rt.MatEditor.mode = rt.Name("basic")
    rt.MatEditor.open()
    # create a plane for the floor
    create_floor()
    # instantiate all materials that can be instantiated
    materials = filter(lambda x: x is not None, map(try_create, rt.material.classes))
    # showcase all materials
    showcase_materials(list(materials))

sample()
