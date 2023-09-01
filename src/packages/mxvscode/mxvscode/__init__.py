"""
    Enable vscode debugging during the startup of 3ds Max.
"""
import sys
import os
import debugpy

def startup():
    """
        Allow the remote vscode debugger to attach to the 3ds Max Python
        interpreter
    """
    print("""mxvscode startup enabling vscode debugging
            (if you don't use VSCode for debugging Python you can uninstall
            mxvscode)""")

    sysexec = sys.executable
    (base, file) = os.path.split(sys.executable)
    if file.lower() == "3dsmax.exe":
        sys.executable = os.path.join(base, "python", "python.exe")
    host = "localhost"
    port = 5678
    debugpy.listen((host, port))
    print(f"-- now ready to receive debugging connections from vscode on (${host}, ${port})")
    sys.executable = sysexec
