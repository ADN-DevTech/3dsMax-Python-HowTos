# HowTo: transformlock

[Original MaxScript Tutorial](https://help.autodesk.com/view/3DSMAX/2020/ENU/?guid=GUID-8EB13535-72B4-439C-94D3-E93434BA163B)
[Source Code](transformlock/__init__.py) 

*Goals:* 
- learn how to call a function in pymxs
- learn how to hook a python function to a 3ds Max ui element

## Explanations

The shows how to create a minimal python tool for 3ds Max. This tools adds a menu item
to the Scripting menu to lock all transformations on the selection.

## Using the tool

From the 3ds Max listener window we can do:

```python
import transformlock

transformlock.startup()
```

If we install this sample as a pip package it will be automatically
started during the startup of 3ds Max (because it defines a startup
entry point for 3ds Max).

## Understanding the code

We first import menuhook. This package provides an easy way to create a menu item
for running a python function.

```python
import menuhook
```

We also import pymxs. Pymxs lets python access the whole MAXScript scripting library.

```python
from pymxs import runtime as rt
```

The core business logic of the program comes from the lock\_selection function. This uses
the setTransformLockFlags of ([node common methods](https://help.autodesk.com/view/3DSMAX/2020/ENU/?guid=GUID-D1D7EB56-A370-4B07-99B4-BC779FB87CAF#GUID-D1D7EB56-A370-4B07-99B4-BC779FB87CAF__SECTION_130281B392F64446B4AE8562EAD75531))
to lock all (`rt.Name("all")` transforms on the whole selection (`rt.selection`)):

```python
def lock_selection():
    '''Lock all transforms on the selection'''
    rt.setTransformLockFlags(rt.selection, rt.Name("all"))
```

We then define the startup function. This function will be called by the 3ds Max
entry point (if this project is installed as a pip package). We can also call it
manually (in the listener window) if we prefer.

```python
def startup():
    """
    Hook the transform lock function to a menu item.
    """
    menuhook.register(
        "howtos",
        "transformlock",
        fcn,
        menu=[ "&Scripting", "Python3 Development", "How To"],
        menutext"Lock transformations for the selection",
        tooltip="Lock transformations for the selection")
```

