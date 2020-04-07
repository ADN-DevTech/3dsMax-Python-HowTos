'''
    Performs a hit test on an object in the active viewport.
'''
from pymxs import runtime as rt # pylint: disable=import-error

def main():
    """Demonstrate hit testing of rays with scene objects."""
    obj = rt.sphere(radius=50)
    point = rt.Point2(400, 200)
    hit_ray = rt.intersectRay(obj, rt.mapScreenToWorldRay(point))
    print(f"hit success {bool(hit_ray)} for point {point}")
    point = rt.Point2(0, 0)
    hit_ray = rt.intersectRay(obj, rt.mapScreenToWorldRay(point))
    print(f"hit success {bool(hit_ray)} for point {point}")

main()
