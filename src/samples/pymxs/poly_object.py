'''
   Demonstrates how to create a mmesh from scratch and to set color per vertex data.
'''
from pymxs import runtime as rt # pylint: disable=import-error

def make_pyramid_mesh(side=20.0):
    '''Construct a pyramid from vertices and faces.'''
    halfside = side / 2.0
    return rt.mesh(
        vertices=[
            rt.point3(0.0, 0.0, side),
            rt.point3(-halfside, -halfside, 0.0),
            rt.point3(-halfside, halfside, 0.0),
            rt.point3(halfside, 0.0, 0.0)
            ],
        faces=[
            rt.point3(1, 2, 3),
            rt.point3(1, 3, 4),
            rt.point3(1, 4, 2),
            rt.point3(2, 3, 4),
        ])

def color_pyramid_mesh(mesh):
    '''Add two color vertices, and refer them in the faces (color the pyramid).'''
    rt.setNumCPVVerts(mesh, 2, True)
    rt.setVertColor(mesh, 1, rt.Point3(255, 0, 0))
    rt.setVertColor(mesh, 2, rt.Point3(0, 0, 255))
    rt.buildVCFaces(mesh)
    rt.setVCFace(mesh, 1, 1, 1, 2)
    rt.setVCFace(mesh, 2, 1, 2, 2)
    rt.setVCFace(mesh, 3, 2, 2, 2)
    rt.setVCFace(mesh, 4, 1, 1, 1)
    rt.setCVertMode(mesh, True)
    rt.update(mesh)

def main():
    '''Construct a pyramid and then add colors to its faces.'''
    rt.resetMaxFile(rt.Name('noPrompt'))
    mesh = make_pyramid_mesh()
    color_pyramid_mesh(mesh)

main()
