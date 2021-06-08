# HowTo: removeallmaterials
[Original MaxScript Tutorial](https://help.autodesk.com/view/MAXDEV/2022/ENU/?guid=GUID-BB996DFB-0367-4DFF-A1CC-50BEB3A97757)
[Source Code](removeallmaterials/__init__.py)

*Goals:* 
- learn how to call a function in pymxs
- learn how to hook a Python function to a 3ds Max ui element

## Explanations

The shows how to create a minimal Python tool for 3ds Max. This tools adds a menu item
to the Scripting menu to remove all materials from the scene. 

## Using the tool

From the 3ds Max listener window we can do:

```python
import removeallmaterials

removeallmaterials.startup()
```

If we install this sample as a pip package it will be automatically
started during the startup of 3ds Max (because it defines a startup
entry point for 3ds Max).

## Understanding the code

We first import menuhook. This package provides an easy way to create a menu item
for running a Python function.

```python
import menuhook
```

We also import pymxs. Pymxs lets Python access the whole MAXScript scripting library.

```python
from pymxs import runtime as rt
```

The core business logic of the program comes from the remove\_all\_materials function. This iterates
`rt.objects` and sets the `material` of these objects to None.

```python
def remove_all_materials():
    '''Remove all materials from the scene'''
    for obj in rt.objects:
        obj.material = None
```

We then define the startup function. This function will be called by the 3ds Max
entry point (if this project is installed as a pip package). We can also call it
manually (in the listener window) if we prefer.

```python
def startup():
    """
    Hook the function to a menu item.
    """
    menuhook.register(
        "removeallmaterials",
        "howtos",
        remove_all_materials,
        menu=["&Scripting", "Python3 Development", "How To"],
        text="Remove all materials from the scene",
        tooltip="Remove all materials from the scene")
```

