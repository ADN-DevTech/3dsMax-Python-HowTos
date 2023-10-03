set -e
script="$(dirname "$(readlink -f "$0")")"
installdir="$(pwd)"
packagedir="$script/src/packages" 

# we need to know the max version. Normally this should be part of the current install dir
# but it can be defined manually with the VERSION environment variable before calling
# the scripts. If it is not it will be inferred from the installation directory
dirversion=$(pwd | grep -o '20[0-9]\{2\}' || echo "")
version=${VERSION:-$dirversion}
if [ -z "$version" ]
then
    # Take the latest ADSK_3DSMAX_x64 dir
    v=$(env | grep 'ADSK_3DSMAX_x64_20[0-9]\{2\}' | sed 's/=.*$//; s/^ADSK_3DSMAX_x64_//' | sort -n -r | head -n 1)
    if (( "$v" > 2021 ))
    then
        version=$v
    else
        echo "3ds Max Version number could not be inferred from the installation directory"
        echo "The VERSION env variable can be set before calling this script to define the 3ds Max Version (ex: VERSION=2022)" 
        exit 1
    fi
fi

localsettings="$HOME/AppData/Local/Autodesk/3dsMax"
if [ ! -f "$installdir/installSettings.ini" ]
then 
    startuppath="$localsettings/$version - 64bit/ENU/scripts/startup"
elif grep -i "installedBuild=1" "$installdir/installSettings.ini" >/dev/null 2>&1
then
    startuppath="$localsettings/$version - 64bit/ENU/scripts/startup"
elif iconv -f UTF-16 -t UTF-8 <InstallSettings.ini | grep -i "installedBuild=1" >/dev/null 2>&1
then
    startuppath="$localsettings/$version - 64bit/ENU/scripts/startup"
else
    startuppath="$installdir/scripts/startup"
fi

if [ "$version" -le "2022" ]
then
    pythonpath="Python37"
else
    pythonpath="Python"
fi

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
    cd "$installdir/$pythonpath"
    if ! ./python.exe -m pip -V 2>/dev/null
    then
        if ! ./python.exe -m ensurepip 2>/dev/null
        then
            local getpip="$(mktemp -d -t tbdXXXXXXXX)"
            curl "https://bootstrap.pypa.io/get-pip.py" > "$getpip/get-pip.py"
            ./python.exe "$getpip/get-pip.py" --user
        fi
    fi
}

# install pystartup.ms or adn-dectech-python-howtos (plugin package) for 2025
installpystartup() {
    if [ "$version" -lt "2025" ]
    then
        cp "$script/src/pystartup/pystartup.ms" "$startuppath"
    else
        cp "$script/src/adn-devtech-python-howtos" "$ProgramData/Autodesk/ApplicationPlugins"
    fi
}


# install all Python packages in the repo with the -e option
installpythonpackages() {
    for f in $(find "$packagedir" -name "setup.py")
    do
        local package="$(dirname "$f")"
        "$installdir/$pythonpath/python.exe" -m pip install --user -e "$package"
    done
}

# uninstall all Python packages in the repo
uninstallpythonpackages() {
    for f in $(find "$packagedir" -name "setup.py")
    do
        local package="$(basename "$(dirname "$f")")"
        local pname="$package-autodesk"
        "$installdir/$pythonpath/python.exe" -m pip uninstall -y "$pname"
    done
}

