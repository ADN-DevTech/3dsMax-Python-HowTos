"""
    Enable vscode debugging during the startup of 3ds Max.
"""
import ptvsd
def startup():
    """
        Allow the remote vscode debugger to attach to the 3ds Max python
        interpreter
    """
    print("""mxvscode startup enabling vscode debugging
            (if you don't use VSCode for debugging python you can uninstall
            mxvscode)""")
    ptvsd.enable_attach()
    print("-- now ready to receive debugging connections from vscode")
