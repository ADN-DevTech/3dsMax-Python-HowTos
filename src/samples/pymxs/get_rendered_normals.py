'''
An example of how to get the vertices and normals of a node
'''
from pymxs import runtime as rt # pylint: disable=import-error

def main():
    """Create a box and display its vertices and normals."""
    box = rt.box()
    print(f"node name: {box.name}")
    trimesh = rt.convertTo(box, rt.TrimeshGeometry)
    print(f" verts: {trimesh.numVerts}")
    for vert in range(trimesh.numVerts):
        normal = rt.getNormal(trimesh, vert + 1)
        vertex = rt.getVert(trimesh, vert + 1)
        print(f"vertex: {vertex}")
        print(f"RNormal: {normal}")
main()
