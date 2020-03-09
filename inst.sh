set -e
script=$(dirname $(readlink -f "$0"))
installdir=$(pwd)
startuppath="$HOME/AppData/Local/Autodesk/3dsMax/2021 - 64bit/ENU/scripts/startup"
exiterr() { 
    echo "$@" 1>&2 
    exit 1
}

# make sure curl is available
if ! command -v curl >/dev/null 2>&1
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
    cp "$script/pystartup/pystartup.ms" "$startuppath"
}


# install all python packages in the repo with the -e option
installpythonpackages() {
    for f in $(find "$script" -name "setup.py")
    do
        local package=$(dirname "$f")
        "$installdir/Python37/python.exe" -m pip install --user -e "$package"
    done
}
