#! /usr/bin/env bash
# create a new pip package for a 3ds Max feature
set -e
script=$(dirname $(readlink -f "$0"))

if [ $# -lt 1 ]
then
    echo "please provide the name of the sample to create"
    exit 1
fi

samplename=$1
sampledescr=${2:-$samplename sample}

if [ -e "$samplename" ]
then
    echo "the directory already exists. please rm -f $samplename if you want to reset it"
    exit 1
fi


mkdir -p "$samplename/$samplename"

cat >"$samplename/LICENSE" <<EOF
Copyright (c) 2020 Autodesk, all rights reserved.
EOF

cat >"$samplename/README.md" <<EOF
# HowTo: $samplename

$sampledescr
EOF

cat >"$samplename/setup.py" <<EOF
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="$samplename-autodesk",
    version="0.0.1",
    author="Autodesk Dude",
    author_email="some.dude@autodesk.com",
    description="$sampledescr",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.autodesk.com/windish/maxpythontutorials",
    packages=setuptools.find_packages(),
    entry_points={'3dsMax': 'startup=$samplename:startup'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "LICENSE :: OTHER/PROPRIETARY LICENSE",
        "Operating System :: Microsoft :: Windows"
    ],
    python_requires='>=3.6'
)
EOF

cat >>$samplename/$samplename/__init__.py <<EOF
"""
    $samplename example: $sampledescr
"""
import menuhook
from pymxs import runtime as rt

def $samplename():
    '''$sampledescr'''
    print("$sampledescr")

def startup():
    """
    Hook the function to a menu item.
    """
    menuhook.register(
        "$samplename",
        "howtos",
        $samplename,
        menu=["&Scripting", "Python3 Development", "How To"],
        text="$sampledescr",
        tooltip="$sampledescr")
EOF
