#! /usr/bin/env bash
set -e
script=$(dirname $(readlink -f "$0"))
source "$script/inst.sh"

# make sure we have 3ds Max in the current path
if [ ! -f ./3dsmax.exe ]
then
    exiterr "This script must run in a 3ds Max installation directory."
fi

echo "install python packages"
"$script"/uninstallhowtos.sh

echo "Uninstall pip"
(
    cd Python37
    ./python.exe -m pip uninstall pip
)

echo "Uninstall pystartup"
rm "$startuppath/pystartup.sh"
