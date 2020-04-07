'''
    Lists all the files in a folder
'''
import os
from pymxs import runtime as rt # pylint: disable=import-error

PY_SCRIPTS_DIR = os.path.join(rt.getDir(rt.Name("scripts")), 'python')
for root, dirs, files in os.walk(PY_SCRIPTS_DIR, topdown=False):
    for name in files:
        print(name)
