# Installation

It is possible to install the samples in 3ds Max. This 
will add a Python3 scripting menu to 3ds Max:

![Integration](/doc/Integration.png)

The examples and some development goodies will be made available from there.

The installation does the following:
- it installs pip in your 3ds Max installation if it's not already there
- it installs pystartup.ms that enables auto start pip packages
- it installs all the samples in --user and -e mode with pip

If you decide to install the howtos, it is highly recommended that you clone
this git repository locally using git bash (whenever we update the samples,
you will be able to update your local version and re-run the installation scripts):

```bash
# from the directory where you want the sample
git clone https://github.com/ADN-DevTech/3dsMax-Python-HowTos.git
```

Also note that *all installation steps decribed here also use git bash* (it is
possible to use another client for git but all installation scripts in
this repo use bash).

### Option A: Install Everthing Locally in One Step (--user)
> Note: the steps described here need to be done from a git bash prompt

The [install.sh](/install.sh) script can be used from bash
to install the samples in 3ds Max. The script needs to be run from a
3ds Max installation directory.

### Option B: Install Everything Locally in Two Steps (--user)
> Note: the steps described here need to be done from a git bash prompt

It is possible to break up the installation in two steps.

- The [installstartup.sh](/installstartup.sh) script can be used
from bash to install pip and [pystartup.ms](/src/pystartup/pystartup.ms).
It needs to run in the 3ds Max installation directory.

You may do only this step if you don't want the HowTos but you
want to install pip and pystartup.ms.

- The [installhowtos.sh](/installhowtos.sh) script can be used from
bash to pip install all the howtos in `--user` mode and `-e` mode (--user
means that the samples will be intalled under `~/AppData/Roaming/Python/Python37/site-packages/`,
and -e means that the packages will be installed as symlinks to the 
source directories so that if the sources change the packages don't need
to be reinstalled).
This script needs to run in the 3ds Max installation directory.

## Uninstalling the HowTos

The steps needed to uninstall the HowTos can be found in [uninstall.md](/doc/uninstall.md).

### Option C: Install the howtos in a virtual environment
> Note: the steps described here need to be done from a git bash prompt

This last option requires three steps.

It can be used to install the HowTos in a virtual environment (ex:
you may want to have a virtual environment for Python development).

- The first step is the same as the first step described in option B:
[installstartup.sh](/installstartup.sh) needs to run in the 3ds Max
installation directory to install pip if it is missing and pystartup.

- The second step consists in installing virtualenv with pip and creating a
virtual environment. These steps are described in the [3ds Max documentation](https://help.autodesk.com/view/MAXDEV/2022/ENU/?guid=Max_Python_API_python_3_support_virtual_env_html).
- The last step consists in installing the HowTos in the virtual environment.
From the same git bash prompt, the [installhowtos.sh](/installhowtos.sh)
script can be used to install the HowTos in a virtual environment. First `cd`
to the directory of the virtual env and then (without activating the env) simply
run [installhowtos.sh](/installhowtos.sh) from that directory.


