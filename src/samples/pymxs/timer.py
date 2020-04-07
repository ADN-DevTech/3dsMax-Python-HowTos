"""
    Demonstrate timers.
"""
import threading
import time
import pymxs # pylint: disable=import-error

GLOBAL_ARGS = {
    "nativeCallTagA": 1,
    "nativeCallTagB": "",
    "nativeCallWithWrapperObjTagA": 1,
    "nativeCallWithWrapperObjName": u"TestName",
    "wrapObj": None
}

def native_call(first, second, local_env):
    """Run timer payload"""
    local_env["nativeCallTagA"] = first
    local_env["nativeCallTagB"] = second

def native_with_wrapper(first, wrap_obj, local_env):
    """Run timer payload"""
    local_env["nativeCallWithWrapperObjTagA"] = first
    wrap_obj.Name = local_env["nativeCallWithWrapperObjName"]
    local_env["wrapObj"] = wrap_obj

def check(local_env):
    """Validate expected results"""
    is_success = True
    if local_env["nativeCallTagA"] != 10 or local_env["nativeCallTagB"] != "second":
        is_success = False
        print("Error: Incorrect native call for threading timer")

    wrap_teapot = local_env["wrapObj"]
    if (local_env["nativeCallWithWrapperObjTagA"] != 10 or
            wrap_teapot is None or
            wrap_teapot.Name != local_env["nativeCallWithWrapperObjName"]):
        is_success = False
        print("Error: Incorrect native call with wrapper object for threading timer")

    return is_success

def main():
    """Demonstrate timers"""
    wrap_teapot = pymxs.runtime.Teapot()

    # test native call
    native_call_timer = threading.Timer(
        0.1,
        native_call,
        [10, "second"],
        kwargs={"local_env": GLOBAL_ARGS})
    native_with_wrapper_timer = threading.Timer(
        0.1,
        native_with_wrapper,
        kwargs={"first": 10, "wrap_obj": wrap_teapot, "local_env": GLOBAL_ARGS})
    print("Start timer")
    native_call_timer.start()
    native_with_wrapper_timer.start()
    time.sleep(0.2)
    if check(GLOBAL_ARGS):
        print("threading timer success")

main()
