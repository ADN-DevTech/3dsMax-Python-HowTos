'''
    Demonstrates how to manage user specified data for any object derived from Animatable.
'''
from pymxs import runtime as rt # pylint: disable=import-error

def create_scene():
    """Create and save scene_with_app_chunk.max"""
    rt.resetMaxFile(rt.Name('noPrompt'))

    # Create a teapot, a scene node and a material instance, they are all
    # objects of Animatable
    node = rt.teapot()
    teapot = node.baseObject
    mtl = rt.StandardMaterial()
    node.Material = mtl
    node.name = "MyTeapot123"

    # Now add some user specified strings to these objects
    rt.setAppdata(teapot, 112, "blah comit")
    rt.setAppdata(teapot, 1234, "I'm a teapot!")
    rt.setAppdata(teapot, 2345, u"我是一个茶壶！")

    rt.setAppdata(node, 5678, "Node of teapot")
    rt.setAppdata(node, 7890, "This is to be removed")
    rt.deleteAppdata(node, 7890)

    rt.setAppdata(mtl, 4567, "Material of teapot")
    rt.saveMaxFile("scene_with_app_chunk.max")
    print("scene with AppChunk is saved.")


def load_and_verify():
    """Load and verify scene_with_app_chunk.max"""
    rt.resetMaxFile(rt.Name('noPrompt'))
    rt.loadMaxFile("scene_with_app_chunk.max")
    print("scene with AppChunk is loaded.")
    # Find the "MyTeapot123" node
    teapot_node = rt.getNodeByName("MyTeapot123")

    if teapot_node is None:
        print("Error: Incorrect saved scene.")
    else:
        print(rt.getAppData(teapot_node, 678))
        obj = teapot_node.baseObject
        print(rt.getAppData(obj, 1234))
        print(rt.getAppData(obj, 2345))
        rt.clearAllAppData(obj)
        print("No 9432 app data {}".format(rt.getAppData(obj, 9432) is None))
        print("No 7890 app data {}".format(rt.getAppData(teapot_node, 9432) is None))
        print(rt.getAppData(teapot_node.Material, 4567))

create_scene()
load_and_verify()
