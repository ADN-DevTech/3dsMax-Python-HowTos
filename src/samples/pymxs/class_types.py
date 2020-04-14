'''
    Demonstrates creating many different types of scene objects that are visible in the viewport.
    The scene objects are grouped by type.
    The types created are Cameras, Lights, Geometric Objects, Shapes, Helpers, Modifiers
    and Materials.
'''
from pymxs import runtime as rt # pylint: disable=import-error
OBJECT_DIMENSION = 5.0
Y_STEP = OBJECT_DIMENSION * 4
X_STEP = OBJECT_DIMENSION * 2.0

def create_box():
    """Create a box."""
    box = rt.box()
    box.Height = OBJECT_DIMENSION
    box.Width = OBJECT_DIMENSION
    box.Length = OBJECT_DIMENSION
    return box

def create_text(pos, message):
    """Create a text."""
    tex = rt.text()
    tex.size = Y_STEP
    tex.text = message
    tex.position = rt.Point3(pos.x, pos.y - OBJECT_DIMENSION, pos.z)
    tex.wirecolor = rt.Color(255, 128, 255)

def create_teapot():
    """Create a teapot."""
    teapot = rt.teapot()
    teapot.radius = OBJECT_DIMENSION
    return teapot

def layout_objects(title, cases, y_position, x_offset_text=-45):
    """Layout a list of nodes in a line"""
    create_text(rt.Point3(x_offset_text, y_position, 0), title)
    x_position = 0.0
    for gen in cases:
        gen.Position = rt.point3(x_position, y_position, 0)
        x_position += X_STEP
        if (x_position % 260.0) < 0.001:
            x_position = 0.0
            y_position += Y_STEP
    return y_position

def create_classes(classes):
    """Create all createble instances of the provided classes"""
    for obj in classes:
        try:
            created = obj()
            print(created)
            yield created
        except RuntimeError:
            pass

def create_cameras(y_position):
    """Create all creatable cameras"""
    print("-- Cameras")
    return layout_objects("Cameras", create_classes(rt.camera.classes), y_position)

def create_lights(y_position):
    """Create all creatable lights"""
    print("-- Lights")
    return layout_objects("Lights", create_classes(rt.light.classes), y_position)

def create_objects(y_position):
    """Create all creatable objects"""
    print("-- Geometric Objects")
    return layout_objects(
        "Geometric Objects",
        create_classes(rt.GeometryClass.classes),
        y_position, -88.0)

def create_shapes(y_position):
    """Create all creatable shapes"""
    print("-- Shapes")
    return layout_objects("Shapes", create_classes(rt.shape.classes), y_position)

def create_helpers(y_position):
    """Create all creatable helpers"""
    print("-- Helpers")
    return layout_objects("Helpers", create_classes(rt.helper.classes), y_position)

def create_modifiers(y_position):
    """Create all creatable modifiers"""
    def create():
        for mod in rt.modifier.classes:
            try:
                created = mod()
                print(created)
                box = create_box()
                rt.addModifier(box, created)
                yield box
            except RuntimeError:
                pass
    print("-- Modifiers")
    return layout_objects("Modifiers", create(), y_position)

def create_materials(y_position):
    """Create all creatable materials"""
    def create():
        for mat in rt.material.classes:
            try:
                created = mat()
                print(mat)
                teapot = create_teapot()
                teapot.Material = created
                yield teapot
            except RuntimeError:
                pass
    print("-- Materials")
    return layout_objects("Materials", create(), y_position)

def create_items():
    """Create all the items in the sample."""
    rt.resetMaxFile(rt.Name('noPrompt'))
    y_line = create_materials(0.0) + 40.0
    y_line = create_modifiers(y_line) + 40.0
    y_line = create_helpers(y_line) + 40.0
    y_line = create_shapes(y_line) + 40.0
    y_line = create_objects(y_line) + 40.0
    y_line = create_lights(y_line) + 40.0
    y_line = create_cameras(y_line) + 40.0

create_items()
