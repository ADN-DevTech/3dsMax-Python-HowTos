#! /usr/bin/env bash
set -e
script="$(dirname "$(readlink -f "$0")")"
source "$script/scripts/inst.sh"
echo "Installing for 3ds Max version: $version. If this is not correct please set the VERSION environment variable before runnning the script. (ex: VERSION=2022)"

# make sure cygpath is available
if ! command -v cygpath >/dev/null 2>&1
then
    exiterr "cygpath needs to be in the path."
fi

# make sure cmd is available
if ! command -v cmd >/dev/null 2>&1
then
    exiterr "cmd needs to be in the path."
fi

venvscript () {
    echo "cd Scripts"
    echo "call activate.bat"
    for f in $(find "$packagedir" -name "setup.py")
    do
        local package="$(dirname "$f")"
        echo "pip.exe install -e \"$(cygpath -d "$package")\""
    done
}

set -e
if [ -f "Scripts/activate.bat" ]
then
    # this is a virtual env
    echo "install python packages in virtual env"
    read -p "Is this what you want (Y/n)? " -r
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        tmpfile="$(mktemp /tmp/XXXXXXX.bat)"
        venvscript > "$tmpfile"
        cmd //C "$tmpfile"
        rm "$tmpfile"
    fi
elif [ -f ./3dsmax.exe ]
then
    # this is the default installation
    echo "install python packages in your account with --user (not in a virtual env)"
    read -p "Is this what you want (Y/n)? " -r
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        installpythonpackages
    fi
else
    exiterr "This script must run in a 3ds Max installation directory or in a virtual environment directory.."
fi
