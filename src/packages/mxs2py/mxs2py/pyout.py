"""
Formats the processed syntax tree as python code.
"""
# pylint: disable=invalid-name, import-error, too-many-lines, fixme, unused-argument
import keyword
import functools
import mxs2py.syntax as s
import mxs2py.limitations as lim
from mxs2py import mxscp
from mxs2py import pytreeprocess
from mxs2py.log import eprint

SCOPE_PREFIX = {
        pytreeprocess.RESOLUTION_RT: "rt.",
        pytreeprocess.RESOLUTION_SELF: "self.",
        pytreeprocess.RESOLUTION_NAKED: "",
        pytreeprocess.RESOLUTION_INVALID: "????????????????."
    }

RESERVED_PYTHON_NAMES = keyword.kwlist + ["str"]

#pylint: disable=too-many-public-methods
class PythonFormatter():
    """
    Converts all syntax constructs in the syntax tree to python code.
    """
    def __init__(self, comments):
        """
        Constructs the PythonFormatter.
        """
        self.SWITCH = {
            s.ARRAY: self.out_array,
            s.ASSIGNMENT: self.out_assignment,
            s.BITARRAY: self.out_bitarray,
            s.BITARRAY_RANGE: self.out_bitarray_range,
            s.CALL: self.out_call,
            s.CASE_EXPR: self.out_case_expr,
            s.CASE_ITEM: self.out_case_item,
            s.COMPUTATION: self.out_computation,
            s.CONTEXT_AT: self.out_context_at,
            s.CONTEXT_EXPR: self.out_context_expr,
            s.CONTEXT_IN_COORDSYS: self.out_context_in_coordsys,
            s.CONTEXT_IN_NODE: self.out_context_in_node,
            s.CONTEXT_WITH: self.out_context_with,
            s.CONTEXT_ABOUT: self.out_context_about,
            s.DECL: self.out_decl,
            s.DO_LOOP: self.out_do_loop,
            s.FOR_LOOP: self.out_for_loop,
            s.FOR_LOOP_FROM_TO_SEQUENCE: self.out_for_loop_from_to_sequence,
            s.FUNCTION_DEF: self.out_function_def,
            s.FUNCTION_RETURN: self.out_function_return,
            s.VAR_NAME: self.out_var_name,
            s.IF_EXPR: self.out_if_expr,
            s.LOOP_CONTINUE: self.out_loop_continue,
            s.LOOP_EXIT: self.out_loop_exit,
            s.MAX_COMMAND: self.out_max_command,
            s.NAME: self.out_name,
            s.ARGUMENT: self.out_argument,
            s.NAMED_ARGUMENT: self.out_named_argument,
            s.NUMBER: self.out_number,
            s.ON_DO_HANDLER: self.out_on_do_handler,
            s.ON_MAP_DO_HANDLER: self.out_on_map_do_handler,
            s.OPERATOR: self.out_operator,
            s.PATH_NAME: self.out_path_name,
            s.POINT2: self.out_point2,
            s.POINT3: self.out_point3,
            s.POINT4: self.out_point4,
            s.PROGRAM: self.out_program,
            s.PROPERTY: self.out_property,
            s.PROPERTY_ACCESSOR_INDEX: self.out_property_accessor_index,
            s.PROPERTY_ACCESSOR_MEMBER: self.out_property_accessor_member,
            s.QUESTION: self.out_question,
            s.REFERENCE: self.out_reference,
            s.STRING: self.out_string,
            s.STRUCT_DEF: self.out_struct_def,
            s.STRUCT_MEMBER_ASSIGN: self.out_struct_member_assign,
            s.STRUCT_MEMBER_DATA: self.out_struct_member_data,
            s.STRUCT_MEMBER_METHOD: self.out_struct_member_method,
            s.EXPR_SEQ: self.out_expr_seq,
            s.THROW: self.out_throw,
            s.TRY_EXPR: self.out_try_expr,
            s.UNARY_MINUS: self.out_unary_minus,
            s.UNARY_NOT: self.out_unary_not,
            s.VARIABLE_DECL: self.out_variable_decl,
            s.WHILE_LOOP: self.out_while_loop,
            s.LOCAL_DECL: self.out_local_decl,
            s.GLOBAL_DECL: self.out_global_decl,
            s.MOUSETOOL_DEF: self.out_mousetool_def,
            s.TIME: self.out_time,
            s.SMPTE_TIME: self.out_smpte_time,
            s.SET_CONTEXT: self.out_set_context,
            s.WHEN_ATTRIBUTE: self.out_when_attribute,
            s.WHEN_OBJECTS: self.out_when_objects,
            s.PLUGIN_DEF: self.out_plugin_def,
            s.RCMENU_DEF: self.out_rcmenu_def,
            s.ROLLOUT_DEF: self.out_rollout_def,
            s.UTILITY_DEF: self.out_utility_def,

            # python only syntax
            s.PY_SHIM_VAR_NAME: self.out_py_shim_var_name,
            s.PY_BUILTIN_VAR_NAME: self.out_py_builtin_var_name,
            s.PY_RT_VAR_NAME: self.out_py_rt_var_name,
            s.PY_NONLOCAL: self.out_py_nonlocal,
            s.PY_GLOBAL: self.out_py_global,
            s.PY_MACROSCRIPT_CLASS: self.out_py_macroscript_class,
            s.PY_ROLLOUT_CLASS: self.out_py_rollout_class,
            s.PY_PLUGIN_CLASS: self.out_py_plugin_class,
            s.PY_TUPLE: self.out_py_tuple,
            s.PY_NOVAR: self.out_py_novar

        }
        # this are mxs globals that need a special translation in python
        self.wellknown_var_names = {
            "true": "True",
            "false": "False",
            "on": "True",
            "off": "False",
            "undefined": "None",
            "unsupplied": "None" # TODO Check this one
        }
        self.comments = comments
        self.cl = 0
        self.generation_comments = []
        self.limitations = {}
        self.disable_comments = 0

    def append_construct_comments(self, construct):
        """Appends generated commetns to code comments"""
        self.generation_comments = self.generation_comments + construct.comments

    def warning_generation_comment(self, new_comment, limitation=None):
        """Emits a code generation comment that will be inserted in the generated code"""
        self.generation_comments.append((s.COMMENT_WARNING, new_comment, limitation))
    def error_generation_comment(self, new_comment, limitation=None):
        """Emits a code generation comment that will be inserted in the generated code"""
        self.generation_comments.append((s.COMMENT_ERROR, new_comment, limitation))
    def info_generation_comment(self, new_comment, limitation=None):
        """Emits a code generation comment that will be inserted in the generated code"""
        self.generation_comments.append((s.COMMENT_INFO, new_comment, limitation))

    def nowarn(self):
        """Disable the emission of comments in a block of code"""
        class NoWarnings:
            """
            Context for disabling warnings in a block.
            """
            def __init__(self, output):
                self.output = output
            def __enter__(self):
                self.output.disable_comments += 1
                return self
            def __exit__(self, vtype, value, traceback):
                self.output.disable_comments -= 1
                return self
        return NoWarnings(self)

    def consume_generation_comments(self):
        """Consumes the accumulated code generation comments"""
        for _, _, limit in self.generation_comments:
            if limit is not None:
                self.limitations[limit] = lim.LIMITATIONS[limit]
        def formatc(cmt):
            kind, text, limi = cmt
            return (f"# ****** {kind} : {text}"
                    if lim is None
                    else f"# ****** {kind} : {text} ({limi})")
        formatted = "\n".join(map(formatc, self.generation_comments))
        if len(formatted) > 0:
            formatted = formatted + "\n"
        self.generation_comments = []
        return formatted

    def consume_limitations(self):
        """Consumes the accumulated limitations commments (detailed info
        about the code generation comments that is appendend at the end
        of the generated code)"""
        thedict = self.limitations
        self.limitations = {}
        lines = [f"* {k}: {v}" for k, v in thedict.items()]
        if len(lines) > 0:
            #pylint: disable=line-too-long
            general_warning = "The maxscript code contains constructs that are not handled properly by the translator: \n\n"
            joined = "\n\n".join(lines)
            return f'\n\n"""\n{general_warning}\n\n{joined}\n"""'
        return ""


    def comments_before_line(self, l):
        """Finds comments that need to be emitted before line l"""
        if self.disable_comments > 0:
            return ""

        ret = self.consume_generation_comments()
        def select(c):
            (tol, _) = c[2]
            return self.cl <= tol <= l and c[1][0] in [mxscp.SINGLE]
        selected = list(map(lambda c: "# " + c[1][1], filter(select, self.comments)))
        if len(selected) > 0:
            ret = ret + '\n'.join(selected) + "\n"
        self.cl = l + 1 # yucky
        return ret

    def flush_comments_at_end(self):
        """Flushes comments that have never been emitted
        (called at the end of the code generation)"""
        return f"{self.comments_before_line(100000000)}"

    def out_py(self, v):
        """output a givn syntactic construct"""
        self.append_construct_comments(v)
        return self.SWITCH[v.construct](v)

    def out_program(self, t):
        """output the program construct"""
        def outline(c):
            if not c.start is None:
                comments = self.comments_before_line(c.start[0])
                line = self.out_py(c)
                return comments + line
            return self.out_py(c)
        if len(t.args[0]) == 0:
            return "pass"
        mapped = map(outline, t.args[0])
        return '\n'.join(mapped)

    def out_expr_seq(self, t):
        """output the expr seq construct"""
        # -- there are two cases to
        # parenthesized expression
        # and program... I'm not sure mxs
        # distinguishes the two. In our case
        # we could create a subcontext to get this right
        inner = self.out_py(t.args[0])
        return f"({inner})"

    def out_computation(self, t):
        """output the computation construct"""
        # we want to flatten the computation
        argops = t.args[0]
        flattened = [self.out_py(val) for val in argops]
        joined = ' '.join(flattened)
        return f"{joined}"

    def out_call(self, t):
        """output the call construct"""
        def strip_subprogram(t):
            if t.construct == s.EXPR_SEQ:
                return t.args[0]
            return t
        with self.nowarn():
            fname = self.out_py(t.args[0])
            args = filter(lambda c: c.construct != s.NAMED_ARGUMENT, t.args[1])
            kwargs = filter(lambda c: c.construct == s.NAMED_ARGUMENT, t.args[1])
            arg = ', '.join(
                    list(map(self.out_py, map(strip_subprogram, args))) +
                    #list(map(self.out_py, args)) +
                    list(map(self.out_py, kwargs))
                    )
        # --- if fname is free
        if fname == "rt.free":
            self.warning_generation_comment("rt.free does not work on python strings", lim.L2)
        # ----
        # otherwise, must be a mxs function from rt
        return f"{fname}({arg})"

    def out_function_method(self, t, method=False):
        """output the function_method construct"""
        fname = t.args[0].args[0]
        # set param names in the inner scope
        targs = list(map(self.out_py, t.args[1]))
        if method:
            targs = ["self"] + targs
        fargs = ', '.join(targs)
        inner = t.args[2]

        # if the body is a subprogram
        inner = self.strip_subprogram_wrapper(inner)

        fbody = self.out_py(inner)

        bodylines = fbody.split("\n")
        if len(bodylines) == 0:
            bodylines = ["pass"]
        bodylines = map(lambda l: "    " + l, bodylines)
        ifbody = '\n'.join(bodylines)
        return f"def {fname}({fargs}):\n{ifbody}\n"

    def out_function_def(self, t):
        """output the function_def construct"""
        return self.out_function_method(t)

    def out_operand(self, t):
        """output the operand construct"""
        # we jus eat the expression wrapper
        return self.out_py(t.args[0])

    def out_name(self, t):
        """output the name construct"""
        return f'rt.name("{t.args[0]}")'

    def out_point2(self, t):
        """output the point2 construct"""
        v1 = self.out_py(t.args[0])
        v2 = self.out_py(t.args[1])
        return f'rt.point2({v1}, {v2})'

    def out_point3(self, t):
        """output the point3 construct"""
        v1 = self.out_py(t.args[0])
        v2 = self.out_py(t.args[1])
        v3 = self.out_py(t.args[2])
        return f'rt.point3({v1}, {v2}, {v3})'

    def out_point4(self, t):
        """output the point4 construct"""
        v1 = self.out_py(t.args[0])
        v2 = self.out_py(t.args[1])
        v3 = self.out_py(t.args[2])
        v4 = self.out_py(t.args[3])
        return f'rt.point4({v1}, {v2}, {v3}, {v4})'

    def out_array(self, t):
        """output the array construct"""
        values = ', '.join(map(self.out_py, t.args[0]))
        return f'rt.array({values})'

    def out_bitarray(self, t):
        """output the bitarray construct"""
        values = ' + '.join(map(self.out_py, t.args[0]))
        return f'rt.bitarray(*({values}))'

    def out_bitarray_range(self, t):
        """output the bitarray_range construct"""
        first = self.out_py(t.args[0])
        return (f'list(range({first}, {self.out_py(t.args[1])} + 1))'
                if t.args[1] is not None
                else f"[{first}]")

    def out_var_name(self, t):
        """output the var_name construct"""
        name = t.args[0]
        # do keyword substitution by uppercasing keywords
        if name in RESERVED_PYTHON_NAMES:
            orig = name
            name = name[0] + name[1:].upper()
            # ----- LIMITATION
            self.warning_generation_comment(f"Reserved name {orig} capitalized as {name}", lim.L5)
            # --------------

        return SCOPE_PREFIX[t.resolution] + name

    def out_operator(self, t):
        """output the operator construct"""
        # here there could be mappings between
        # MXS and python
        if t.args[0] == "^":
            return "**"
        return t.args[0].lower()

    def out_number(self, t):
        """output the number construct"""
        return t.args[0]

    def out_string(self, t):
        """output the string construct"""
        return f'"{t.args[0]}"'

    def out_if_expr(self, t):
        """output the if_expr construct"""
        # the truth here is that in mxs if is
        # an expression and in python it is a statement
        # when the value of an if is ignored it does not
        # matter but we will eventually have to deal with this
        condition = self.out_py(t.args[0])
        thenexpr = self.out_py(self.strip_subprogram_wrapper(t.args[1]))
        ithenexpr = self.indent_block(thenexpr)
        if t.args[2] is None:
            return f"if {condition}:\n{ithenexpr}"
        elseexpr = self.out_py(self.strip_subprogram_wrapper(t.args[2]))
        ielseexpr = self.indent_block(elseexpr)
        return f"if {condition}:\n{ithenexpr}\nelse:\n{ielseexpr}"

    def out_while_loop(self, t):
        """output the while_loop construct"""
        whileexpr = self.out_py(t.args[0])
        bodyexpr = self.out_py(self.strip_subprogram_wrapper(t.args[1]))
        ibodyexpr = self.indent_block(bodyexpr)
        return f"while {whileexpr}:\n{ibodyexpr}"

    def out_do_loop(self, t):
        """output the do_loop construct"""
        bodyexpr = self.out_py(self.strip_subprogram_wrapper(t.args[0]))
        whileexpr = self.out_py(t.args[1])
        ibodyexpr = self.indent_block(bodyexpr)
        return f"while True:\n{ibodyexpr}\n    if not ({whileexpr}):\n        break"


    def out_for_loop(self, t):
        """output the for_loop construct"""
        var_names = ", ".join(list(map(self.out_py, t.args[0])))
        source = t.args[1]
        sequence = source[0]
        whilev = source[1]
        wherev = source[2]
        bodyexpr = self.out_py(self.strip_subprogram_wrapper(t.args[2]))

        sequencestr = self.out_py(sequence)

        # disable coment emission for the while program
        with self.nowarn():
            if whilev is not None:
                whilev = self.out_py(whilev)
                bodyexpr = f"if not {whilev}:\n    break\n{bodyexpr}"
        if wherev is not None:
            wherev = self.out_py(wherev)
            bodyexpr = f"if not {wherev}:\n    continue\n{bodyexpr}"

        ibodyexpr = self.indent_block(bodyexpr)
        # --- collect not supported
        if t.args[3] == "collect":
            self.warning_generation_comment("collect not yet supported in for loops", lim.L3)
        # -------------------------

        return f"for {var_names} in {sequencestr}:\n{ibodyexpr}"

    def out_for_loop_from_to_sequence(self, t):
        """output the for_loop_from_to_sequence construct"""
        fromv = self.out_py(t.args[0])
        tov = self.out_py(t.args[1])
        byv = t.args[2]
        rangestr = (f"range(int({fromv}), 1 + int({tov}))"
                if byv is None
                else f"range({fromv}, {tov}, {self.out_py(byv)})")
        return rangestr

    def indent_lines(self, lines):
        """split a block of text in lines, indent them and return the
        resulting list"""
        return map(lambda l: "    " + l, lines.split("\n"))

    def indent_block(self, lines):
        """indent a block of multiline text"""
        return "\n".join(self.indent_lines(lines))

    def strip_subprogram_wrapper(self, t):
        """strip a subprogram wrapper in the tree.
        weird. this seems to belong in pytreeprocess."""
        if t.construct == s.EXPR_SEQ:
            return t.args[0]
        return t

    def out_variable_decl(self, t):
        """output the variable_decl construct"""
        scope = t.args[0]
        assignments = t.args[1]

        def out_none(d):
            """output the none construct"""
            # these are always in the current topmost scope
            # so we take the name directly
            decl = self.out_py(d)
            return decl

        def out_local(d):
            """output the local construct"""
            decl = self.out_py(d)
            return decl

        def out_global(d):
            """output the global construct"""
            decl = self.out_py(d)
            name = self.out_py(d.args[0])
            return f"global {name}\n{decl}"

        def out_persistentglobal(b):
            """output the persistentglobal construct"""
            return out_global(b)

        if scope is None:
            return "\n".join(map(out_none, assignments))
        if scope.construct == s.LOCAL:
            return "\n".join(map(out_local, assignments))
        if scope.construct == s.GLOBAL:
            return "\n".join(map(out_global, assignments))
        return "\n".join(map(out_persistentglobal, assignments))

    def out_struct_def(self, t):
        """output the struct_def construct"""
        name = t.args[0].args[0]
        members = t.args[1]
        # filter data members
        #lastcase = list(filter(lambda x: x.args[0] is None, cases))

        amembers = list(filter(lambda x: x.construct == s.STRUCT_MEMBER_ASSIGN, members))
        omembers = list(filter(
            lambda x: x.construct in [s.STRUCT_MEMBER_METHOD, s.STRUCT_MEMBER_DATA],
            members))
        eventmembers = list(filter(lambda x: x.construct == s.ON_DO_HANDLER, members))

        # filter other members
        imembers = self.indent_block('\n'.join(map(self.out_py, omembers)))
        cmembers = self.indent_block(self.indent_block('\n'.join(map(self.out_py, amembers))))

        # we can take care of "on create" event members (in the constructor)
        #createevents = filter(lambda x: x.args[0] == "create", eventmemebers)


        # --- collect not supported
        if len(eventmembers) > 0:
            self.warning_generation_comment("event handlers in structs not supported", lim.L4)
        # -------------------------
        #pylint: disable=line-too-long
        return f"class {name}:\n{imembers}\n    def __init__(self, **kwargs):\n        for key, value in kwargs.items():\n            setattr(self, key, value)\n{cmembers}"

    def out_struct_member_assign(self, t):
        """output the struct_member_assign construct"""
        name = t.args[0].args[0]
        value = self.out_py(t.args[1])
        return f"self.{name} = {value}"

    def out_struct_member_data(self, t):
        """output the struct_member_data construct"""
        name = t.args[0].args[0]
        return f"{name} = None"

    def out_struct_member_method(self, t):
        """output the struct_member_method construct"""
        return self.out_function_method(t.args[0], True)

    def out_property(self, t):
        """output the property construct"""
        accessors = t.args[1]
        raccessors = "".join(map(self.out_py, accessors)) if accessors else ""
        name = self.out_py(t.args[0])
        lcidpy = f"{name}{raccessors}"
        lcid = t.args[0].args[0]
        return self.wellknown_var_names[lcid] if str(lcid) in self.wellknown_var_names else lcidpy

    def out_property_accessor_index(self, t):
        """output the property_accessor_index construct"""
        expt = self.out_py(t.args[0])
        return f"[{expt} - 1]"

    def out_property_accessor_member(self, t):
        """output the property_accessor_member construct"""
        expt = self.out_py(t.args[0])
        return f".{expt}"

    def out_assignment(self, t):
        """output the assignment construct"""
        prop = t.args[0]
        op = t.args[1]
        val = t.args[2]
        tval = self.out_py(val)
        if op == "=" and prop.construct != s.PY_TUPLE:
            if prop.args[1] is None:
                # this is the magic part where this assignment becomes a
                # variable declaration (I think this is needed, but I did not double check in mxs)
                # I also believe the prop needs not to be in the sstacck as a struct
                # this magic thing only happens if the variable
                # does not exist or exists in the global scope
                tprop = self.out_py(prop)
                return f"{tprop} {op} {tval}"
        tprop = self.out_py(prop)
        return f"{tprop} {op} {tval}"

    def out_argument(self, t):
        """output the argument construct"""
        tname = self.out_py(t.args[0])
        # references not supported yet
        return f"{tname}"

    def out_named_argument(self, t):
        """output the named_argument construct"""
        tname = self.out_py(t.args[0])
        tvalue = self.out_py(t.args[1]) if t.args[1] is not None else "None"
        # references not supported yet
        return f"{tname}={tvalue}"

    def out_function_return(self, t):
        """output the function_return construct"""
        if t.args[0] is not None:
            tret = self.out_py(t.args[0])
            return f"return {tret}"
        return "return"

    def out_loop_continue(self, t):
        """output the loop_continue construct"""
        return "continue"

    def out_loop_exit(self, t):
        """output the loop_exit construct"""
        loopval = t.args[0]
        if loopval is not None:
            tloopval = self.out_py(loopval)
            # pylint: disable=line-too-long
            return f"{tloopval} # WARNING: evaluated for side effects\nbreak # WARNING: loop exit value not supported yet"
        return "break"

    def out_case_expr(self, t):
        """output the case_expr construct"""
        cases = t.args[1]
        if len(cases) == 0:
            return ""
        lastcase = list(filter(lambda x: x.args[0] is None, cases))
        normalcases = list(filter(lambda x: x.args[0] is not None, cases))

        def format_action(c):
            return self.indent_block(self.out_py(self.strip_subprogram_wrapper(c)))


        def format_condition_action(c):
            cond = self.out_py(c.args[0])
            act = format_action(c.args[1])
            return (cond, act)

        def with_val(normalcases):
            val = self.out_py(t.args[0])
            def format_elif(c):
                condition, action = format_condition_action(c)
                return f"elif {val} == {condition}:\n{action}"

            firstcase = normalcases[0]
            normalcases = normalcases[1:]
            if len(normalcases) == 0:
                # only a default case! do it all the time
                return format_action(lastcase[0].args[1])
            (condition, action) = format_condition_action(firstcase)
            ret = f"if {val} == {condition}:\n{action}"

            if len(normalcases) > 0:
                ret = ret + "\n" + "\n".join(list(map(format_elif, normalcases)))

            if len(lastcase) > 0:
                action = format_action(lastcase[0].args[1])
                ret = ret + f"\nelse:\n{action}"
            return ret

        def without_val(normalcases):
            def format_elif(c):
                condition, action = format_condition_action(c)
                return f"elif {condition}:\n{action}"

            firstcase = normalcases[0]
            normalcases = normalcases[1:]
            if len(normalcases) == 0:
                # only a default case! do it all the time
                return format_action(lastcase[0].args[1])
            (condition, action) = format_condition_action(firstcase)
            ret = f"if {condition}:\n{action}"

            if len(normalcases) > 0:
                ret = ret + "\n" + "\n".join(list(map(format_elif, normalcases)))

            if len(lastcase) > 0:
                action = format_action(lastcase[0].args[1])
                ret = ret + f"\nelse:\n{action}"
            return ret

        return without_val(normalcases) if t.args[0] is None else with_val(normalcases)

    def out_case_item(self, t):
        """output the case_item construct"""

    def out_try_expr(self, t):
        """output the try_expr construct"""
        # the truth here is that in mxs if is
        # an expression and in python it is a statement
        # when the value of an if is ignored it does not
        # matter but we will eventually have to deal with this
        tryexpr = self.out_py(self.strip_subprogram_wrapper(t.args[0]))
        itryexpr = self.indent_block(tryexpr)
        catchexpr = self.out_py(self.strip_subprogram_wrapper(t.args[1]))
        icatchexpr = self.indent_block(catchexpr)
        return f"try:\n{itryexpr}\nexcept Exception:\n{icatchexpr}"

    def out_max_command(self, t):
        """output the max_command construct"""
        items = t.args[0]
        titems = " ".join(list(map(self.out_py, items)))
        return f"mxsshim.max(\"{titems}\")"

    def out_question(self, t):
        """output the question construct"""
        return "?"

    def out_context_with(self, t):
        """output the context_with construct"""
        # pylint: disable=too-many-return-statements
        kind = t.args[0]
        val = self.out_py(t.args[1])
        if kind == "animate":
            return f"with pymxs.animate({val}):"
        if kind == "undo":
            return f"with pymxs.undo({val}):"
        if kind == "redraw":
            return f"with pymxs.redraw({val}):"
        if kind == "quiet":
            return f"with pymxs.quiet({val}):"
        if kind == "printAllElements":
            return f"with mxsshim.printAllElements({val}):"
        if kind == "defaultAction":
            return f"with mxsshim.defaultAction({val}):"
        if kind == "MXSCallstackCaptureEnabled":
            return f"with mxsshim.MXSCallstackCaptureEnabled({val}):"
        if kind == "dontRepeatMessages":
            return f"with mxsshim.dontRepeatMessages({val}):"
        if kind == "macroRecorderEmitterEnabled":
            return f"with mxsshim.macroRecorderEmitterEnabled({val}):"
        return ""

    def out_context_about(self, t):
        """output the context_about construct"""
        val = self.out_py(t.args[0])
        return f"with mxsshim.about({val})"

    def out_context_at(self, t):
        """output the context_at construct"""
        kind = t.args[0]
        val = self.out_py(t.args[1])
        if kind == "level":
            return f"with pymxs.atlevel({val}):"
        if kind == "time":
            return f"with pymxs.attime({val}):"
        return ""

    def out_context_in_node(self, t):
        """output the context_in_node construct"""
        val = self.out_py(t.args[0])
        return f"with mxsshim.in_node({val}):"

    def out_context_in_coordsys(self, t):
        """output the context_in_coordsys construct"""
        val = self.out_py(t.args[0])
        return f"with mxsshim.in_coordsys({val}):"

    def out_context_expr(self, t):
        """output the context_expr construct"""
        def join_indented(prev, new):
            return new if prev is None else f"{new}\n" + self.indent_block(prev)

        expr = self.strip_subprogram_wrapper(t.args[1])
        texpr = self.out_py(expr)
        contexts = t.args[0]
        #tc = list(map(self.out_py, contexts))
        tcontexts = list(filter(lambda x: x != "", map(self.out_py, contexts)))

        if len(tcontexts) > 0:
            context = functools.reduce(
                        join_indented,
                        reversed(tcontexts + [texpr])
                        )
            return context
        return texpr

    def out_path_name(self, t):
        """output the path_name construct"""
        p = t.args[0]
        return f"mxsshim.path(\"{p}\")"

    def out_py_shim_var_name(self, t):
        """output the py_shim_var_name construct"""
        return f"mxsshim.{t.args[0]}"

    def out_py_rt_var_name(self, t):
        """output the py_rt_var_name construct"""
        return f"rt.{t.args[0]}"

    def out_py_builtin_var_name(self, t):
        """output the py_builtin_var_name construct"""
        return t.args[0]

    def out_py_nonlocal(self, t):
        """output the py_nonlocal construct"""
        return f"nonlocal {t.args[0]}"

    def out_py_global(self, t):
        """output the py_global construct"""
        return f"global {t.args[0]}"

    def out_unary_minus(self, t):
        """output the unary_minus construct"""
        texpr = self.out_py(t.args[0])
        return f"-{texpr}"

    def out_unary_not(self, t):
        """output the unary_not construct"""
        texpr = self.out_py(t.args[0])
        return f"not {texpr}"

    def out_decl(self, d):
        """output the decl construct"""
        name = self.out_py(d.args[0])
        value = self.out_py(d.args[1]) if d.args[1] is not None else "None"
        return f"{name} = {value}"

    def out_py_macroscript_class(self, d):
        """output the py_macroscript_class construct"""
        class_name_c = d.args[0]
        macroscript_name_c = d.args[1]
        handlers_c = d.args[2]
        events_c = d.args[3]
        other_decls = d.args[4]

        # --------------------
        # convert the events to functions
        def generate_event_handler(c):
            ct = self.out_py(c)
            return self.indent_block(ct)
        handlers = "\n".join(list(map(generate_event_handler, handlers_c)))

        # --------------------
        # convert other decls (to class members)
        members = self.indent_block("\n".join(list(map(self.out_py, other_decls))))

        # --------------------
        def generate_registration(c):
            return f'self.on("{c}", self.{c})'

        registration = "\n".join(list(map(generate_registration, events_c)))
        registration = self.indent_block(registration)
        registration = self.indent_block(registration)
        # ---------------------
        class_name = self.out_py(class_name_c)
        macroscript_name = self.out_py(macroscript_name_c)
        self.warning_generation_comment("shimming of macroscripts is poorly supported", lim.L6)
        result = f"""class {class_name}(mxsshim.MacroScript):
    def __init__(self, **kwargs):\n{registration}
        mxsshim.MacroScript.__init__(self, "{macroscript_name}", **kwargs)\n{members}\n{handlers}"""
        return result

    def out_py_rollout_class(self, d):
        """output the py_rollout_class construct"""
        #pylint: disable=too-many-locals
        class_name_c = d.args[0]
        rollout_name_c = d.args[1]
        label_c = d.args[2]
        #handlers_c = d.args[3]
        #events_c = d.args[4]
        #other_decls = d.args[5]
        rollout_items = d.args[6]

        # --------------------
        # generate a rollout item
        def generate_rollout_item(i):
            itemtype = i.args[0]
            varname = self.out_py(i.args[1])
            label = self.out_py(i.args[2])
            return f'mxsshim.RolloutItem("{itemtype}", {varname}, {label})'
        items = ",\n".join(list(map(generate_rollout_item, rollout_items)))
        items = self.indent_block(items)
        items = self.indent_block(items)
        items = self.indent_block(items)
        items = f"        self.items(\n{items})"

        # --------------------
        # generate label
        label = f'        self.label = {self.out_py(label_c)}\n'

        # --------------------
        # convert the events to functions
        #def generate_event_handler(c):
        #    ct = self.out_py(c)
        #    return self.indent_block(ct)
        #handlers = "\n".join(list(map(generate_event_handler, handlers_c)))
        handlers = ""
        # --------------------
        # convert other decls (to class members)
        #members = self.indent_block("\n".join(list(map(self.out_py, other_decls))))
        members = ""

        # --------------------
        #def generate_registration(c):
        #    return f'self.on("{c}", self.{c})'

        #registration = "\n".join(list(map(generate_registration, events_c)))
        #registration = self.indent_block(registration)
        #registration = self.indent_block(registration)
        registration = ""
        # ---------------------
        class_name = self.out_py(class_name_c)
        macroscript_name = self.out_py(rollout_name_c)

        self.warning_generation_comment("shimming of plugins is poorly supported", lim.L8)

        result = f"""class {class_name}(mxsshim.Rollout):
    def __init__(self, **kwargs):\n{label}\n{items}\n{registration}
        mxsshim.Rollout.__init__(self, "{macroscript_name}", **kwargs)\n{members}\n{handlers}"""
        return result

    def out_py_plugin_class(self, d):
        """output the py_plugin_class construct"""
        #pylint: disable=too-many-locals,unreachable
        return "mxshim.unsupported()"

        class_name_c = d.args[0]
        rollout_name_c = d.args[1]
        label_c = d.args[2]
        #handlers_c = d.args[3]
        #events_c = d.args[4]
        #other_decls = d.args[5]
        rollout_items = d.args[6]

        # --------------------
        # generate a rollout item
        def generate_rollout_item(i):
            itemtype = i.args[0]
            varname = self.out_py(i.args[1])
            label = self.out_py(i.args[2])
            return f'mxsshim.RolloutItem("{itemtype}", {varname}, {label})'
        items = ",\n".join(list(map(generate_rollout_item, rollout_items)))
        items = self.indent_block(items)
        items = self.indent_block(items)
        items = self.indent_block(items)
        items = f"        self.items(\n{items})"

        # --------------------
        # generate label
        label = f'        self.label = {self.out_py(label_c)}\n'

        # --------------------
        # convert the events to functions
        #def generate_event_handler(c):
        #    ct = self.out_py(c)
        #    return self.indent_block(ct)
        #handlers = "\n".join(list(map(generate_event_handler, handlers_c)))
        handlers = ""
        # --------------------
        # convert other decls (to class members)
        #members = self.indent_block("\n".join(list(map(self.out_py, other_decls))))
        members = ""

        # --------------------
        #def generate_registration(c):
        #    return f'self.on("{c}", self.{c})'

        #registration = "\n".join(list(map(generate_registration, events_c)))
        #registration = self.indent_block(registration)
        #registration = self.indent_block(registration)
        registration = ""
        # ---------------------
        class_name = self.out_py(class_name_c)
        macroscript_name = self.out_py(rollout_name_c)
        self.warning_generation_comment("shimming of plugins is poorly supported", lim.L8)
        result = f"""class {class_name}(mxsshim.Rollout):
    def __init__(self, **kwargs):\n{label}\n{items}\n{registration}
        mxsshim.Rollout.__init__(self, "{macroscript_name}", **kwargs)\n{members}\n{handlers}"""
        return result


    def out_py_tuple(self, d):
        """output the py_tuple construct"""
        targs = list(map(self.out_py, d.args[0]))
        largs = ", ".join(targs)
        return f"({largs})"

    def out_py_novar(self, d):
        """output the py_novar construct"""
        return "_"

    def out_local_decl(self, d):
        """output the local_decl construct"""
        return "\n".join(list(map(self.out_py, d.args[0])))

    def out_global_decl(self, d):
        """output the global_decl construct"""
        return "\n".join(list(map(self.out_py, d.args[0])))

    def out_mousetool_def(self, d):
        """output the mousetool_def construct"""
        self.warning_generation_comment("shimming of tools is poorly supported", lim.L10)
        return "msxshim.mousetool('tbd')"

    def out_throw(self, d):
        """output the throw construct"""
        #val = d.args[1]
        #debuginfo = d.args[1]
        if d.args[0] is None:
            return 'raise RuntimeError()'
        message = self.out_py(d.args[0])
        return f'raise RuntimeError({message})'

    def out_reference(self, d):
        """output the reference construct"""
        inner = self.out_py(d.args[0])
        return f'pymxs.byref({inner})'

    def out_time(self, d):
        """output the time construct"""
        return f'mxsshim.time("{d.args[0]}")'

    def out_smpte_time(self, d):
        """output the smpte_time construct"""
        return f'mxsshim.time("{d.args[0]}")'

    def out_set_context(self, d):
        """output the set_context construct"""
        return 'mxsshim.setcontext()'

    def out_on_do_handler(self, d):
        """output the on_do_handler construct"""
        return ''

    def out_on_map_do_handler(self, d):
        """output the on_map_do_handler construct"""
        return ''

    def out_when_attribute(self, d):
        """output the when_attribute construct"""
        return ''

    def out_when_objects(self, d):
        """output the when_objects construct"""
        return ''

    # FIXME: don't know why I need this, should have been
    # removed at this point
    def out_plugin_def(self, d):
        """output the plugin_def construct"""
        self.warning_generation_comment("out_plugin_dif", lim.L11)
        return ''

    # FIXME: don't know why I need this, should have been
    # removed at this point
    def out_rcmenu_def(self, d):
        """output the rcmenu_def construct"""
        self.warning_generation_comment("out_recmenu_def", lim.L11)
        return ''

    # FIXME: don't know why I need this, should have been
    # removed at this point
    def out_rollout_def(self, d):
        """output the rollout_def construct"""
        self.warning_generation_comment("out_rollout_def", lim.L11)
        return ''

    # FIXME: don't know why I need this, should have been
    # removed at this point
    def out_utility_def(self, d):
        """output the utility_def construct"""
        self.warning_generation_comment("out_utility_def", lim.L11)
        return ''

def out_py(constructs, comments, file_header="Auto translated maxscript", snippet=False):
    """output the py construct"""
    # mutating, disgusting:
    pytreeprocess.preprocess(constructs)
    #eprint(" ------ transformed syntax tree ---")
    #eprint(constructs)
    #eprint(" ----------------------------------")
    cxt = PythonFormatter(comments)
    if snippet:
        return cxt.out_py(constructs) + "\n"
    fh = ""  if file_header is None else f"'''{file_header}'''\n"
    # pylint: disable=line-too-long
    return f"{fh}from pymxs import runtime as rt\nimport mxsshim\nimport pymxs\n{cxt.out_py(constructs)}\n{cxt.flush_comments_at_end()}\n{cxt.consume_limitations()}"
