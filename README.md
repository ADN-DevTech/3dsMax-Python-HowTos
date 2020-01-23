# How To - Practical Examples For Python

This repo contains a python implementation of the [MaxScript How Tos](https://help.autodesk.com/view/3DSMAX/2020/ENU/?guid=GUID-25C9AD58-3665-471E-8B4B-54A094C1D5C9)
provided in the 3ds Max documentation.

The conversion from MaxScript to Python could have been more mechanical but we chose to implement
the python version in the best python way known to us. An example of this is that we use PySide2
(Qt) for the UI as much as possible instead of using more traditional 3ds Max ui mechanisms.

## Before we start

All the examples in the tutorials are implemented as pip packages. This is a bit heavy for
small things (we provide a setup.py, a LICENSE and everything) but makes things installable
and shareable more easily. As soon as something has dependencies on external packages or requires
more than one python file, pip packages become very convenient. Because we think it is a good
practice to package 3ds Max python tools with pip, we provide all our examples in this form.

### Packages that are not examples but that are provided in this repo

- [menuhook](menuhook/README.md) is not meant to be an example (but is still interesting as such!) but
as a way of attaching python functions to 3ds Max menu items. The menuhook package is used by 
most of the other samples.


## Python Examples

How To?

- Develop a Transform Lock Script [transformlock](transformlock/README.md)
- Remove all materials [removeallmaterials](removeallmaterials/README.md)
- Quickly rename selected objects [renameselected](renameselected/README.md)
- Output Object Data to File [speedsheet](speedsheet/README.md)
- Create a quick video preview [quickpreview](quickpreview/README.md)

## Python Examples that don't come from maxscript howtos

- Update a progressbar from a python thread [threadprogressbar](threadprogressbar/README.md)

## Extra Goodies

- [create.sh](create.sh) will generate an empty pip package in the current working directory.
