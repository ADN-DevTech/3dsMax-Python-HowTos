# Uninstalling the HowTos

It is easy undo the work of the installation scripts. The steps needed
to uninstall everything are explained here.

## uninstall.sh

The `uninstall.sh` script will:

- uninstall pip
- uninstall the pip packages of the samples
- remove pystartup.ms

The menu items in 3ds Max will not be removed automatically (the steps
needed to remove them are explained at the bottom of this page).

## Removing pystartup.ms (manual uninstall)

### For 3dsMax before 2025
After the installation, pystartup.ms will be copied to:

"$HOME/AppData/Local/Autodesk/3dsMax/2022 - 64bit/ENU/scripts/startup"

It can simply be removed from there.

> Note: pystartup.ms finds the pip packages
> in the Python environment. If they expose a 3dsMax startup entry point
> the entry point is called during the 3ds Max startup.

By removing this file none of the HowTo packages will be started
automatically when 3ds Max starts.

### For 3dsMax 2025 and greater

Starting with 2025, pystartup.ms is no longer needed. Instead the 
[adn-devtech-python-howtos](/src/adn-devtech-python-howtos) directory is 
copied to "C:\ProgramData\Autodesk\ApplicationPlugins". 

It can be manually removed by doing (from gitbash):

```bash
rm -fr "$ProgramData/Autodesk/ApplicationPlugins/adn-devtech-python-howtos"
```

## Removing pip (manual uninstall)

The installation script also install pip in user mode.

You can also remove pip (although this is not really recommended).
To remove it: 

```bash
# current directory needs to be maxinstallationfolder/Python37:
./python.exe -m pip uninstall pip
```

## Removing the individual HowTos (manual uninstall)

The HowTos can be uninstalled individually by calling:

```bash
# current directory needs to be maxinstallationfolder/Python37:
./python.exe -m pip uninstall reloadmod-autodesk
```

> Note that the full package name should be the name of the
> package directory followed by `-autodesk`.

## Uninstalling all the HowTos at Once (manual uinstall)

The [uninstallhowtos.sh](/uninstallhowtos.sh) can be used
to uninstall all the howtos at once. This will automatically call
`./python.exe -m pip uninstall` for all the HowTos packages.

## Getting rid of the menu items and the action items in 3ds Max

Menu items and action items added to 3ds Max are permanent. 
Cleaning up the menu items needs to be done manually from the
user interface (Customize > Customize User Interface > Menus).

