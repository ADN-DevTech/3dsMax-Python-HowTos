# Plugin Packages in 2025 and Integration With the New Menu System

In 3ds Max 2025 and above, plugin packages may contain python script components.
When installing the samples from this repo in a 2025 version of 3ds Max,
the [adn-devtech-python-howtos](/src/adn-devtech-python-howtos) plugin package
is copied to "$ProgramData/Autodesk/ApplicationPlugins". The [PackageContents.xml](/src/adn-devtech-python-howtos/PackageContents.xml)
file of this plugin package declares a python pre-start-up script:

```xml
  <Components Description="pre-start-up scripts parts">
     <RuntimeRequirements OS="Win64" Platform="3ds Max" SeriesMin="2025" SeriesMax="2025" />
     <ComponentEntry ModuleName="./scripts/pyStartup.py" />
  </Components>
```

The [./scripts/pyStartup.py](/src/adn-devtech-python-howtos/scripts/pyStartup.py) script
first does what [pystartup.ms](/src/pystartup/pystartup.ms) used to do:

```python
def _python_startup():
    try:
        import pkg_resources
    except ImportError:
        print('startup Python modules require pip to be installed.')
        return	
    for dist in pkg_resources.working_set: 
        entrypt = pkg_resources.get_entry_info(dist, '3dsMax', 'startup')
        if not (entrypt is None):
            try:
                fcn = entrypt.load()
                fcn()
            except Exception as e:
                print(f'skipped package startup for {dist} because {e}, startup not working')

```

Then it integrates the samples to the new menu system of 2025:

```python
    # configure 2025 menus
    from pymxs import runtime as rt
    from menuhook import register_howtos_menu_2025
    def menu_func():
        menumgr = rt.callbacks.notificationparam()
        register_howtos_menu_2025(menumgr)

    # menu system
    cuiregid = rt.name("cuiRegisterMenus")
    howtoid = rt.name("pyScriptHowtoMenu")
    rt.callbacks.removescripts(id=cuiregid)
    rt.callbacks.addscript(cuiregid, menu_func, id=howtoid)

```


## Integration With the New Menu System

The [menuhook](/src/menuhook/) code has been reworked to integrate menu items for the 
various howtos to the new menu system:

```python
def register(action, category, fcn, menu=None, text=None, tooltip=None, in2025_menuid=None, id_2025=None):
```

Takes two new parameters: 
- `in2025_menuid` : the guid of the containing menu
- `id_2025i` : the guid of the item to create

And stores the needed menu items in the `registered_items` list:

```python
            registered_items.append((in2025_menuid, id_2025, category, action))
```

The `register_howotos_menu_2025` function, called whenever the menu system needs to regenerate its structure, uses the `registered_items` list to add items to the menu manager:

```python
    # hook the registered items
    for reg in registered_items:
        (in2025_menuid, id_2025, category, action) = reg
        scriptmenu = menumgr.getmenubyid(in2025_menuid)
        if scriptmenu is not None:
            try:
                actionitem = scriptmenu.createaction(id_2025, 647394, f"{action}`{category}")
            except Exception as e:
                print(f"Could not create item {category}, {action} in menu {in2025_menuid} because {e}")
        else:
            print(f"Could not create item {category}, {action}, in missing menu {in2025_menuid}")


```
