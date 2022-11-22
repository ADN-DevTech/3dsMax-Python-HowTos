"""
This module processes the MAXScript syntax tree so that things
become possible in python:

- MXSExpr that are used for their values are converted to expr in the python world
- The last line of all functions is converted to an expr
- The last line of functions is converted to a return statement
"""
# pylint: disable=invalid-name,line-too-long,too-many-lines
from mxs2py import syntax
from mxs2py.log import eprint

# Maybe (or maybe not, we can emit vardecl when we create subfonctions for all
# nonlocal and global variables)
#class FnScope:
#    """ We want the list of all variables and their scopes in all functions"""

class TreeItem():
    """
    Iterated item in the syntax tree
    """
    def __init__(self, construct, parent_item=None, arg_index=None, array_index = None):
        self.construct = construct
        self.parent_item = parent_item
        self.arg_index = arg_index
        self.array_index = array_index

    def is_construct(self):
        """Check if the syntax tree item is a Construct"""
        return isinstance(self.construct, syntax.Construct)

    def __str__(self):
        """Convert to string"""
        return str(self.construct)

    def replace_construct(self, c):
        """Replace this item's construct"""
        if self.array_index is not None:
            self.parent_item.construct.args[self.arg_index][self.array_index] = c
        elif self.arg_index is not None:
            self.parent_item.construct.args[self.arg_index] = c
        else:
            raise ValueError("Invalid parent")

    def append_construct(self, c):
        """Append a construct after this one"""
        if self.array_index is not None:
            self.parent_item.construct.args[self.arg_index].insert(self.array_index + 1, c)
        else:
            raise ValueError("Invalid parent")

def iterate_item(tree_item):
    """Iterate below tree_itemi strting by the children, then this item"""
    if not tree_item.is_construct():
        return
    for index, arg in enumerate(tree_item.construct.args):
        if isinstance(arg, syntax.Construct):
            yield from iterate_item(TreeItem(arg, tree_item, index))
        elif isinstance(arg, list):
            for i, litem in enumerate(arg):
                yield from iterate_item(TreeItem(litem, tree_item, index, i))
    yield tree_item

def iterate_item_bfs(tree_item):
    """Iterate below tree_item starting by this item then the children"""
    if not tree_item.is_construct():
        return
    yield tree_item
    for index, arg in enumerate(tree_item.construct.args):
        if isinstance(arg, syntax.Construct):
            yield from iterate_item_bfs(TreeItem(arg, tree_item, index))
        elif isinstance(arg, list):
            for i, litem in enumerate(arg):
                yield from iterate_item_bfs(TreeItem(litem, tree_item, index, i))

def iterate_parent(tree_item):
    """Iterate, walking the parents of this item"""
    if tree_item is None:
        return
    yield tree_item
    yield from iterate_parent(tree_item.parent_item)

def all(selectors, subitem): #pylint: disable=redefined-builtin
    """Make sure all selectors match"""
    for sel in selectors:
        if isinstance(sel, list):
            passed = False
            for subsel in sel:
                if subsel(subitem):
                    passed = True
                    break
            if not passed:
                return False
        elif not sel(subitem):
            return False
    return True

def query(selectors, tree_item):
    """Query by selectors starting at tree_item"""
    return [ subitem for subitem in iterate_item(tree_item)
        if all(selectors, subitem)]

def query_bfs(selectors, tree_item):
    """Query by selectors starting at tree_item, bfs"""
    return [ subitem for subitem in iterate_item_bfs(tree_item)
        if all(selectors, subitem)]

def query_parent(selectors, tree_item):
    """Query by selectors, climbing int the parents"""
    return [ subitem for subitem in iterate_parent(tree_item)
        if all(selectors, subitem)]

def find_first_parent(selectors, tree_item):
    """Find the first parent matching a bunch of selectors"""
    for subitem in iterate_parent(tree_item):
        if all(selectors, subitem):
            return subitem
    return None

ANY_CONSTRUCT = "_ANY_CONSTRUCT_"
TOP_LEVEL = "_TOP_LEVEL_"

def find_by_layering(item, layers):
    """Find by layering"""
    while len(layers) > 0:
        if item == TOP_LEVEL:
            if layers[0] == TOP_LEVEL or TOP_LEVEL in layers[0]:
                return TOP_LEVEL # < --- this is pretty hacky
            return None
        c = item.construct.construct
        l = layers[0]
        if l == ANY_CONSTRUCT:
            pass
        elif isinstance(l, list):
            if not c in l:
                return None
        elif c != l:
            return None
        layers = layers[1:]
        item = item.parent_item
        if item is None:
            item = TOP_LEVEL
    return item

def filter_by_layering(item, layers):
    """Filter by layering"""
    return find_by_layering(item, layers) is not None

def filter_constructs(constructs):
    """Filter constructs (need to be in the provided list)"""
    def filt(item):
        return item.construct.construct in constructs
    return filt

def filter_and(filters):
    """Filter items that need to match all filters (and multiple filters)"""
    def filt(item):
        for f in filters:
            if not f(item):
                return False
        return True
    return filt

def filter_or(filters):
    """Filter items that need to match some filters (or multiple filters)"""
    def filt(item):
        for f in filters:
            if f(item):
                return True
        return False
    return filt

def filter_all(_):
    """Filter all constructs (keep them all!)"""
    return True

def filter_top_level(item):
    """Filter the top level construct"""
    return item.parent_item is None

def last_program_step(item):
    """Filter the last program step"""
    return ((item.parent_item is not None) and
            item.parent_item.construct.construct == syntax.PROGRAM and
            item.array_index is not None and
            item.array_index == len(item.parent_item.construct.args[0]) -1)

def at_indent_0_from_function_program(item):
    # this is what we need above our head to be in this category
    """Filter at indent 0 of function program"""
    layering = [ANY_CONSTRUCT, syntax.PROGRAM, syntax.EXPR_SEQ, syntax.FUNCTION_DEF]
    return filter_by_layering(item, layering)

def is_function_program(item):
    """Filter is function program"""
    return find_by_layering(
            item,
            [syntax.PROGRAM, [TOP_LEVEL, syntax.EXPR_SEQ], syntax.FUNCTION_DEF]) is not None

def is_program(item):
    """Filter is program"""
    return item.construct.construct == syntax.PROGRAM

PYTHON_EXPR = [
            syntax.ARRAY,
            syntax.BITARRAY,
            syntax.CALL,
            syntax.COMPUTATION,
            syntax.VAR_NAME,
            syntax.MAX_COMMAND,
            syntax.NAME,
            syntax.NUMBER,
            syntax.PATH_NAME,
            syntax.POINT2,
            syntax.POINT3,
            syntax.PROPERTY,
            syntax.STRING ]

is_python_expr = filter_constructs(PYTHON_EXPR)

is_computation = filter_constructs([syntax.COMPUTATION])

is_try_expr = filter_constructs([syntax.TRY_EXPR])

is_if_expr = filter_constructs([syntax.IF_EXPR])

def is_layering(layering):
    """A filter that deos filter_by_layering"""
    def filt(item):
        return filter_by_layering(item, layering)
    return filt

def is_used_as_statement(item):
    """Filter someting tat is used as a statement"""
    # this is what we need above our head to be in this category
    layering = [
            ANY_CONSTRUCT,
            syntax.PROGRAM
            ]

    return filter_by_layering(item, layering)

def is_used_as_expression(item):
    """Filter someting tat is used as an expression"""
    # note: this is not accurate because of the last statement of a program
    # but intended
    return not is_used_as_statement(item)

def return_last_function_value(topconstruct):
    """(processing) make the last value of a function be returned"""
    items = query([
            is_python_expr,
            at_indent_0_from_function_program,
            last_program_step
        ], TreeItem(topconstruct))
    # for each of these items we want to wrap them in a return
    for item in items:
        item.replace_construct(
            syntax.Construct(syntax.FUNCTION_RETURN, item.construct))

def return_last_function_assignment(topconstruct):
    """(processing) makes the last assignement of a function be returned"""
    items = query([
            is_layering([syntax.ASSIGNMENT]),
            at_indent_0_from_function_program,
            last_program_step
        ], TreeItem(topconstruct))
    for item in items:
        # special case of returning a PY_TUPLE
        if item.construct.args[0].construct == syntax.PY_TUPLE:
            # if the first element of the tuple is a no var (_) replace it by a ret
            retprop = item.construct.args[0].args[0][0]
            if retprop.construct == syntax.PY_NOVAR:
                retprop = syntax.Construct(syntax.VAR_NAME, "_ret")
                retprop.resolution = RESOLUTION_NAKED
                item.construct.args[0].args[0][0] = retprop
            item.append_construct(
                syntax.Construct(syntax.FUNCTION_RETURN, retprop))

        else:
            assigned_varname = item.construct.args[0].args[0]
            # does not work for paths
            if assigned_varname.construct == syntax.VAR_NAME:
                assigned_string = assigned_varname.args[0]
                prop = syntax.Construct(syntax.VAR_NAME, assigned_string)
                prop.resolution = assigned_varname.resolution
                item.append_construct(
                    syntax.Construct(syntax.FUNCTION_RETURN, prop))

def replace_op_by_call(construct, opname, call, call_id_construct):
    """Damn"""
    def replace(ops_and_operands):
        selection = filter(
            lambda iop: iop[1].construct == syntax.OPERATOR and iop[1].args[0] == opname,
            enumerate(ops_and_operands))

        l = []
        prev = 0
        for i, _ in selection:
            l = (l + ops_and_operands[prev: i-1] +
                    [syntax.Construct(
                        syntax.CALL,
                        syntax.Construct(call_id_construct, call),
                        [ops_and_operands[i-1], ops_and_operands[i+1]])])
            prev = i + 2

        l = l + ops_and_operands[prev:]
        return l
    if construct.construct == syntax.COMPUTATION:
        construct.args = (replace(construct.args[0]),)

def return_last_block_step(topitem):
    """Damn"""
    cnstr = topitem.construct
    if cnstr.construct == syntax.EXPR_SEQ:
        cnstr = cnstr.args[0]
    if cnstr.construct == syntax.PROGRAM:
        steplist = cnstr.args[0]
        # we could add a return None to an empty steplist but
        # otherwise we will do "pass" and it does the same thing
        if len(steplist) > 0:
            last = steplist[-1]
            if last.construct != syntax.FUNCTION_RETURN:
                ret = syntax.Construct(syntax.FUNCTION_RETURN, last)
                steplist[-1] = ret
    # there are plenty of cases where the construct is one thing
    # and is returnable
    elif cnstr.construct in PYTHON_EXPR:
        topitem.replace_construct(syntax.Construct(syntax.FUNCTION_RETURN, cnstr))

def replace_operators_by_calls(topconstruct, opname, call, call_id_construct):
    """Replace multiple operators by calls"""
    # find all computations
    for computation in query([is_computation], TreeItem(topconstruct)):
        replace_op_by_call(computation.construct, opname, call, call_id_construct)

# if trycatch is not used at the root level of a program, its value
# is needed, so it needs to be transformed to an expression
def replace_non_program_trycatch(topconstruct):
    """Hardcore"""
    def replace(n, trycatchitem):
        trycatchconstruct = trycatchitem.construct
        new_func_name = f"try_catch_fn_{n}"
        # construct the try catch function
        prepended_declarations = declare_assigned_locals_as_nonlocal(trycatchitem.construct)
        prog = syntax.Construct(
                syntax.PROGRAM,
                list(prepended_declarations) + [trycatchitem.construct])
        eseq = syntax.Construct(syntax.EXPR_SEQ, prog)
        funcname = syntax.Construct(syntax.VAR_NAME, new_func_name)
        funcname.resolution = RESOLUTION_NAKED
        func = syntax.Construct(syntax.FUNCTION_DEF, funcname, [], eseq)
        # make sure that the last line of the try catch function's trycatch
        # return their value
        return_last_block_step(TreeItem(trycatchconstruct.args[0], trycatchitem, 0))
        return_last_block_step(TreeItem(trycatchconstruct.args[1], trycatchitem, 1))

        # recursively run substitutions of the generated function
        # (this may not even be needed because we go bottom up... not too sure)

        # add the created function to the outer function
        function_program = find_first_parent([is_function_program], trycatchitem)
        function_program_construct = function_program.construct
        function_program_construct.args[0].insert(0, func)

        # replace the trycatch item by A CALL to the the new func
        fn = syntax.Construct(syntax.VAR_NAME, new_func_name)
        fn.resolution = RESOLUTION_NAKED
        call = syntax.Construct(syntax.CALL, fn, ())
        trycatchitem.replace_construct(call)

    # the last lines of funtion programs can be handled differently: we simply
    # return all branches of the try-cacth
    for trycatch in query([
            is_try_expr,
            at_indent_0_from_function_program,
            last_program_step
            ], TreeItem(topconstruct)):
        tcconstruct = trycatch.construct
        return_last_block_step(TreeItem(tcconstruct.args[0], trycatch, 0))
        return_last_block_step(TreeItem(tcconstruct.args[1], trycatch, 1))

    # for the more complex case of try cach in the middle of expressions, we
    # need to replace them by function calls
    for n, trycatch in enumerate(
            query([is_try_expr,
            is_used_as_expression],
            TreeItem(topconstruct))):
        replace(n, trycatch)

# if ifexpr is not used at the root level of a program, its value
# is needed, so it needs to be transformed to an expression
def replace_non_program_ifexpr(topconstruct):
    """Hardcore, ifexpr replacement by function"""
    def replace(n, ifexpritem):
        ifexprconstruct = ifexpritem.construct
        new_func_name = f"if_expr_fn_{n}"
        # construct the try catch function
        prepended_declarations = declare_assigned_locals_as_nonlocal(ifexpritem.construct)
        prog = syntax.Construct(
                syntax.PROGRAM,
                list(prepended_declarations) + [ifexpritem.construct])
        eseq = syntax.Construct(syntax.EXPR_SEQ, prog)
        funcname = syntax.Construct(syntax.VAR_NAME, new_func_name)
        funcname.resolution = RESOLUTION_NAKED
        func = syntax.Construct(syntax.FUNCTION_DEF, funcname, [], eseq)
        # make sure that the last line of the try catch function's ifexpr
        # return their value
        return_last_block_step(TreeItem(ifexprconstruct.args[1], ifexpritem, 1))
        if ifexprconstruct.args[2] is not None:
            return_last_block_step(TreeItem(ifexprconstruct.args[2], ifexpritem, 2))

        # recursively run substitutions of the generated function
        # (this may not even be needed because we go bottom up... not too sure)

        # add the created function to the outer function
        function_program = find_first_parent([is_function_program], ifexpritem)
        function_program_construct = function_program.construct
        function_program_construct.args[0].insert(0, func)

        # replace the ifexpr item by A CALL to the the new func
        fn = syntax.Construct(syntax.VAR_NAME, new_func_name)
        fn.resolution = RESOLUTION_NAKED
        call = syntax.Construct(syntax.CALL, fn, ())
        ifexpritem.replace_construct(call)

    # the last lines of funtion programs can be handled differently: we simply
    # return all branches of the try-cacth
    for ifexpr in query([
            is_if_expr,
            at_indent_0_from_function_program,
            last_program_step
            ], TreeItem(topconstruct)):
        tcconstruct = ifexpr.construct
        return_last_block_step(TreeItem(tcconstruct.args[1], ifexpr, 1))
        if tcconstruct.args[2] is not None:
            return_last_block_step(TreeItem(tcconstruct.args[2], ifexpr, 2))

    # for the more complex case of try cach in the middle of expressions, we
    # need to replace them by function calls
    for n, ifexpr in enumerate(query([is_if_expr, is_used_as_expression], TreeItem(topconstruct))):
        eprint(f">>> {is_used_as_expression(ifexpr)} <<<< {ifexpr.construct.construct}")
        eprint(f"{ ifexpr.parent_item.construct.construct }")
        eprint(f"{is_used_as_statement(ifexpr)}")
        eprint(f"{is_layering([ANY_CONSTRUCT])(ifexpr)}")
        eprint(f"{is_layering([ANY_CONSTRUCT, syntax.PROGRAM])(ifexpr)}")
        replace(n, ifexpr)


def lowercase_names(topconstruct):
    """replace all names by lowercase (mxs is case insensitive, keep things consistent)"""
    for vn  in query([is_layering([syntax.VAR_NAME])], TreeItem(topconstruct)):
        vn.construct.args[0] = vn.construct.args[0].lower()

def declare_assigned_locals_as_nonlocal(topconstruct: syntax.Construct):
    """
    This is meant to be called on a subtree that we want to wrap in a local function
    """
    def declare_modifiable(item):
        def create_declaration(decl_construct, vname):
            eprint(f" vname -------------------------- {vname.args[0]}")
            return syntax.Construct(
                decl_construct,
                vname.args[0])

        construct = item.construct
        prop = construct.args[0]
        propname = prop.args[0]
        scopeset = construct.scopeset
        # if the variable resolves to the global or local scope we need
        # to locally declare it as global or locally declare it as
        # non local
        scope = scopeset.get_scope(propname)
        if scope.stype == SCOPE_GLOBAL:
            return create_declaration(syntax.PY_GLOBAL, propname)
        if scope.stype in [SCOPE_FUNCTION, SCOPE_METHOD]:
            return create_declaration(syntax.PY_NONLOCAL, propname)

    to_be_added = filter(
            lambda x : x is not None,
            map(declare_modifiable,
                query([is_layering([syntax.ASSIGNMENT])], TreeItem(topconstruct))))

    return to_be_added

#There are 3 notions here:
#- The ScopeSet (could be call ScopeEnvironment): which contains the many existing
#scopes at a given time. The content of the scopeset makes it 100% clear where we
#are in the scope (if there is a struct scope but no local scope we are in the
#struct def)
#
#- The Scope (one given element of the ScopeSet) contains the variable names that
#exist in that scope
#
#
#When we se a given var_name in the code it's just a name. Based on the "ScopeSet"
#the var_name and maybe the language construct the variable can be assigned a
#Resolution (how to address it)
#
#For example if someone does :
#local <var_name> = 2
#var_name needs to remain resolved to the local scope because it's a var decl.
#It only serves as a name in this context. So if a variable already has a resolution
#when it is further processed down the tree it needs to keep this resolution.
#
#The only possible resolutions are:
#
#RESOLUTION_RT =0
#RESOLUTION_SELF = 1
#RESOLUTION_NAKED = 2
#RESOLUTION_INVALID = 3
#
#but... to support code relocation we may need something else (not sure)`
#
#

# this is a scope (pool of variable names)
SCOPE_MXSGLOBAL = 0
SCOPE_GLOBAL = 1
SCOPE_FUNCTION = 2
SCOPE_STRUCT = 3
SCOPE_METHOD = 4

# this is the decoration to put to a variable name
RESOLUTION_RT = 0
RESOLUTION_SELF = 1
RESOLUTION_NAKED = 2
RESOLUTION_INVALID = 3

IN_GLOBAL_CODE_TO_RESOLUTION = {
    SCOPE_MXSGLOBAL: RESOLUTION_RT,
    SCOPE_GLOBAL: RESOLUTION_NAKED,

    SCOPE_FUNCTION: RESOLUTION_INVALID,
    SCOPE_STRUCT: RESOLUTION_INVALID,
    SCOPE_METHOD: RESOLUTION_INVALID
}
IN_STRUCT_CODE_TO_RESOLUTION = {
    SCOPE_MXSGLOBAL: RESOLUTION_RT,
    SCOPE_GLOBAL: RESOLUTION_NAKED,

    SCOPE_FUNCTION: RESOLUTION_INVALID,
    SCOPE_STRUCT: RESOLUTION_NAKED,
    SCOPE_METHOD: RESOLUTION_INVALID
}
IN_METHOD_CODE_TO_RESOLUTION = {
    SCOPE_MXSGLOBAL: RESOLUTION_RT,
    SCOPE_GLOBAL: RESOLUTION_NAKED,

    SCOPE_FUNCTION: RESOLUTION_INVALID,
    SCOPE_STRUCT: RESOLUTION_SELF,
    SCOPE_METHOD: RESOLUTION_NAKED
}
IN_FUNCTION_CODE_TO_RESOLUTION = {
    SCOPE_MXSGLOBAL: RESOLUTION_RT,
    SCOPE_GLOBAL: RESOLUTION_NAKED,

    SCOPE_FUNCTION: RESOLUTION_NAKED,
    SCOPE_STRUCT: RESOLUTION_INVALID,
    SCOPE_METHOD: RESOLUTION_INVALID
}
class Scope:
    #pylint: disable=too-few-public-methods
    """A scope that can contain multipe variable names"""
    def __init__(self, stype=SCOPE_FUNCTION, outer = None):
        """Init the scope"""
        self.stype = stype
        self.dict = {}
        # loop scopes can have an outer scope (the function scope)
        self.outer = outer
    def set(self, name:str):
        """Set a variable inside the scope"""
        self.dict[name] = True

class ScopeSet:
    #pylint: disable=too-many-public-methods
    """A scopeset that contains all the scopes that we track at a given moment"""
    def __init__(self, gscope = None, lscope = None, sscope = None, mscope = None):
        if gscope is None:
            gscope = Scope(SCOPE_GLOBAL)
        self.gscope = gscope
        self.lscope = lscope
        # method scope (the reason for this is that you could define a struct inside a function)
        self.mscope = mscope
        self.sscope = sscope
        # this is the list of names that when not scoped should always be rt
        self.ALWAYS_RESOLVE_RT = [ "subobjectlevel" ]


    def get_scope(self, namec: syntax.Construct ):
        """Get the scope of a name construct"""
        if namec.construct != syntax.VAR_NAME:
            raise Exception(f"Invalid arg {namec.construct} {namec.args[0]}")
        name = namec.args[0]
        if self.sscope is not None and name in self.sscope.dict:
            return self.sscope
        if self.mscope is not None and name in self.mscope.dict:
            return self.mscope
        # at this point, it cannot be a method
        if self.lscope is not None and name in self.lscope.dict:
            return self.lscope
        if self.gscope is not None and name in self.gscope.dict:
            return self.gscope
        return None

    def in_global_code(self):
        """Is the current scope the global scope"""
        return self.sscope is None and self.lscope is None
    def in_struct_code(self):
        """Is the current scope struct scope"""
        return self.mscope is None and self.sscope is not None
    def in_method_code(self):
        """Is the current scope method scope"""
        return self.mscope is not None
    def in_function_code(self):
        """Is the current scope function scope"""
        return self.lscope is not None and self.sscope is None

    def get_default_declaration_scope(self):
        """Return the scope to use for declaring variables"""
        if self.in_global_code():
            return self.gscope
        if self.in_struct_code():
            return self.sscope
        if self.in_method_code():
            return self.mscope
        if self.in_function_code():
            return self.lscope
        raise Exception("to be refined")

    def get_method_or_function_or_global_scope(self):
        """Return method function or global scope"""
        if self.mscope is not None:
            return self.mscope
        if self.lscope is not None:
            return self.lscope
        # not in a function of any kind? must be in the global scope
        return self.gscope

    def resolve_to(self, v: syntax.Construct, resolution):
        """Assign the resolution of a variable to a scope (where it belongs)
        (the resolution being naked, rt, self, etc..., )"""
        if not hasattr(v, "resolution"):
            v.resolution = resolution

    def resolve_to_scope(self, v : syntax.Construct, scope: Scope) -> None :
        """Resolve a variable to a scope
        (the resolution being naked, rt, self, etc...)"""
        if self.in_global_code():
            resolution = IN_GLOBAL_CODE_TO_RESOLUTION[scope.stype]
        elif self.in_struct_code():
            resolution = IN_STRUCT_CODE_TO_RESOLUTION[scope.stype]
        elif self.in_method_code():
            resolution = IN_METHOD_CODE_TO_RESOLUTION[scope.stype]
        else:
            resolution = IN_FUNCTION_CODE_TO_RESOLUTION[scope.stype]
        self.resolve_to(v, resolution)

    def resolve(self, v: syntax.Construct) -> None:
        """Resolve a variable to its scope
        (the resolution being naked, rt, self, etc
        and the scope being the bucket of variables where it has been defined)"""
        scope = self.get_scope(v)
        if scope is not None:
            return self.resolve_to_scope(v, scope)
        return self.resolve_to(v, RESOLUTION_RT)

    def assign_variable(self, v: syntax.Construct, is_nested: bool):
        """Set the scope and resolution of a variable given that it is being
        assigned"""
        scope = self.get_scope(v)
        if scope is None:
            # this means that we assign to a mxs scope variable
            if is_nested or v.args[0][0:2] == "::" or v.args[0] in self.ALWAYS_RESOLVE_RT:
                v.resolution = RESOLUTION_RT
            else:
                self.declare_variable(v)
            return
        # there is no impact on scopes if the variable already exists
        # but we should set the resolution of the current variable
        self.resolve_to_scope(v, scope)

    def declare_variable(self, v):
        """Set the scope and resolution of a variable given that it is being
        declared"""
        scope = self.get_default_declaration_scope()
        scope.set(v.args[0])
        self.resolve_to(v, RESOLUTION_NAKED)

    def declare_struct_variable(self, v):
        """Declare a struct variable, setting its scope and resolution"""
        scope = self.sscope
        scope.set(v.args[0])
        self.resolve_to(v, RESOLUTION_NAKED)

    def declare_global_variable(self, v):
        """Declare a global variable, setting its scope and resolution"""
        scope = self.gscope
        scope.set(v.args[0])
        self.resolve_to(v, RESOLUTION_NAKED)

    def declare_local_variable(self, v):
        """Declare a local variable, setting its scope and resolution"""
        scope = self.get_method_or_function_or_global_scope()
        scope.set(v.args[0])
        self.resolve_to(v, RESOLUTION_NAKED)

    def declare_persistent_global_variable(self, v):
        """Declare a persistent global (mxs!!!) variable, setting its scope and resolution"""
        scope = self.gscope
        scope.set(v.args[0])
        self.resolve_to(v, RESOLUTION_NAKED)

    def add_loop_variable(self, v):
        """Declare a loop variable, setting its scope and resolution"""
        scope = self.get_method_or_function_or_global_scope()
        scope.set(v)
        self.resolve_to(v, RESOLUTION_NAKED)

    def declare_struct(self, v):
        """Declare a struct variable, setting its scope and resolution"""
        scope = self.get_default_declaration_scope()
        scope.set(v.args[0])
        self.resolve_to(v, RESOLUTION_NAKED)

    def declare_function(self, v):
        """Declare a function setting its scope and resolution"""
        scope = self.get_default_declaration_scope()
        scope.set(v.args[0])
        self.resolve_to(v, RESOLUTION_NAKED)

    def declare_function_parameter(self, v):
        """Declare a function parameter, setting its scope and resolution"""
        scope = self.get_default_declaration_scope()
        scope.set(v.args[0])
        self.resolve_to(v, RESOLUTION_NAKED)

    def use_variable(self, v):
        """Declare the usage of a variable, setting its scope and resolution"""
        self.resolve(v)

def annotate_scopes(topconstruct):
    """Transform the syntax tree from a topconstruct so that all variables are
    scoped and resolved"""
    #pylint: disable=too-many-branches, too-many-statements
    global_scopeset = ScopeSet()
    scopeset = global_scopeset
    for vn in iterate_item_bfs(TreeItem(topconstruct)):
        cn = vn.construct.construct
        eprint(f"{cn} ")
        # set the default scopeset (inherited from parent item)
        if vn.parent_item is None:
            vn.scopeset = global_scopeset
        else:
            vn.scopeset = vn.parent_item.scopeset
        scopeset = vn.scopeset

        if cn == syntax.STRUCT_DEF:
            # declare the name of the struct in the current scope
            vn.scopeset.declare_struct(vn.construct.args[0])
            # push a new scope
            scopeset = ScopeSet(scopeset.gscope, None, Scope(SCOPE_STRUCT), None)
            vn.scopeset = scopeset
        elif cn == syntax.STRUCT_MEMBER_ASSIGN:
            scopeset.declare_variable(vn.construct.args[0])
            # the right part should be seen as in a method scope
            # (this will be rendered in the constructor)
            vn.scopeset = ScopeSet(scopeset.gscope, None, scopeset.sscope, Scope(SCOPE_METHOD))

        elif cn == syntax.STRUCT_MEMBER_DATA:
            scopeset.declare_variable(vn.construct.args[0])
        #elif cn == syntax.STRUCT_MEMBER_METHOD:
            #scopeset.resolve_to_scope(vn.construct.args[0], scopeset.sscope)
        elif cn == syntax.FUNCTION_DEF:
            # put the name of the function in the current scopeset
            scopeset.declare_function(vn.construct.args[0])

            if scopeset.in_struct_code():
                # create a method scope
                scopeset = ScopeSet(scopeset.gscope, None, scopeset.sscope, Scope(SCOPE_METHOD))
            else:
                scopeset = ScopeSet(scopeset.gscope, Scope(SCOPE_FUNCTION), None, None)

            vn.scopeset = scopeset
            # all the function args need to go in the function scope
            for arg in vn.construct.args[1]:
                scopeset.declare_function_parameter(arg.args[0])
        elif cn == syntax.NAMED_ARGUMENT:
            scopeset.resolve_to(vn.construct.args[0], RESOLUTION_NAKED)
        elif cn == syntax.ASSIGNMENT:
            # property -> var_name
            to_assign = vn.construct.args[0].args[0]
            is_nested = vn.construct.args[0].args[1] is not None
            # note can also be a pathname (which does not need scoping)
            if to_assign.construct == syntax.VAR_NAME:
                scopeset.assign_variable(to_assign, is_nested)
            # for assignments, keep the scopeset, we use this for transforming
            # expressions to functions
            vn.construct.scopeset = scopeset

        elif cn == syntax.VARIABLE_DECL:
            declare_scope = vn.construct.args[0]
            decls = vn.construct.args[1]
            if declare_scope is None:
                for decl in decls:
                    scopeset.declare_variable(decl.args[0])
            elif declare_scope.construct == syntax.GLOBAL:
                for decl in decls:
                    scopeset.declare_global_variable(decl.args[0])
            elif declare_scope.construct == syntax.LOCAL:
                for decl in decls:
                    scopeset.declare_local_variable(decl.args[0])
            elif declare_scope.construct == syntax.PERSISTENTGLOBAL:
                for decl in decls:
                    scopeset.declare_persistent_global_variable(decl.args[0])
            else:
                raise Exception("Unexpected decl var scope")

        elif cn == syntax.ON_DO_HANDLER:
            # push a method scope
            scopeset = ScopeSet(scopeset.gscope, None, scopeset.sscope, Scope(SCOPE_METHOD))
            vn.scopeset = scopeset

        elif cn == syntax.LOCAL_DECL:
            decls = vn.construct.args[0]
            for decl in decls:
                scopeset.declare_struct_variable(decl.args[0])

        elif cn == syntax.FOR_LOOP:
            # put all vars in the local scope
            # (in reality, we would need a loop scope, not supported yet)
            for v in vn.construct.args[0]:
                scopeset.declare_function_parameter(v)

        elif cn == syntax.REFERENCE:
            # if there is not indexing
            # the referenced variable must be local
            referenced = vn.construct.args[0]
            if referenced.args[1] is None:
                # -- we want to know if the referenced variable
                # -- has already been declared in the current declaration scope
                # -- if not we want to do as if it was and makr it for local declaration
                if scopeset.get_scope(referenced.args[0]) != scopeset.get_default_declaration_scope():
                    scopeset.declare_variable(referenced.args[0])
                    # this is a bit hacky, because processed in
                    # a later stage (local declaration of byref variables)
                    referenced.args[0].mark_for_local_declaration = True



        elif cn == syntax.MACROSCRIPT_DEF:
            vn.construct.args[0].resolution = RESOLUTION_NAKED

        elif cn == syntax.MACROSCRIPT_CLAUSE:
            # push a new scope and use a struct scope
            scopeset = ScopeSet(scopeset.gscope, None, Scope(SCOPE_STRUCT), None)
            vn.scopeset = scopeset

        elif cn == syntax.ROLLOUT_DEF:
            vn.construct.args[0].resolution = RESOLUTION_NAKED

        elif cn == syntax.ROLLOUT_CLAUSE:
            # push a new scope and use a struct scope
            scopeset = ScopeSet(scopeset.gscope, None, Scope(SCOPE_STRUCT), None)
            vn.scopeset = scopeset

        elif cn == syntax.PLUGIN_DEF:
            vn.construct.args[0].resolution = RESOLUTION_NAKED
            # then we push a new scope for the plugin. Why
            # not do it like that for rollouts and macroscripts?
            scopeset = ScopeSet(scopeset.gscope, None, Scope(SCOPE_STRUCT), None)
            vn.scopeset = scopeset

        elif cn == syntax.ATTRIBUTES_DEF:
            vn.construct.args[0].resolution = RESOLUTION_NAKED
            # then we push a new scope for the plugin. Why
            # not do it like that for rollouts and macroscripts?
            scopeset = ScopeSet(scopeset.gscope, None, Scope(SCOPE_STRUCT), None)
            vn.scopeset = scopeset

        elif cn == syntax.MAX_COMMAND:
            items = vn.construct.args[0]
            for it in items:
                if it.construct == syntax.VAR_NAME:
                    scopeset.resolve_to(it, RESOLUTION_NAKED)

        elif cn == syntax.PROPERTY_ACCESSOR_MEMBER:
            vn.construct.args[0].resolution = RESOLUTION_NAKED

        elif cn == syntax.VAR_NAME:
            scopeset.use_variable(vn.construct)
            # note: because of the :: that cannot be found in the
            # scopes that we track, the presence of :: will always resolve
            # the variable in the mxs global scope which is what we want
            # BUT: we strip the :: from the name
            vn.construct.args[0] = vn.construct.args[0].replace("::", "")

def substitute_macroscripts(topconstruct):
    """Process the syntax tree to subsitute macrosscripts with python constructs"""
    #pylint: disable=too-many-locals
    def generate_method(namecode):
        event_name, code = namecode
        method_name = syntax.Construct(syntax.VAR_NAME, event_name.args[0])
        method_name.resolution = RESOLUTION_NAKED
        fcn = syntax.Construct(syntax.FUNCTION_DEF, method_name, [], code)
        method = syntax.Construct(syntax.STRUCT_MEMBER_METHOD, fcn)
        return method

    def generate_handler_method(ondohandler):
        return generate_method(ondohandler.args)

    for _, macro_script_it in enumerate(
            query(
                [is_layering([syntax.MACROSCRIPT_DEF])],
                TreeItem(topconstruct))
            ):
        macro_script = macro_script_it.construct
        vname = macro_script.args[0]
        vnop = macro_script.args[1]
        exprseq = macro_script.args[2]
        # we need the upper "program" construct for inserting
        # statements

        # create a class for the macroscript
        sname = f"MacroScript_{vname.args[0]}"
        snamec = syntax.Construct(syntax.VAR_NAME, sname)
        snamec.resolution = RESOLUTION_NAKED

        if exprseq.construct == syntax.EXPR_SEQ:
            mname = syntax.Construct(syntax.VAR_NAME, "execute")
            mname.resolution = RESOLUTION_NAKED
            other_decls = []
            event_members = list(map(generate_method, [(mname, exprseq)]))
            events = ["execute"]
        else:
            clause_items = exprseq.args[0]
            on_do_handlers = list(filter(lambda c: c.construct == syntax.ON_DO_HANDLER, clause_items))
            other_decls = list(filter(lambda c: c.construct != syntax.ON_DO_HANDLER, clause_items))
            event_members = list(map(generate_handler_method, on_do_handlers))
            events = list(map(lambda c: c.args[0].args[0], on_do_handlers))
        #decl_class = syntax.Construct(syntax.STRUCT_DEF, snamec, members)

        decl_class = syntax.Construct(syntax.PY_MACROSCRIPT_CLASS, snamec, vname, event_members, events, other_decls)

        # and substitute the MASCROSCRIPT_DEF by a call to the struct
        # constructor
        snamec = syntax.Construct(syntax.VAR_NAME, sname)
        snamec.resolution = RESOLUTION_NAKED
        cnstr_call = syntax.Construct(syntax.CALL, snamec, vnop)
        macro_script_it.replace_construct(cnstr_call)

        # we now want to add this class declaration in the top level of the
        # program
        # (note: we do this after because this breaks indices... could cause other
        # problems?)
        function_program = find_first_parent([is_function_program], macro_script_it)
        function_program_construct = function_program.construct
        function_program_construct.args[0].insert(0, decl_class)

def substitute_rollouts(topconstruct):
    """Process the syntax tree to subsitute rollouts with python constructs"""
    #pylint: disable=too-many-locals
    def generate_method(namecode):
        event_name, code = namecode
        method_name = syntax.Construct(syntax.VAR_NAME, event_name.args[0])
        method_name.resolution = RESOLUTION_NAKED
        fcn = syntax.Construct(syntax.FUNCTION_DEF, method_name, [], code)
        method = syntax.Construct(syntax.STRUCT_MEMBER_METHOD, fcn)
        return method

    def generate_handler_method(ondohandler):
        return generate_method(ondohandler.args)
    for _, rollout_it in enumerate(
            query(
                [is_layering([syntax.ROLLOUT_DEF])],
                TreeItem(topconstruct))
            ):
        rollout = rollout_it.construct
        vname = rollout.args[0]
        label = rollout.args[1]
        #vnop = rollout.args[2]
        clauses = rollout.args[3]
        # we need the upper "program" construct for inserting
        # statements

        # create a class for the macroscript
        sname = f"Rollout_{vname.args[0]}"
        snamec = syntax.Construct(syntax.VAR_NAME, sname)
        snamec.resolution = RESOLUTION_NAKED

        # vname is really a name that we give to the rollout
        vname.resolution = RESOLUTION_NAKED

        rollout_items = list(filter(lambda c: c.construct == syntax.ROLLOUT_ITEM, clauses))
        on_do_handlers = list(filter(lambda c: c.construct == syntax.ON_DO_HANDLER, clauses))
        other_decls = list(filter(lambda c: c.construct != syntax.ON_DO_HANDLER, clauses))
        event_members = list(map(generate_handler_method, on_do_handlers))
        events = list(map(lambda c: c.args[0].args[0], on_do_handlers))
        #decl_class = syntax.Construct(syntax.STRUCT_DEF, snamec, members)

        decl_class = syntax.Construct(syntax.PY_ROLLOUT_CLASS, snamec, vname, label, event_members, events, other_decls, rollout_items)

        # and substitute the ROLLOUT_DEF by a call to the struct
        # constructor
        snamec = syntax.Construct(syntax.VAR_NAME, sname)
        snamec.resolution = RESOLUTION_NAKED
        # ---------- this vnop thing does not work
        cnstr_call = syntax.Construct(syntax.CALL, snamec, []) #vnop) <<<< problem here
        rollout_it.replace_construct(cnstr_call)

        # we now want to add this class declaration in the top level of the
        # program
        # (note: we do this after because this breaks indices... could cause other
        # problems?)
        function_program = find_first_parent([is_function_program], rollout_it)
        function_program_construct = function_program.construct
        function_program_construct.args[0].insert(0, decl_class)

def substitute_plugins(topconstruct):
    """Process the syntax tree to subsitute plugins with python constructs"""
    #pylint: disable=too-many-locals
    def generate_method(namecode):
        event_name, code = namecode
        method_name = syntax.Construct(syntax.VAR_NAME, event_name.args[0])
        method_name.resolution = RESOLUTION_NAKED
        fcn = syntax.Construct(syntax.FUNCTION_DEF, method_name, [], code)
        method = syntax.Construct(syntax.STRUCT_MEMBER_METHOD, fcn)
        return method

    def generate_handler_method(ondohandler):
        return generate_method(ondohandler.args)
    for _, plugin_it in enumerate(
            query(
                [is_layering([syntax.PLUGIN_DEF])],
                TreeItem(topconstruct))
            ):
        plugin = plugin_it.construct
        vname = plugin.args[0]
        label = plugin.args[1]
        #vnop = plugin.args[2]
        clauses = [] #plugin.args[3]
        # we need the upper "program" construct for inserting
        # statements

        # create a class for the macroscript
        sname = f"Plugin_{vname.args[0]}"
        snamec = syntax.Construct(syntax.VAR_NAME, sname)
        snamec.resolution = RESOLUTION_NAKED

        # vname is really a name that we give to the plugin
        vname.resolution = RESOLUTION_NAKED

        plugin_items = list(filter(lambda c: c.construct == syntax.ROLLOUT_ITEM, clauses))
        on_do_handlers = list(filter(lambda c: c.construct == syntax.ON_DO_HANDLER, clauses))
        other_decls = list(filter(lambda c: c.construct != syntax.ON_DO_HANDLER, clauses))
        event_members = list(map(generate_handler_method, on_do_handlers))
        events = list(map(lambda c: c.args[0].args[0], on_do_handlers))
        #decl_class = syntax.Construct(syntax.STRUCT_DEF, snamec, members)

        decl_class = syntax.Construct(syntax.PY_PLUGIN_CLASS, snamec, vname, label, event_members, events, other_decls, plugin_items)

        # and substitute the ROLLOUT_DEF by a call to the struct
        # constructor
        snamec = syntax.Construct(syntax.VAR_NAME, sname)
        snamec.resolution = RESOLUTION_NAKED
        # ---------- this vnop thing does not work
        cnstr_call = syntax.Construct(syntax.CALL, snamec, []) #vnop) <<<< problem here
        plugin_it.replace_construct(cnstr_call)

        # we now want to add this class declaration in the top level of the
        # program
        # (note: we do this after because this breaks indices... could cause other
        # problems?)
        function_program = find_first_parent([is_function_program], plugin_it)
        function_program_construct = function_program.construct
        function_program_construct.args[0].insert(0, decl_class)

def substitute_attributes(topconstruct):
    """Process the syntax tree to subsitute attributes with python constructs"""
    #pylint: disable=too-many-locals
    def generate_method(namecode):
        event_name, code = namecode
        method_name = syntax.Construct(syntax.VAR_NAME, event_name.args[0])
        method_name.resolution = RESOLUTION_NAKED
        fcn = syntax.Construct(syntax.FUNCTION_DEF, method_name, [], code)
        method = syntax.Construct(syntax.STRUCT_MEMBER_METHOD, fcn)
        return method

    def generate_handler_method(ondohandler):
        return generate_method(ondohandler.args)
    for _, plugin_it in enumerate(
            query(
                [is_layering([syntax.ATTRIBUTES_DEF])],
                TreeItem(topconstruct))
            ):
        plugin = plugin_it.construct
        vname = plugin.args[0]
        label = plugin.args[1]
        #vnop = plugin.args[2]
        clauses = [] #plugin.args[3]
        # we need the upper "program" construct for inserting
        # statements

        # create a class for the macroscript
        sname = f"Attributes_{vname.args[0]}"
        snamec = syntax.Construct(syntax.VAR_NAME, sname)
        snamec.resolution = RESOLUTION_NAKED

        # vname is really a name that we give to the plugin
        vname.resolution = RESOLUTION_NAKED

        plugin_items = list(filter(lambda c: c.construct == syntax.ROLLOUT_ITEM, clauses))
        on_do_handlers = list(filter(lambda c: c.construct == syntax.ON_DO_HANDLER, clauses))
        other_decls = list(filter(lambda c: c.construct != syntax.ON_DO_HANDLER, clauses))
        event_members = list(map(generate_handler_method, on_do_handlers))
        events = list(map(lambda c: c.args[0].args[0], on_do_handlers))
        #decl_class = syntax.Construct(syntax.STRUCT_DEF, snamec, members)

        decl_class = syntax.Construct(syntax.PY_PLUGIN_CLASS, snamec, vname, label, event_members, events, other_decls, plugin_items)

        # and substitute the ROLLOUT_DEF by a call to the struct
        # constructor
        snamec = syntax.Construct(syntax.VAR_NAME, sname)
        snamec.resolution = RESOLUTION_NAKED
        # ---------- this vnop thing does not work
        cnstr_call = syntax.Construct(syntax.CALL, snamec, []) #vnop) <<<< problem here
        plugin_it.replace_construct(cnstr_call)

        # we now want to add this class declaration in the top level of the
        # program
        # (note: we do this after because this breaks indices... could cause other
        # problems?)
        function_program = find_first_parent([is_function_program], plugin_it)
        function_program_construct = function_program.construct
        function_program_construct.args[0].insert(0, decl_class)

def flatten_exprseq_outside_computation(topconstruct):
    """Flattens an expr seq"""
    # expr seq are programs with parenthesis and
    # +/- sadly this is how parenthesis in computations end up
    for _, eseq_it in enumerate(
            query(
                #[is_layering([[TOP_LEVEL, syntax.PROGRAM], syntax.EXPR_SEQ])],
                [is_layering([syntax.EXPR_SEQ, syntax.PROGRAM])],
                TreeItem(topconstruct))
            ):
        eseq = eseq_it.construct
        print(f"%%%%%%%%%%%%%%% {eseq}")
        eseq_it.replace_construct(eseq.args[0])

def declare_references(topconstruct):
    """omg"""
    for vn in query([is_layering([syntax.REFERENCE])], TreeItem(topconstruct)):
        referenced = vn.construct.args[0]
        if referenced.construct == syntax.PROPERTY:
            if referenced.args[1] is None:
                # this is a simple "name" thing. if it has been
                # scoped as rt. then well we should instead declare it locally
                varname = referenced.args[0]
                print(varname)
                if hasattr(varname, "mark_for_local_declaration"):
                    program = find_first_parent([is_program], vn)
                    snamec = syntax.Construct(syntax.VAR_NAME, varname.args[0])
                    snamec.resolution = RESOLUTION_NAKED
                    undefc = syntax.Construct(syntax.VAR_NAME, "udefined")
                    undefc.resolution = RESOLUTION_NAKED
                    declc = syntax.Construct(syntax.DECL, snamec, None)
                    program.construct.args[0].insert(0, declc)

def process_call_byref_assign(topconstruct):
    """we are looking for byref calls that are at the toplevel of a program block"""
    for topcalls in query([is_layering([syntax.CALL, syntax.ASSIGNMENT, syntax.PROGRAM])], TreeItem(topconstruct)):
        assignment = topcalls.parent_item
        #c = topcalls.construct
        # -- check the args of this call: do them contain a reference
        # we need to find all the
        refs = query([is_layering([syntax.REFERENCE, syntax.CALL, syntax.ASSIGNMENT, syntax.PROGRAM])], topcalls)
        if len(refs) > 0:
            var_names = list(map(lambda r: r.construct.args[0].args[0], refs))
            var_names.insert(0, assignment.construct.args[0])
            res_tuple = syntax.Construct(syntax.PY_TUPLE, var_names)
            # here we need to create a tuple
            assignment.construct.args[0] = res_tuple

def process_call_byref_noassign(topconstruct):
    """we are looking for assignations from byref calls that are at the toplevel of a program block"""
    for topcalls in query([is_layering([syntax.CALL, syntax.PROGRAM])], TreeItem(topconstruct)):
        c = topcalls.construct
        # -- check the args of this call: do them contain a reference
        # we need to find all the
        refs = query([is_layering([syntax.REFERENCE, syntax.CALL, syntax.PROGRAM])], topcalls)
        if len(refs) > 0:
            var_names = list(map(lambda r: r.construct.args[0].args[0], refs))
            var_names.insert(0, syntax.Construct(syntax.PY_NOVAR))
            res_tuple = syntax.Construct(syntax.PY_TUPLE, var_names)
            assign = syntax.Construct(syntax.ASSIGNMENT, res_tuple, "=", c)
            # here we need to create a tuple
            topcalls.replace_construct(assign)

def preprocess(topconstruct):
    """Apply all pre processing operations to the syntax tree.
    This is not super efficient because we have multiple passes,
    etc... meant to be "simple" rather than performant :)"""
    lowercase_names(topconstruct)
    annotate_scopes(topconstruct)
    # this is probably useless:
    process_call_byref_assign(topconstruct)
    process_call_byref_noassign(topconstruct)
    declare_references(topconstruct)
    substitute_macroscripts(topconstruct)
    substitute_rollouts(topconstruct)
    substitute_plugins(topconstruct)
    substitute_attributes(topconstruct)
    return_last_function_value(topconstruct)
    return_last_function_assignment(topconstruct)
    replace_operators_by_calls(topconstruct, "as", "as_type", syntax.PY_RT_VAR_NAME)
    replace_non_program_trycatch(topconstruct)
    replace_non_program_ifexpr(topconstruct)
    flatten_exprseq_outside_computation(topconstruct)
