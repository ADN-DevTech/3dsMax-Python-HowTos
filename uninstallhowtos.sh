#! /usr/bin/env bash
set -e
script=$(dirname $(readlink -f "$0"))
source "$script/inst.sh"

venvscript () {
    echo "cd Scripts"
    echo "call activate.bat"
    for f in $(find "$script" -name "setup.py")
    do
        local package=$(basename "$(dirname "$f")")
        echo "pip.exe uninstall -y $package-autodesk"
    done
}

if [ -f "Scripts/activate.bat" ]
then
    # this is a virtual env
    echo "unininstall python packages from virtual env"
    read -p "Is this what you want (Y/n)? " -n 1 -r
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        tmpfile=$(mktemp /tmp/XXXXXXX.bat)
        venvscript > "$tmpfile"
        cmd //C "$tmpfile"
        rm "$tmpfile"
    fi
elif [ -f ./3dsmax.exe ]
then
    # this is the default installation
    echo "uininstall python packages from your user account"
    read -p "Is this what you want (Y/n)? " -n 1 -r
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        uninstallpythonpackages
    fi
else
    exiterr "This script must run in a 3ds Max installation directory or in a virtual environment directory."
fi

