# pystartup

`pystartup.ms` is a MAXScript file that adds to 3ds Max the ability to startup
pip packages when they are present in the python environment.


## Installation
The pystartup.ms file must be copied to the 3dsMax startup directory.

## How to make a pip package "auto start"

To be automatically loaded by this mechanism, a pip package must
implement the 3dsMax startup entry point.


This is done by adding a line like this in the setup.py file of
a pip package:

```python
    entry_points={'3dsMax': 'startup=yourpackagename:startup'},
```

where `yourpackagename` is the name of the package (i.e. import
yourpackagename works) and startup is an exported function of 
yourpackagename that will be called during startup.

Most if not all python samples in this repo implement this entry
point. [transformlock's setup script](/transformlock/setup.py) can
be taken as en example as well as [transformlock's \_\_init\_\_.py](/transformlock/transformlock/__init__.py).


## The maxscript code

The pystartup.ms code consists in a call to python.execute that runs
a small python program.

```maxscript
if isProperty python "execute" then (
    python.execute ("def _python_startup():\n" +
	"    try:\n" +
    "        import pkg_resources\n" +
    "    except ImportError:\n" +
    "        print('startup python modules require pip to be installed.')\n" +
    "        return\n" +	
    "    for dist in pkg_resources.working_set: \n" +
    "        entrypt = pkg_resources.get_entry_info(dist, '3dsMax', 'startup')\n" +
    "        if not (entrypt is None):\n" +
    "            try:\n" +
    "                fcn = entrypt.load()\n" +
    "                fcn()\n" +
    "            except:\n" +
	"                print('skipped package startup for {}, startup not working'.format(dist))\n" +
    "_python_startup()\n" +
    "del _python_startup")
)
``` 

## The python code

Here is the python code used for the entry points:

```python
def _python_startup():
    try:
        import pkg_resources
    except ImportError:
        print('startup python modules require pip to be installed.')
        return
    for dist in pkg_resources.working_set: 
        entrypt = pkg_resources.get_entry_info(dist, '3dsMax', 'startup')
        if not (entrypt is None):
            try:
                fcn = entrypt.load()
                fcn()
            except:
                print('skipped package startup for {}, startup not working'.format(dist))
_python_startup()
del _python_startup
```

`pkg\_resources` is part of [setuptools](https://setuptools.readthedocs.io/en/latest/pkg_resources.html) 
and comes installed with pip. It allows this script to discover packages present
in the environment.

The script first imports pkg\_resources.

```python
        import pkg_resources
```

it then iterates all packages in the environment:

```python
    for dist in pkg_resources.working_set: 
```

It then tries to find the 3dsMax startup entry point in the package:

```python
        entrypt = pkg_resources.get_entry_info(dist, '3dsMax', 'startup')
```

And if this works, loads and executes the entry point:

```python
        if not (entrypt is None):
            try:
                fcn = entrypt.load()
                fcn()
            except:
                print('skipped package startup for {}, startup not working'.format(dist))
```
