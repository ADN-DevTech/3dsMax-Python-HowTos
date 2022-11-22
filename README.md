# 3ds Max 2021 and 2022 Python How Tos
### Practical Python 3.7 Development Examples For 3ds Max

![Splash](/doc/Splash.png)

This repo contains various Python programming examples and tutorials targeting [3ds Max 2021 and 2022](https://www.autodesk.ca/en/products/3ds-max/overview)'s 
Python 3.7 support (the samples are not meant to be used with the Python 2.7 interpreter shipped
in previous versions of 3ds Max).

All the examples in the tutorials are implemented as pip packages. This is a bit heavy for
small things (we provide a setup.py, a LICENSE and everything) but makes things installable
and shareable more easily. As soon as something has dependencies on external packages or requires
more than one Python file, pip packages become very convenient. Because we think it is a good
practice to package 3ds Max Python tools with pip, we provide all our examples in this form.

## Installation

It is not necessary to install the HowTos: the repo can simply be used as a passive
directory of samples and documentation for Python developers.

- Installing the HowTos will add menu items to 3ds Max, and is documented [here](doc/install.md)
- After an update from github it is necessary to rerun install scripts to get everything 
working as expected


## Python How Tos

### New content

[mxs2py](/src/packages/mxs2py/README.md) Automatically convert maxscript to python 

### Samples

The samples below are translations of [MAXScript How Tos](https://help.autodesk.com/view/MAXDEV/2022/ENU/?guid=GUID-25C9AD58-3665-471E-8B4B-54A094C1D5C9) that
can be found in the 3ds Max online documentation.

The conversion from MaxScript to Python could have been more mechanical but we chose to implement
the Python version in the best Python way known to us. An example of this is that we use PySide2
(Qt) for the UI as much as possible instead of using more traditional 3ds Max ui mechanisms.

*How To?*

- Develop a Transform Lock Script [transformlock](/src/packages/transformlock/README.md)
- Remove all materials [removeallmaterials](/src/packages/removeallmaterials/README.md)
- Quickly rename selected objects [renameselected](/src/packages/renameselected/README.md)
- Output Object Data to File [speedsheet](/src/packages/speedsheet/README.md)
- Create a quick video preview [quickpreview](/src/packages/quickpreview/README.md)
- Access the Z-Depth Channel [zdepthchannel](/src/packages/zdepthchannel/README.md)

## Python Examples that don't come from maxscript howtos

- Update a progressbar from a Python thread [threadprogressbar](/src/packages/threadprogressbar/README.md)
- Create a single instance modal dialog [singleinstancedlg](/src/packages/singleinstancedlg/README.md)
- Add menu items to open documentation pages in the web browser [inbrowserhelp](/src/packages/inbrowserhelp/README.md)
- Integrate a Python Console [pyconsole](/src/packages/pyconsole/README.md)
- Run code on thre main thread [mxthread](/src/packages/mxthread/README.md)
- Automatically convert maxscript to python [mxs2py](/src/packages/mxs2py/README.md)

## Python Samples

Python samples can be found in [src/samples](/src/samples). These samples may already be in your 3ds Max
installation directories.

## 3dsMax startup entry point

[pystartup](/src/pystartup/README.md) provides the maxscript code that, when copied to 3ds Max's
startup directory, will automatically launch pip packages with the 3dsMax startup
entry point.

## Tools

The following packages are not really examples but Python tools.

- [menuhook](/src/packages/menuhook/README.md) is not meant to be an example (but is still interesting as such!) but
as a way of attaching Python functions to 3ds Max menu items. The menuhook package is used by 
most of the other samples.

- [realoadmod](/src/packages/reloadmod/README.md) is small tool that will reload all development modules in one
operation

- [mxvscode](/src/packages/mxvscode/README.md) is a small tool that will automatically import ptvsd (the
VSCode debugging interface) during the startup of 3ds Max and make it accept remote connections.
This may slow down the startup of 3ds Max quite a bit and is meant as a developer-only tool.

## Extra Goodies

- [install.sh](install.sh) will install pip, install pystartup and pip install all the samples
- [uninstall.sh](uninstall.sh) will uninstall what was installed with install.sh
- [installstartup.sh](installstartup.sh) will install pip and pystartup and nothing more
- [installhowtos.sh](installhowtos.sh) will install only the howtos (works in a virtual env)
- [checks.sh](/scripts/checks.sh) runs pylint on the code, validates that 3ds Max is named properly,
validates that code blocks in markdown always specify the programming language, checks that
all links are valid in all markdown files of the repo
- [create.sh](/scripts/create.sh) will generate an empty pip package in the current working directory.
