"""
    Demonstrate saving a 3ds Max file.
"""
from os import path
from pymxs import runtime as rt # pylint: disable=import-error

FILEPATH = path.join(rt.sysInfo.tempdir, "test.max")
rt.saveMaxFile(FILEPATH)
print(f"Requested filename {FILEPATH}\n path {rt.maxFilePath}\n file {rt.maxFileName}")
