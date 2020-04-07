'''
   Demonstrates how to create a mesh from scratch and to set color per vertex data.
'''
from pymxs import runtime as rt # pylint: disable=import-error

def set_edge_visibility(mesh, face, aedge, bedge, cedge):
    """Set the visibility of face edges"""
    rt.setEdgeVis(mesh, face, 1, aedge)
    rt.setEdgeVis(mesh, face, 2, bedge)
    rt.setEdgeVis(mesh, face, 3, cedge)

def make_pyramid_mesh(side=20.0):
    """Create a pyramid from vertices and faces."""
    mesh = rt.mesh()
    mesh.numverts = 4
    mesh.numfaces = 4

    halfside = side / 2.0
    rt.SetVert(mesh, 1, rt.Point3(0.0, 0.0, side))
    rt.SetVert(mesh, 2, rt.Point3(-halfside, -halfside, 0.0))
    rt.SetVert(mesh, 3, rt.Point3(-halfside, halfside, 0.0))
    rt.SetVert(mesh, 4, rt.Point3(halfside, 0.0, 0.0))

    rt.setFace(mesh, 1, 1, 2, 3)
    set_edge_visibility(mesh, 1, True, True, False)

    rt.setFace(mesh, 2, 1, 3, 4)
    set_edge_visibility(mesh, 2, True, True, False)

    rt.setFace(mesh, 3, 1, 4, 2)
    set_edge_visibility(mesh, 2, True, True, False)

    rt.setFace(mesh, 4, 2, 3, 4)
    set_edge_visibility(mesh, 2, True, True, False)

    rt.update(mesh)
    return mesh

def output_channel(mesh, channel, name):
    """Retrieve and display the information about a given mesh map."""
    print("Channel: " + name)
    if not rt.meshop.getMapSupport(mesh, channel):
        print(" Not enabled")
        return

    vertices = rt.meshop.getNumMapVerts(mesh, channel)
    print(f" Number of texture vertices: {vertices}")
    for vindex in range(1, vertices + 1):
        vertex = rt.meshop.getMapVert(mesh, channel, vindex)
        print(f"  Texture vertex {vertex.X}, {vertex.Y}, {vertex.Z}")

    faces = rt.meshop.getNumMapFaces(mesh, channel)
    print(f" Number of faces: {faces}")
    for findex in range(1, faces + 1):
        face = rt.meshop.getMapFace(mesh, channel, findex)
        print(f"  Texture vertex indices {face.X}, {face.Y}, {face.Z}")
    print()

def output_channels(mesh):
    """Retrieve and display the information about all channels."""
    nummaps = rt.meshop.getNumMaps(mesh)
    print(f"NumMaps: {nummaps}")
    print()
    output_channel(mesh, 0, "color per vertex")
    output_channel(mesh, 1, "texture mapping")

def main():
    """Create a mesh, color it, and output information about its maps."""
    # reset the scene
    rt.resetMaxFile(rt.Name('noPrompt'))
    # create a mesh
    mesh = make_pyramid_mesh()
    print("Updating the color per vertex channel")
    rt.setNumCPVVerts(mesh, 2)
    rt.buildVCFaces(mesh)
    rt.setVertColor(mesh, 1, rt.Color(255, 0, 0))
    rt.setVertColor(mesh, 2, rt.Color(0, 0, 255))
    rt.setVCFace(mesh, 1, rt.Point3(1, 1, 2))
    rt.setVCFace(mesh, 2, rt.Point3(1, 2, 2))
    rt.setVCFace(mesh, 3, rt.Point3(2, 2, 2))
    rt.setVCFace(mesh, 4, rt.Point3(1, 1, 1))
    rt.setCVertMode(mesh, True)
    rt.update(mesh)
    output_channels(mesh)

main()
