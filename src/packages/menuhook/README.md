# menuhook

This package provides a convenient way to hook a Python function
to a 3ds Max menu item.

## Example

When a component is loaded, it can add itself to a 3ds Max menu by doing this:

```python
import menuhook

def fcn():
    """
    Do something. This is the function we want to attach to a menu
    item.
    """
    print("hello")

menuhook.register(
    # the name of the action (will be listed in menu customization dialogs)
    "myaction", 
    # the category for the action
    "my category", 
    # the function to be executed (this is registered for a single run of 3ds Max)
    fcn,
    # the menu for this action. if None is provided the action
    # will not be added to a menu, only created as an action.
    # this can be deeply nested.
    menu=["&Scripting", "Samples"],
    # the menu text. if None is provided, the action name will be used
    text"the text for the menu item", 
    # the menu tool tip. if None is provided, the action name will be used
    tooltip="the tooltip")
```

- The menu item will only be added once for this (action, category) in
a given 3ds Max installation (if the action is already present, the menu item
will not be created)

- If during the startup of 3ds Max the Python module is not loaded (but was
loaded in a previous run), the menu item will still be there. When
invoking it the user will be notified that a Python module required to
implement the function was not loaded.

- The user remains the owner of menus (as it is in the current 3ds Max
implementation). Yes a new component may add an item once to a menu, but
the user is free to remove it, move it, duplicate it and his choices will
never be overridden.

## Q & A

*Q:* Why not using PySide2 directly?

*A:* 3ds Max uses Qt for its menu and technically they can be inspected
and modified during PySide2. But the Menu Manager inside 3ds Max owns the
menus and can regenerate them (using Qt) at any time during the execution
of 3ds Max. And because of that any change made to the menus using PySide2
instead of the 3ds Max Menu Manager will be lost. In short: things will
not behave as expected.


*Q:* My Python component is in a virtual env that I only use for launching
3ds Max for special tasks (e.g. I have a special configuration of 3ds Max for
software development that includes tools that are not used for content
creation... I do this to reduce the clutter for my users) but I still see
its menu items when launching 3ds Max outside this virtual environment. Worse,
when I do this the menu items don't work but display a message that something
is missing.

*A:* There is no solution for this at this point. Menu items, once created,
remain in the menu structure forever and are owned by the user of 3ds Max
who can move them around, duplicate them, remove them, etc. This may
change in the future.


*Q:* Doing this creates a 'macro' and this macro never goes away

*A:* The Python & maxscript apis currently do not allow to remove macros
that have been created. So the [macros](https://help.autodesk.com/view/MAXDEV/2021/ENU/?guid=GUID-3DC75DDE-E4BC-4033-ABA9-A42063036CB9) 
that we create are permanent
but if we don't load the Python packages that implement them during
an execution of 3ds Max they become dangling. We are able to detect that
and notify the users. 


*Q:* Would it be possible to remove menu items (to make them not permanent)?

*A:* The [menu manager](https://help.autodesk.com/view/MAXDEV/2021/ENU/?guid=GUID-258F6015-6B45-4A87-A7F5-BB091A2AE065),
provides a way to remove menu items. This could be used. But the solution
would not be crash proof (it would be difficult to establish that the menu
item has been removed for real, by using only what the menu manager provides).
For now, this will not be supported here.

## How the code works

This is not a sample (but a utility that is used by other samples).

Nevertheless the code is in [menuhook/__init__.py](menuhook/__init__.py) and does:

```python
from pymxs import runtime as rt
```

To get access to the 3dsMax scripting library for Python (pymxs).

Then it uses `rt.macros` to access functions from the [macro scripts](https://help.autodesk.com/view/MAXDEV/2021/ENU/?guid=GUID-3DC75DDE-E4BC-4033-ABA9-A42063036CB9).
As it is now we have to create a macro for a function we want to hook to the menu.

The macro has an action and a category (that identifies it). It is done by this call:

```python
    rt.macros.new(
        category,
        action,
        tooltip,
        text,
        mxs)
```

When this (category, action) exists, we can use `rt.menuman`, the [menu manager](https://help.autodesk.com/view/MAXDEV/2021/ENU/?guid=GUID-258F6015-6B45-4A87-A7F5-BB091A2AE065)
to find the menu in which we want to add an item:

```python
    targetmenu = rt.menuman.findmenu(menu)
```

If we manage to find it, we create an action item for our (action, category) and add it to the 
target menu. Finallly we update the menubar:

```python
    if targetmenu:
        newaction = rt.menuman.createActionItem(action, category)
        if newaction:
            targetmenu.addItem(newaction, -1)
            rt.menuman.updateMenuBar()
```

