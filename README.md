# How To - Practical Examples For Python

![Splash](Splash.png)

This repo contains various Python programming samples.

All the examples in the tutorials are implemented as pip packages. This is a bit heavy for
small things (we provide a setup.py, a LICENSE and everything) but makes things installable
and shareable more easily. As soon as something has dependencies on external packages or requires
more than one Python file, pip packages become very convenient. Because we think it is a good
practice to package 3ds Max Python tools with pip, we provide all our examples in this form.

## Installation

It is not necessary to install the HowTos: the repo can simply be used as a passive
directory of samples and documentation for Python developers.

This being said, it is also possible to install the samples in 3ds Max. This 
will add a Python3 scripting menu to 3ds Max:

![Integration](Integration.png)

The examples and some development goodies will be made available from there.

The installation does the following:
- it installs pip in your 3ds Max installation if it's not already there
- it installs pystartup.ms that enables auto start pip packages
- it installs all the samples in --user and -e mode with pip

If you decide to install the howtos, it is highly recommended that you clone
this git repository locally using git bash (whenever we update the samples,
you will be able to update your local version and re-run the installation scripts):

```bash
# from the directory where you want the sample
git clone https://git.autodesk.com/windish/pythonhowtos.git
```

Also note that *all installation steps decribed here also use gitbash*.

### Option A: Install Everthing Locally in One Step (--user)
(Note: the steps described here need to be done from a gitbash prompt)

The [install.sh](install.sh) script can be used from bash
to install the samples in 3ds Max. The script needs to be run from a
3ds Max installation directory.

### Option B: Install Everything Locally in Two Steps (--user)
(Note: the steps described here need to be done from a gitbash prompt)

It is possible to break up the installation in two steps.

- The [installstartup.sh](installstartup.sh) script can be used
from bash to install pip and [pystartup.ms](/pystartup/pystartup.ms).
It needs to run in the 3ds Max installation directory.

You may do only this step if you don't want the HowTos but you
want to install pip and pystartup.ms.

- The [installhowtos.sh](installhowtos.sh) script can be used from
bash to pip install all the howtos in `--user` mode and `-e` mode (--user
means that the samples will be intalled under `~/AppData/Roaming/Python/Python37/site-packages/`,
and -e means that the packages will be installed as symlinks to the 
source directories so that if the sources change the packages don't need
to be reinstalled).
This script needs to run in the 3ds Max installation directory.

## Uninstalling the HowTos

The steps needed to uninstall the HowTos can be found in [uninstall.md](uninstall.md).

### Option C: Install the howtos in a virtual environment
(Note: the steps described here need to be done from a gitbash prompt)

This last option requires three steps.

It can be used to install the HowTos in a virtual environment (ex:
you may want to have a virtual environment for Python development).

- The first step is the same as the first step described in option B:
[installstartup.sh](installstartup.sh) needs to run in the 3ds Max
installation directory to install pip if it is missing and pystartup.

- The second step consists in installing virtualenv with pip and creating a
virtual environement. These steps are desribed in the [3ds Max documentation](http://help-staging.autodesk.com/view/MAXDEV/2021/ENU/?guid=virtual_env).

- The last step consists in installing the HowTos in the virtual environment.
From the same gitbash prompt, the [installhowtos.sh](/installhowtos.sh)
script can be used to install the HowTos in a virtual environment. First `cd`
to the directory of the virtual env and then (without activating the env) simply
run [installhowtos.sh](/installhowtos.sh) from that directory.

## Packages that are not examples but that are provided in this repo

- [menuhook](menuhook/README.md) is not meant to be an example (but is still interesting as such!) but
as a way of attaching Python functions to 3ds Max menu items. The menuhook package is used by 
most of the other samples.

- [realoadmod](reloadmod/README.md) is small tool that will reload all development modules in one
operation

- [mxvscode](mxvscode/README.md) is a small tool that will automatically import ptvsd (the
VSCode debugging interface) during the startup of 3ds Max and make it accept remote connections.
This may slow down the startup of 3ds Max quite a bit and is meant as a developer-only tool.


## Python How Tos

The samples below are translations of [MAXScript How Tos](https://help.autodesk.com/view/3DSMAX/2020/ENU/?guid=GUID-25C9AD58-3665-471E-8B4B-54A094C1D5C9) that
can be found in the 3ds Max online documentation.

The conversion from MaxScript to Python could have been more mechanical but we chose to implement
the Python version in the best Python way known to us. An example of this is that we use PySide2
(Qt) for the UI as much as possible instead of using more traditional 3ds Max ui mechanisms.

*How To?*

- Develop a Transform Lock Script [transformlock](transformlock/README.md)
- Remove all materials [removeallmaterials](removeallmaterials/README.md)
- Quickly rename selected objects [renameselected](renameselected/README.md)
- Output Object Data to File [speedsheet](speedsheet/README.md)
- Create a quick video preview [quickpreview](quickpreview/README.md)
- Access the Z-Depth Channel [zdepthchannel](zdepthchannel/README.md)

## Python Examples that don't come from maxscript howtos

- Update a progressbar from a Python thread [threadprogressbar](threadprogressbar/README.md)
- Create a single instance modal dialog [singleinstancedlg](singleinstancedlg/README.md)
- Add menu items to open documentation pages in the web browser [inbrowserhelp](inbrowserhelp/README.md)

## 3dsMax startup entry point

[pystartup](pystartup/README.md) provides the maxscript code that, when copied in 3ds Max's
startup directory, will automatically launch pip packages with the 3dsMax startup
entry point.

## Extra Goodies

- [create.sh](create.sh) will generate an empty pip package in the current working directory.
- [install.sh](install.sh) will install pip, install pystartup and pip install all the samples
- [installstartup.sh](installstartup.sh) will install pip and pystartup and nothing more
- [installhowtos.sh](installhowtos.sh) will install only the howtos (works in a virtual env)
- [checks.sh](checks.sh) runs pylint on the code, validates that 3ds Max is named properly,
validates that code blocks in markdown always specify the programming language, checks that
all links are valid in all markdown files of the repo
- [makepreview.sh](makepreview.sh) regenerates the Splash.png for the repo
