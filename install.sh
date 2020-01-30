#! /usr/bin/env bash
set -e
script=$(dirname $(readlink -f "$0"))
installdir=$(pwd)

exiterr() { 
    echo "$@" 1>&2; 
    exit 1
}

# make sure we have 3ds Max in the current path
if [ ! -f ./3dsmax.exe ] 
then
    exiterr "This script must run in a 3ds Max installation"
fi

# make sure curl is available
if [ ! command -v curl ]
then 
    exiterr "curl needs to be in the path."
fi

# install pip
installpip() {
    cd "$installdir/Python37"
    if ! ./python.exe -m pip -V
    then
        local getpip=$(mktemp -d -t tbdXXXXXXXX)
        curl "https://bootstrap.pypa.io/get-pip.py" > "$getpip/get-pip.py"
        ./python.exe "$getpip/get-pip.py" --user
    fi
}

# install pystartup.ms
installpystartup() {
    # FIXME: this is bad, would be better in AppData
    cp "$script/pystartup/pystartup.ms" "$installdir/Scripts/startup"
}


# install all python packages in the repo with the -e option
installpythonpackages() {
    for f in $(find "$script" -name "setup.py")
    do
        local package=$(dirname "$f")
        "$installdir/Python37/python.exe" -m pip install --user -e "$package"
    done
}


echo "Install pip if missing"
installpip

echo "Install pystartup"
installpystartup

echo "install python packages"
installpythonpackages
