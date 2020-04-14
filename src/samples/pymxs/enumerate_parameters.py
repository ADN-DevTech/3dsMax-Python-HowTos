'''
    Creates all geometric objects and lists their parameters.
'''
from pymxs import runtime as rt # pylint: disable=import-error

for cl in rt.GeometryClass.classes:
    try:
        obj = cl()
        print(f"Properties for class {cl}")
        # This would also work:
        # rt.showProperties(o)
        for pn in rt.getPropNames(obj):
            print(f"  {pn} {rt.getProperty(obj, pn)}")
    except RuntimeError:
        # Some geometry classes cannot be instantiated
        pass
