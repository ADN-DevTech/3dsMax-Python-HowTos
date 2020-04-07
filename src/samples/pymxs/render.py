"""
    Demonstrate scene rendering with pymxs.
"""
import os
import math
import pymxs # pylint: disable=import-error
from pymxs import runtime as rt # pylint: disable=import-error

INST = rt.Name("instance")

def create_spheres():
    '''Create a scene made of spiralling spheres.'''
    sphere = rt.sphere(radius=6.0)
    revolutions = 9 * 360
    radius = 40.0
    z_sphere = 0.0
    # cloning the original sphere to create the spiral effect
    for i in range(0, revolutions, 20):
        # the maxscript CloneNodes method accepts a named argument called 'newNodes'
        # the argument must be sent by reference as it serves as an output argument
        # since the argument is not also an input argument, we can simply initialize
        # the byref() object as 'None'
        # the output argument along with the call result is then returned in a tuple
        # note: 'newNodes' returns an array of cloned nodes
        #       in the current case, only one element is cloned
        result, nodes = rt.MaxOps.CloneNodes(sphere, cloneType=INST, newNodes=pymxs.byref(None))
        radians = math.radians(i)
        x_sphere = radius * math.cos(radians)
        y_sphere = radius * math.sin(radians)
        # note: 'newNodes' returned an array of cloned nodes
        #       in the current case, only one element is cloned
        nodes[0].Position = rt.Point3(x_sphere, y_sphere, z_sphere)
        z_sphere += 1.0
        radius -= 0.20

def maximize_perspective():
    '''Setup perspective for the render'''
    rt.viewport.setLayout(rt.Name('layout_1'))
    rt.viewport.setType(rt.Name('view_persp_user'))
    rt.viewport.setTM(
        rt.matrix3(
            rt.point3(0.707107, 0.353553, -0.612372),
            rt.point3(-0.707107, 0.353553, -0.612372),
            rt.point3(0, 0.866025, 0.5),
            rt.point3(-0.00967026,-70.3466,-552.481)
            )
        )

def render():
    '''Render in the renderoutput directory.'''
    output_path = os.path.join(rt.getDir(rt.Name("renderoutput")), 'foo.jpg')
    if os.path.exists(output_path):
        os.remove(output_path)
    rt.render(outputFile=output_path)

def demo_render():
    '''Create a demo scene, adjust the perspective and render the scene'''
    rt.resetMaxFile(rt.Name('noPrompt'))
    create_spheres()
    maximize_perspective()
    render()

demo_render()
