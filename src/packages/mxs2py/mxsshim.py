"""
This file provides a python implementation for maxscript syntactic elements.
Note: maxscript has many syntactic elements that have not python equivalent,
the workarounds provided here build a maxscript string from a python construct
and then evaluate the maxscript.

Remark: this is very incomplete and buggy (the translator will output this,
but this will not execute properly... some more work is needed to make this happen!).
"""
# pylint: disable=invalid-name,import-error, fixme
from pymxs import runtime as rt
from pymxs import contextmanager

rt.execute("fn as_type a b = (a as b)")

def max(*args): # pylint: disable=redefined-builtin
    '''Runs a max menu command, just like the maxscript max statement.'''
    return rt.execute("max " + " ".join(args))

def time(*args):
    """evaluates an mxs time by safe executing it"""
    return rt.safeExecute(*args)

@contextmanager
def printAllElements(onoff):
    """dummy implementation of context, todo: implement?"""
    print(f"SetContext printAllElements {onoff}")
    yield
    print(f"ClearContext printAllElements {onoff}")

@contextmanager
def defaultAction(onoff):
    """dummy implementation of context, todo: implement?"""
    print(f"SetContext defaultAction {onoff}")
    yield
    print(f"ClearContext defaultAction {onoff}")

@contextmanager
def MXSCallstackCaptureEnabled(onoff):
    """dummy implementation of context, todo: implement?"""
    print(f"SetContext MXSCallstackCaptureEnabled {onoff}")
    yield
    print(f"ClearContext MXSCallstackCaptureEnabled {onoff}")

@contextmanager
def dontRepeatMessages(onoff):
    """dummy implementation of context, todo: implement?"""
    print(f"SetContext dontRepeatMessages {onoff}")
    yield
    print(f"ClearContext dontRepeatMessages {onoff}")

@contextmanager
def macroRecorderEmitterEnabled(onoff):
    """dummy implementation of context, todo: implement?"""
    print(f"SetContext macroRecorderEmitterEnabled {onoff}")
    yield
    print(f"ClearContext macroRecorderEmitterEnabled {onoff}")

@contextmanager
def in_node(node): # pylint: disable=unused-argument
    """dummy implementation of context, todo: implement?"""
    print("SetContext in_node")
    yield
    print("ClearContext in_node")

@contextmanager
def in_coordsys(coordsys): # pylint: disable=unused-argument
    """dummy implementation of context, todo: implement?"""
    print("SetContext in_coordsys")
    yield
    print("ClearContext in_coordsys")


def path(p):
    """Evaluates a $ path by safe executing it"""
    return rt.safeExecute(p)

rt.python_macroscripts = {}

class MacroScript(): # pylint: disable=too-few-public-methods
    """incomplete very early macroscript wrapper"""
    events = {}

    def __init__(self, macroscriptname, **kwargs):
        # pylint: disable=line-too-long
        rt.python_macroscripts[macroscriptname] = self
        function_block = "\n".join(
                list(map(
                    lambda k: f'on {k} do ( python_macroscripts["{macroscriptname}"].events["{k}"] () )',
                    self.events)))
        named_args = "  ".join(list(map(lambda k: f"{k}:{kwargs[k]}", kwargs)))
        mxs_string = f"macroscript {macroscriptname} {named_args} ( {function_block} )"
        rt.execute(mxs_string)

    def on (self, eventname, handler):
        """Add an event"""
        self.events[eventname] = handler

class RolloutItem():# pylint: disable=too-few-public-methods
    """incomplete very early rollout item wrapper"""
    def __init__(self, kind, var, *args, **kwargs):
        # we need to be able to format all variations of args that we can receive
        label = f'"{args[0]}"' if len(args)>0 else ""
        def formatkv(k, value):
            """Format a key value in mxs"""
            if k=="width":
                return f"width:{value}"
            if k=="height":
                return f"height:{value}"
            if k=="orient":
                return f"orient:#{str(value)}"
            if k=="across":
                return f"across:{value}"
            if k=="degrees":
                return f"degrees:{value}"
            return "???"

        kw = " ".join(list(map(lambda kw: formatkv(kw, kwargs[kw]), kwargs)))

        self.string  = f'{kind} {var} {label} {kw}'

class RolloutGroup():# pylint: disable=too-few-public-methods
    """incomplete very early rollout group wrapper"""
    def __init__(self, label, *args):
        """Construct a rollout group"""
        items = "\n".join(map(lambda x: x.string, args))
        self.string = f'group "{label}" ( {items} )'

rt.python_rollouts = {}
class Rollout():# pylint: disable=too-few-public-methods
    """incomplete very early rollout wrapper"""
    events = {}
    itemlist = []

    def __init__(self, rolloutname, **_):
        """Construct a rollout"""
        # pylint: disable=line-too-long
        self.label=rolloutname
        rt.python_rollouts[rolloutname] = self
        controls = "\n".join(map(lambda x: x.string, self.itemlist))
        function_block = "\n".join(list(map(lambda k: f'on {k} do ( python_rollouts["{rolloutname}"].events["{k}"] () )', self.events)))
        #named_args = "  ".join(list(map(lambda k: f"{k}:{kwargs[k]}", kwargs)))
        mxs_string = f'rollout {rolloutname} "{self.label}" ( {controls} {function_block} )'
        print(mxs_string)
        rt.execute(mxs_string)

    def on (self, eventname, handler):
        """Add an event"""
        self.events[eventname] = handler

    def items(self, *args):
        """Add an item"""
        self.itemlist.extend(args)
