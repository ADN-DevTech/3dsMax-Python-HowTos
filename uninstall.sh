#! /usr/bin/env bash
set -e
script="$(dirname "$(readlink -f "$0")")"
source "$script/scripts/inst.sh"

# make sure we have 3ds Max in the current path
if [ ! -f ./3dsmax.exe ]
then
    exiterr "This script must run in a 3ds Max installation directory."
fi

echo "Uninstall python packages"
"$script"/uninstallhowtos.sh

echo "Uninstall pip"
(
    cd "$pythonpath"
    ./python.exe -m pip uninstall pip
)

echo "Uninstall pystartup and adn-devtech-python-howtos"
rm -f "$startuppath/pystartup.ms"
rm -fr "$ProgramData/Autodesk/ApplicationPlugins/adn-devtech-python-howtos"

