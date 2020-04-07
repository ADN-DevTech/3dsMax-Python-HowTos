'''
    Demonstrates using the inspect module to list all of the classes in
    pymxs and the total number of members exposed.

    (Note that there is no 1:1 relationship between the classes in
    maxscript and the python classes exposed in pymxs: a single pymxs
    wrapper exposes almost all maxscript classes. You can use 
    pymxs.runtime.apropos(), showClass(), and other MAXScript inspection 
    methods to get information about MAXScript objects and classes)
'''
import os
import inspect
import pymxs # pylint: disable=import-error
from pymxs import runtime as rt # pylint: disable=import-error

def inspect_pymxs():
    """Inspect the classes exported by pymxs and generate a report."""
    api = {}
    classes = inspect.getmembers(pymxs, inspect.isclass)
    totalcnt = 0
    for curclass in classes:
        name = str(curclass[0])
        membercnt = len(curclass[1].__dict__)
        totalcnt += membercnt
        api[name] = membercnt

    fname = os.path.join(rt.sysInfo.tempdir, 'pyms_api.txt')
    with open(fname, 'w') as output:
        for k in sorted(api.keys()):
            output.write(k + " has " + str(api[k]) + " members\n")

    print("Results saved to", fname)
    print("Total number of classes ", len(api))
    print("Total number of API elements ", totalcnt)
    print("Average number of API elements per class ", totalcnt / len(api))

inspect_pymxs()
