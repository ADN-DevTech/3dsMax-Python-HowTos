"""
an mxs parser in python using parsec


This will parse an mxs program to a syntactic
tree.

Then the tree could be use to translate maxscript
to python or for other purposes
"""
# pylint: disable=invalid-name, import-error, too-many-lines, unsupported-binary-operation, fixme, undefined-variable
import sys
from parsec import * # pylint: disable=wildcard-import, redefined-builtin, unused-wildcard-import
import mxs2py.syntax as s

sys.setrecursionlimit(2500)
###################################### HACK FOR DEBUGGING
def logparser(nametext):
    """Decorate a parser for debugging"""
    def lp(p):
        '''`Make a parser as optional. If success, return the result, otherwise return
        default_value silently, without raising any exception. If default_value is not
        provided None is returned instead.
        '''
        @Parser
        def inner_parser(text, index):
            res = p(text, index)
            print(f"{nametext} {text[index:(index+10)]} {index}")
            return res
        return inner_parser
    return lp

###################################### HACK

lparen = string('(')
rparen = string(')')
lbrace = string('{')
rbrace = string('}')
lbrack = string('[')
rbrack = string(']')
colon = string(':')
comma = string(',')
true = string('true').result(True)
false = string('false').result(False)
null = string('null').result(None)

def st(t):
    """wrap a string a syntactic construct"""
    return lambda x: s.Construct(t, x)

def number():
    '''Parse number.'''
    return regex(
            r'-?(([0-9]+)([.](?![.])[0-9]*)?|([.][0-9]+))([eE][+-]?[0-9]+)?[lL]?'
            ).parsecmap(st(s.NUMBER))

def intnumber():
    '''Parse integer number.'''
    return regex(r'-?[1-9][0-9]*[lL]?').parsecmap(st(s.NUMBER))

def hexnumber():
    """parse a hex number"""
    return regex(r'0x[0-9a-fA-F]+').parsecmap(st(s.NUMBER))

def question():
    '''Parse number.'''
    return regex(r'\?').parsecmap(st(s.QUESTION))

@generate
def quoted():
    '''Parse quoted string.'''
    @generate
    def normal():
        body = yield regex(r'"([^"\\]|\\.)*"')
        return body

    @generate
    def verbatim():
        body = yield regex(r'@"[^"]*"')
        body = body.replace("\\", "\\\\")
        return body[1:]

    body = yield normal | verbatim

    return s.Construct(s.STRING, body[1:-1])

def reserved():
    """Parse a reserved keyword"""
    # pylint: disable=line-too-long
    return regex("(about|and|animate|as|at|attributes|by|case|catch|collect|continue|coordsys|do|else|exit|fn|for|from|function|global|if|in|local|macroscript|mapped|max|not|of|off|on|or|parameters|persistent|plugin|rcmenu|return|rollout|set|struct|then|throw|to|tool|try|undo|utility|when|where|while|with)(?![a-zA-Z0-9_])", re.IGNORECASE)

def nonkwchar():
    """parse a character that cannot be part of a keyword"""
    return regex("[^a-zA-Z0-9_]")

def keyword(kw):
    """parse a keyword"""
    return ends_with(regex(kw, re.IGNORECASE), nonkwchar())

def on_value():
    """parse the mxs on"""
    # note: in maxscript on & off are special... they are keywords (contrary to undefined, ...)
    return keyword("on")

def off_value():
    """parse the mxs off"""
    # note: in maxscript on & off are special... they are keywords (contrary to undefined, ...)
    return keyword("off")

# ###### SPACES

def singlelinespaces1():
    '''normalspaces with no newlines'''
    return regex("[ \t]+")

def singlelinespaces():
    '''normalspaces with no newlines'''
    return regex(r"([ \t]*(\\.*\n)?)*", re.MULTILINE)

def normalspaces():
    """parse spaces including newlines"""
    return regex(r"[; \t\n\r\\]*", re.MULTILINE)

def statementsep():
    '''statement separator'''
    return regex("[;\n\r]")

# ################### LITERALS

def var_name():
    '''var_name'''
    return (
        on_value() ^
        off_value() ^
        exclude(regex("(::)?('[^']+'|[a-zA-Z_][a-zA-Z0-9_]*)(?!:)"),
            reserved())).parsecmap(st(s.VAR_NAME))

def named_arg_var_name():
    '''var_name'''
    return (
        #exclude(regex("[a-zA-Z_][a-zA-Z0-9_]*(?=:)"), reserved())).parsecmap(st(s.VAR_NAME))
        # weirdly in mascript these allow to use of reserved keywords
        regex("[a-zA-Z_][a-zA-Z0-9_]*(?=:)")).parsecmap(st(s.VAR_NAME))

@generate
def mxsname():
    '''name'''
    @generate
    def unquoted_mxsname():
        name = yield regex("#[a-zA-Z0-9_]+")
        return s.Construct(s.NAME, name[1:])
    @generate
    def quoted_mxsname():
        name = yield regex("#'[^']*'")
        return s.Construct(s.NAME, name[2:-1])
    ret = yield unquoted_mxsname | quoted_mxsname
    return ret

@generate
def time():
    """parse a mxs time"""
    @generate
    def tv():
        # pylint: disable=redefined-outer-name
        num = yield number()
        unit = yield regex("[msft]")
        return f"{num.args[0]}{unit}"
    tvs = yield many1(tv)
    return s.Construct(s.TIME, "".join(tvs))

def smptetime():
    """parse a smpte time"""
    return regex(r"-?[0-9]+:[0-9]+\.[0-9]+").parsecmap(st(s.SMPTE_TIME))

def listsep():
    '''list separator'''
    return regex("[ \t\n\r;]*,[ \t\n\r;]*")

@generate
def point2():
    """parse a point2"""
    yield lbrack
    yield normalspaces()
    v1 = yield expression
    yield listsep()
    v2 = yield expression
    yield normalspaces()
    yield rbrack
    return s.Construct(s.POINT2, v1, v2)


@generate
def point3():
    """parse a point3"""
    yield lbrack
    yield normalspaces()
    v1 = yield expression
    yield listsep()
    v2 = yield expression
    yield listsep()
    v3 = yield expression
    yield normalspaces()
    yield rbrack
    return s.Construct(s.POINT3, v1, v2, v3)

@generate
def point4():
    """parse a point4"""
    yield lbrack
    yield normalspaces()
    v1 = yield expression
    yield listsep()
    v2 = yield expression
    yield listsep()
    v3 = yield expression
    yield listsep()
    v4 = yield expression
    yield normalspaces()
    yield rbrack
    return s.Construct(s.POINT4, v1, v2, v3, v4)

@generate
def array():
    """parse an array"""
    yield string("#")
    yield normalspaces()
    yield string("(")
    yield normalspaces()
    values = yield sepBy(expression, listsep())
    yield normalspaces()
    yield rparen
    return s.Construct(s.ARRAY, values)

@generate
def bitarray():
    # pylint: disable=unused-variable
    """parse a bitarray"""
    @generate
    def bitarray_number():
        ret = yield (number() ^
            property_ref |
            expr_seq
            # ??? ? last listener result (OMG!!) ==> could be shimmed in python if true
            )
        return ret

    @generate
    def bitarray_to():
        yield string("..")
        yield normalspaces()
        toexpr = yield expression
        return toexpr

    @generate
    def bitarray_range():
        fromexpr = yield expression
        yield normalspaces()
        toexpr = yield optional(bitarray_to)
        return s.Construct(s.BITARRAY_RANGE, fromexpr, toexpr)


    yield string("#")
    yield normalspaces()
    yield string("{")
    yield normalspaces()
    values = yield sepBy(bitarray_range, listsep())
    yield normalspaces()
    yield rbrace
    return s.Construct(s.BITARRAY, values)

@generate
def path_name():
    """parse a pathname, the thing that starts with a $"""
    # the last part of this is a big hack of something that needs to be revisiter for sample 268
    name_component = regex(r"'[^']*'|([A-Za-z0-9_\*\?\\]|(\.\.\.))*")
    yield string("$")
    components = yield sepBy(name_component, string("/"))
    pn = "$" + "/".join(components)
    return s.Construct(s.PATH_NAME, pn)

# ################# FUNCTIONS
@generate
def factor():
    """parse a factor"""
    @generate
    def unary_minus():
        yield string("-")
        yield normalspaces()
        expr = yield expression
        return s.Construct(s.UNARY_MINUS, expr)

    @generate
    def unary_not():
        yield keyword("not")
        yield normalspaces()
        expr = yield expression
        return s.Construct(s.UNARY_NOT, expr)

    ret = yield (hexnumber() ^
            time ^
            smptetime() ^
            number() |
            quoted |
            path_name |
            var_name() |
            mxsname ^
            array ^
            bitarray ^
            point4 ^
            point3 ^
            point2 ^
            unary_minus ^
            unary_not ^
            expr_seq
            )
    return ret

@generate
def operand():
    """parse an operand"""
    # This looks like a hack, but I don't think you can take the
    # reference of an arbitrary expression in maxscript, i.e. this is an error
    #zzz = 3
    #3
    #fn getzzz = (return zzz)
    #getzzz()
    #getzzz ()
    #3
    #&(getzzz())
    # but weirdly &(abc[3]) needs to work
    @generate
    def parenthesized_property_ref():
        yield string("(")
        yield normalspaces()
        pr = yield property_ref ^ parenthesized_property_ref
        yield normalspaces()
        yield string(")")
        return pr
    @generate
    def unary_reference():
        yield string("&")
        yield normalspaces()
        expr = yield property_ref ^ parenthesized_property_ref
        return s.Construct(s.REFERENCE, expr)

    #simple values that can be used as function args
    ret = yield (
        property_ref ^
        unary_reference ^
        factor
        # index (this is included in property_ref the way we do it here)
        )
    return ret

@generate
def function_def():
    '''Parse function definition'''

    @generate
    def argument_def():
        ref = yield optional(string("&"))
        vn = yield var_name()
        return s.Construct(s.ARGUMENT, vn, ref)
    @generate
    def named_argument_def():
        @generate
        def optional_value():
            yield normalspaces()
            value = yield operand
            return value

        ref = yield optional(string("&"))
        iden = yield named_arg_var_name()
        yield string(":")
        value = yield optional(optional_value)
        return s.Construct(s.NAMED_ARGUMENT, iden, value, ref)

    yield keyword("fn|function")
    yield normalspaces()
    fname = yield var_name()
    yield normalspaces()
    fargs = yield sepBy((named_argument_def ^ argument_def), normalspaces())
    yield normalspaces()
    yield string("=")
    yield normalspaces()
    funexpr = yield expression
    return s.Construct(s.FUNCTION_DEF, fname, fargs, funexpr)

@generate
def named_argument():
    """parse a named argument"""
    iden = yield named_arg_var_name()
    yield string(":")
    yield singlelinespaces()
    value = yield operand
    return s.Construct(s.NAMED_ARGUMENT, iden, value)

@generate
def function_call():
    '''Parse a function call'''

    @generate
    def no_parameters():
        yield string("(")
        yield singlelinespaces()
        yield string(")")
        return []

    @generate
    def parameters():
        fargs = yield sepBy1((named_argument ^ operand), singlelinespaces())
        return fargs


    # pylint: disable=comparison-with-callable
    fname = yield property_ref < regex(r"(?!(\-| *- ))")
    yield singlelinespaces()
    fargs = yield no_parameters ^ parameters
    return s.Construct(s.CALL, fname, fargs)

@generate
def function_return():
    """parse a function return"""
    @generate
    def optional_value():
        yield normalspaces()
        value = yield expression
        return value

    yield keyword("return")
    value = yield optional(optional_value)
    return s.Construct(s.FUNCTION_RETURN, value)

# ################ variable_decl (note these are NOT expressions)

@generate
def decl():
    """parse a decl"""
    @generate
    def var_assignment():
        localiden = yield var_name()
        yield normalspaces()
        yield string("=")
        yield normalspaces()
        value = yield expression
        return s.Construct(s.DECL, localiden, value)

    @generate
    def declaration():
        localiden = yield var_name()
        return s.Construct(s.DECL, localiden, None)

    v = yield var_assignment ^ declaration
    return v

@generate
def variable_decl():
    """parse a variable decl"""
    @generate
    def persistent_global_scope():
        yield keyword("persistent")
        yield normalspaces()
        yield keyword("global")
        return s.Construct(s.PERSISTENTGLOBAL)

    @generate
    def global_scope():
        yield keyword("global")
        return s.Construct(s.GLOBAL)

    @generate
    def local_scope():
        yield keyword("local")
        return s.Construct(s.LOCAL)

    @generate
    def scope_def():
        sdef = yield (
            persistent_global_scope ^
            global_scope ^
            local_scope)
        return sdef

    # parsing (if there is no scope, it not a decl it an assignment)
    scope = yield scope_def
    yield normalspaces()
    assignments = yield sepBy1(
        decl, # optional_assignment if scope else assignment,
        listsep())

    return s.Construct(s.VARIABLE_DECL, scope, assignments)

# ################# Assignment

@generate
def assignment():
    """parse and assignment"""
    prop = yield property_ref
    yield normalspaces()
    oper = yield regex(r"(=|\+=|-=|\*=|/=)")
    yield normalspaces()
    val = yield expression
    return s.Construct(s.ASSIGNMENT, prop, oper, val)

# ################# STRUCTS
@generate
def struct_def():
    """parse a struct def"""
    @generate
    def struct_assignment():
        localiden = yield var_name()
        yield normalspaces()
        yield string("=")
        yield normalspaces()
        value = yield expression
        return s.Construct(s.STRUCT_MEMBER_ASSIGN, localiden, value)

    @generate
    def declaration():
        localiden = yield var_name()
        return s.Construct(s.STRUCT_MEMBER_DATA, localiden)

    @generate
    def fcn():
        fcn = yield function_def
        return s.Construct(s.STRUCT_MEMBER_METHOD, fcn)

    @generate
    def member():
        yield optional(keyword("private|public"))
        yield normalspaces()
        v = yield struct_assignment ^ on_do_handler ^ declaration ^ fcn
        return v

    yield keyword("struct")
    yield normalspaces()
    name = yield var_name()
    yield normalspaces()
    yield lparen
    yield normalspaces()
    members = yield sepBy1(
        member,
        listsep()
        )
    yield normalspaces()
    yield rparen

    return s.Construct(s.STRUCT_DEF, name, members)

@generate
def property_ref():
    """parse a property ref"""
    def member_name():
        '''member_name'''
        return regex("[a-zA-Z_][a-zA-Z0-9_]*").parsecmap(st(s.VAR_NAME))
    @generate
    def quoted_member_name():
        '''quoted member_name'''
        name = yield regex("'.*'")
        return s.Construct(s.VAR_NAME, name[1:-1])

    @generate
    def member_accessor():
        yield string(".")
        yield normalspaces()
        iden = yield quoted_member_name ^ member_name()
        return s.Construct(s.PROPERTY_ACCESSOR_MEMBER, iden)

    @generate
    def index_accessor():
        yield string("[")
        yield normalspaces()
        expr = yield expression
        yield normalspaces()
        yield string("]")
        return s.Construct(s.PROPERTY_ACCESSOR_INDEX, expr)

    @generate
    def accessor():
        acc = yield (
            member_accessor |
            index_accessor
            )
        return acc
    @generate
    def nestedproperty():
        @generate
        def parenthesized_subscriptable():
            yield lparen
            yield normalspaces()
            se = yield simple_expr
            yield normalspaces()
            yield rparen
            return se

        @generate
        def subscriptable():
            # note: the impact on performance of supporting the parenthesis thing here
            # is pretty dramatic especially with nested parenthesis: every parenthesis
            # block and all what it contains needs to be parsed twice.
            # The way of fixing this (well the only way that I see) is to have optional
            # subscripting after parameters (so this would be a completely different
            # way of implementing this)
            # factor # FIXME: also a parentesised expression
            iden = yield var_name() | path_name | parenthesized_subscriptable
            return iden
        root = yield subscriptable
        yield normalspaces()
        indexing = yield sepBy1(accessor, normalspaces())
        return s.Construct(s.PROPERTY, root, indexing)
    @generate
    def simpleproperty():
        iden = yield var_name()
        return s.Construct(s.PROPERTY, iden, None)

    # this is wrong but will require more cleanup
    prop = yield (
        nestedproperty ^
        simpleproperty)
    return prop

# ################# EXPRESSIONS

# ----- other expressions
def operator():
    '''operator in some computation'''
    return regex(
            r"and(?![a-z0-9])|or(?![a-z0-9_])|as(?![a-z0-9_])|>=|<=|==|!=|[+*/<>\-^]",
            re.IGNORECASE).parsecmap(st(s.OPERATOR))

#def unaryoperator():
#    """parse unary operator"""
#    return regex(r"-|not(?![a-z0-9_])", re.IGNORECASE).parsecmap(st(s.UNARYOPERATOR))

@generate
def computation_operand():
    """parse an operand"""
    ret = yield function_call ^ operand
    return ret

@generate
def op():
    """pare an operator"""
    left = yield computation_operand
    yield normalspaces() #singlelinespaces()
    oper = yield operator()
    return [left, oper]

@generate
def computation():
    """parse a computation"""
    ops = yield sepBy1(op, normalspaces())
    yield normalspaces()
    final = yield computation_operand
    flattened = [v for op in ops for v in op] + [final]
    return s.Construct(s.COMPUTATION, flattened)

@generate
def simple_expr():
    """parse a simple expr"""
    ret = yield (
        computation ^
        function_call ^
        operand ^
        expr_seq
        )
    return ret

@generate
def expression():
    """Maybe should be called a statement or..."""
    ret = yield (
        variable_decl ^
        assignment ^
        if_expr ^
        while_loop ^
        do_loop ^
        for_loop ^
        loop_exit ^
        case_expr ^
        struct_def ^
        try_expr ^
        throw ^
        function_def ^
        function_return ^
        loop_continue ^ # !!!????
        context_expr ^
        set_context ^
        max_command ^
        simple_expr ^
        utility_def ^
        rollout_def ^
        mousetool_def ^
        rcmenu_def ^
        macroscript_def ^
        plugin_def ^
        attributes_def ^
        when_handler
        )
    return ret

# ############### PROGRAM CONTROL FLOW

@generate
def if_expr():
    """parse an if expr"""
    @generate
    def if_then_else():
        yield keyword("then")
        yield normalspaces()
        thenexpr = yield expression
        # optional else
        @generate
        def else_expr():
            yield normalspaces()
            yield keyword("else")
            yield normalspaces()
            expr = yield expression
            return expr
        elseexpr = yield optional(else_expr)
        return (thenexpr, elseexpr)

    @generate
    def if_do():
        yield keyword("do")
        yield normalspaces()
        thenexpr = yield expression
        return (thenexpr, None)

    yield keyword("if")
    yield singlelinespaces()
    expr = yield expression
    yield normalspaces()
    (thenexpr, elseexpr) = yield if_then_else ^ if_do

    return s.Construct(s.IF_EXPR, expr, thenexpr, elseexpr)

@generate
def while_loop():
    """parse a while loop"""
    yield keyword("while")
    yield normalspaces()
    whileexpr = yield expression
    yield normalspaces()
    yield keyword("do")
    yield normalspaces()
    bodyexpr = yield expression
    return s.Construct(s.WHILE_LOOP, whileexpr, bodyexpr)

@generate
def do_loop():
    """parse a do loop"""
    yield keyword("do")
    yield normalspaces()
    bodyexpr = yield expression
    yield normalspaces()
    yield keyword("while")
    yield normalspaces()
    whileexpr = yield expression
    return s.Construct(s.DO_LOOP, bodyexpr, whileexpr)

# this is an over simplification but easy
# to improve
@generate
def for_loop():
    """parse a for loop"""
    yield keyword("for")
    yield normalspaces()
    ident = yield separated(var_name(), listsep(), 1, 3, False)
    yield normalspaces()
    yield keyword("in") ^ string("=")
    yield normalspaces()

    @generate
    def by_expr():
        yield keyword("by")
        yield normalspaces()
        expr = yield expression
        return expr
    @generate
    def where_expr():
        yield keyword("where")
        yield normalspaces()
        expr = yield expression
        return expr
    @generate
    def while_expr():
        yield keyword("while")
        yield normalspaces()
        expr = yield expression
        return expr

    @generate
    def from_to_sequence():
        fromexpr = yield expression
        yield normalspaces()
        yield keyword("to")
        yield normalspaces()
        toexpr = yield expression
        yield normalspaces()
        byexpr = yield optional(by_expr)
        return s.Construct(s.FOR_LOOP_FROM_TO_SEQUENCE, fromexpr, toexpr, byexpr)
    @generate
    def source():
        sequence = yield from_to_sequence ^ expression
        yield normalspaces()
        whileexpr = yield optional(while_expr)
        yield normalspaces()
        whereexpr = yield optional(where_expr)
        return [sequence, whileexpr, whereexpr]

    src = yield source
    yield normalspaces()
    mode = yield keyword("do|collect")
    yield normalspaces()
    expr = yield expression
    return s.Construct(s.FOR_LOOP, ident, src, expr, mode)

@generate
def loop_continue():
    """parse a continue"""
    yield keyword("continue")
    return s.Construct(s.LOOP_CONTINUE)

@generate
def loop_exit():
    """parse a loop exit"""
    @generate
    def with_expr():
        yield normalspaces()
        yield keyword("with")
        yield normalspaces()
        value = yield operand
        return value

    yield keyword("exit")
    value = yield optional(with_expr)
    return s.Construct(s.LOOP_EXIT, value)

# ############## TRY EXPR

@generate
def try_expr():
    """parse a try expr"""
    yield keyword("try")
    yield normalspaces()
    tryexpr = yield expression
    yield normalspaces()
    yield keyword("catch")
    yield normalspaces()
    catchexpr = yield expression
    return s.Construct(s.TRY_EXPR, tryexpr, catchexpr)

@generate
def throw():
    """parse a throw"""
    @generate
    def debug_thing():
        yield keyword("debugbreak:")
        yield singlelinespaces()
        val = yield simple_expr
        return val

    @generate
    def full_throw():
        message = yield simple_expr
        yield singlelinespaces()
        val = yield optional(simple_expr)
        yield singlelinespaces()
        debuginfo = yield optional(debug_thing)
        return s.Construct(s.THROW, message, val, debuginfo)

    yield keyword("throw")
    yield singlelinespaces()
    full = yield optional(full_throw)
    return full if full is not None else s.Construct(s.THROW, None, None, None)

# ############## CASE EXPR
# +/- hacky : this is the same as factor excepted
# for name that here CAN be followed by a :
def case_var_name():
    '''var_name'''
    return (
        on_value() ^
        off_value() ^
        exclude(
            regex("(::)?('[^']+'|[a-zA-Z_][a-zA-Z0-9_]*)"),
            reserved())).parsecmap(st(s.VAR_NAME))

@generate
def case_factor():
    """parse a factor in a case"""
    @generate
    def unary_minus():
        yield string("-")
        yield normalspaces()
        expr = yield expression
        return s.Construct(s.UNARY_MINUS, expr)

    @generate
    def unary_not():
        yield keyword("not")
        yield normalspaces()
        expr = yield expression
        return s.Construct(s.UNARY_NOT, expr)

    ret = yield (hexnumber() ^
            time ^
            smptetime() ^
            number() |
            quoted |
            path_name |
            case_var_name() |
            mxsname ^
            array ^
            bitarray ^
            point4 ^
            point3 ^
            point2 ^
            unary_minus ^
            unary_not ^
            expr_seq
            # ??? ? last listener result (OMG!!) ==> could be shimmed in python if true
            )
    return ret

@generate
def case_expr():
    # pylint: disable=useless-return
    """parse a case expr"""
    @generate
    def default():
        yield keyword("default")
        return None

    @generate
    def case_item():
        case = yield default ^ case_factor
        yield normalspaces()
        yield string(":")
        yield normalspaces()
        expr = yield expression
        return s.Construct(s.CASE_ITEM, case, expr)

    yield keyword("case")
    yield normalspaces()
    expr = yield optional(expression)
    yield normalspaces()
    yield keyword("of")
    yield normalspaces()
    yield lparen
    yield normalspaces()
    cases = yield sepBy(case_item, end_of_statement)
    yield normalspaces()
    yield rparen
    return s.Construct(s.CASE_EXPR, expr, cases)

# ############## MAX_COMMAND
@generate
def max_command():
    """parse max command"""
    def max_command_var_name():
        '''var_name'''
        return (
            regex("[a-zA-Z_][a-zA-Z0-9_]*")).parsecmap(st(s.VAR_NAME))

    yield keyword("max")
    yield singlelinespaces()
    things = yield sepBy((max_command_var_name() ^ question()), singlelinespaces())
    return s.Construct(s.MAX_COMMAND, things)

# ############## CONTEXT_EXPR
@generate
def about_context():
    """parse the about context expr"""
    yield keyword("about")
    yield normalspaces()
    v = yield operand
    return s.Construct(s.CONTEXT_ABOUT, v)

@generate
def with_context():
    """parse the with context expr"""
    # pylint: disable=line-too-long
    yield optional(keyword("with"))
    yield normalspaces()
    kw = yield keyword("(animate|undo|redraw|quiet|printAllElements|defaultAction|MXSCallstackCaptureEnabled|dontRepeatMessages|macroRecorderEmitterEnabled)")
    yield normalspaces()
    v = yield operand #expression
    return s.Construct(s.CONTEXT_WITH, kw, v)
@generate
def at_context():
    """parse the at context expr"""
    yield keyword("at")
    yield normalspaces()
    kw = yield keyword("level|time")
    yield normalspaces()
    v = yield operand
    return s.Construct(s.CONTEXT_AT, kw, v)

@generate
def innode_context():
    """parse the in context expr"""
    yield keyword("in")
    yield normalspaces()
    v = yield expression
    return s.Construct(s.CONTEXT_IN_NODE, v)

@generate
def incoordsys_context():
    """parse the in coordsys context expr"""
    @generate
    def special_name():
        name = yield keyword("world|local|parent|grid|screen")
        return s.Construct(s.NAME, name)
    yield optional(keyword("in"))
    yield normalspaces()
    yield keyword("coordsys")
    yield normalspaces()
    v = yield special_name | operand
    return s.Construct(s.CONTEXT_IN_COORDSYS, v)

@generate
def context_expr():
    """parse a context expr"""
    contexts = yield sepBy1(
            about_context ^
            incoordsys_context ^
            innode_context ^
            at_context ^
            with_context, listsep())
    yield normalspaces()
    expr = yield expression
    return s.Construct(s.CONTEXT_EXPR, contexts, expr)


# set context
@generate
def set_context():
    """parse a set context"""
    yield keyword("set")
    yield normalspaces()
    cxt = yield about_context ^ incoordsys_context ^ innode_context ^ at_context ^ with_context
    return s.Construct(s.SET_CONTEXT, cxt)

# ############## FUNKY THINGS ----------------------------------------------------
# opinion: this is so wrong that it should be deprecated and replaced by an api
# that would simply be used by python. There should be an api for of this.

@generate
def utility_clause():
    """parse a utility clause"""
    res = yield rollout_def ^ rollout_clause
    return res

@generate
def utility_def():
    """parse a utility def"""
    yield keyword("utility")
    yield normalspaces()
    vname = yield var_name()
    yield normalspaces()
    stri = yield quoted
    yield normalspaces()
    vnop = yield optional(named_argument)
    yield normalspaces()
    yield string("(")
    yield normalspaces()
    clauses = yield sepBy(rollout_clause, end_of_statement) #normalspaces())
    yield normalspaces()
    yield string(")")
    return s.Construct(s.UTILITY_DEF, vname, stri, vnop, clauses)

@generate
def local_decl():
    """parse a local def"""
    yield keyword("local")
    yield normalspaces()
    decls = yield sepBy1(decl, listsep())
    return s.Construct(s.LOCAL_DECL, decls)

@generate
def global_decl():
    """parse a global decl"""
    yield keyword("global")
    yield normalspaces()
    decls = yield sepBy1(decl, listsep())
    return s.Construct(s.GLOBAL_DECL, decls)

@generate
def rollout_item():
    """parse a rollout item"""
    # pylint: disable=line-too-long
    kw = yield keyword("dotnetcontrol|hyperlink|subrollout|multilistbox|imgtag|curvecontrol|angle|label|button|edittext|combobox|dropdownList|listbox|spinner|slider|pickbutton|radiobuttons|checkbox|checkbutton|colorPicker|mapbutton|materialbutton|progressbar|timer|bitmap|groupbox")
    yield normalspaces()
    var = yield var_name()
    yield normalspaces()
    label = yield optional(quoted)
    yield normalspaces()
    args = yield sepBy(named_argument, normalspaces())
    return s.Construct(s.ROLLOUT_ITEM, kw, var, label, args)


@generate
def item_group():
    """parse an item group"""
    yield keyword("group")
    yield normalspaces()
    qstring = yield quoted
    yield normalspaces()
    yield string("(")
    yield normalspaces()
    group = yield sepBy(rollout_item, normalspaces())
    yield normalspaces()
    yield string(")")
    return s.Construct(s.ROLLOUT_GROUP, qstring, group)

# FIXME: is this necessary? can we simply use the generic on_do_handler that we use elsewhere
@generate
def rollout_handler():
    """parse a rollout handler"""
    yield keyword("on")
    yield normalspaces()
    handlername = yield var_name()
    yield normalspaces()
    varn = yield var_name()
    yield normalspaces()
    varn2 = yield optional(var_name())
    yield normalspaces()
    varn3 = yield optional(var_name())
    yield normalspaces()
    yield keyword("do")
    yield normalspaces()
    expr = yield expression
    return s.Construct(s.ROLLOUT_HANDLER, handlername, varn, varn2, varn3, expr)

@generate
def rollout_clause():
    """parse a rollout clause"""
    clause = yield (local_decl ^
        global_decl ^
        function_def ^
        struct_def ^
        mousetool_def ^
        item_group ^
        rollout_item ^
        rollout_handler)
    # this is weird, why this clause?
    # (in the macroscript thing we use it as a bundle of things...
    # not sure I remember why either)
    return s.Construct(s.ROLLOUT_CLAUSE, clause)

@generate
def rollout_def():
    """parse a rollout def"""
    yield keyword("rollout")
    yield normalspaces()
    vname = yield var_name()
    yield normalspaces()
    qstring = yield quoted
    yield normalspaces()
    vnop = yield sepBy(named_argument, normalspaces())
    yield normalspaces()
    yield string("(")
    yield normalspaces()
    clauses = yield sepBy(rollout_clause, normalspaces())
    yield normalspaces()
    yield string(")")
    return s.Construct(s.ROLLOUT_DEF, vname, qstring, vnop, clauses)


@generate
def rcmenu_item():
    """parse a rcmenu item"""
    yield keyword("menuitem|separator|submenu")
    yield normalspaces()
    varname = yield var_name()
    yield normalspaces()
    label = yield quoted
    yield normalspaces()
    vnarg = yield sepBy(named_argument, singlelinespaces())
    return s.Construct(s.RCMENU_ITEM, varname, label, vnarg)

@generate
def rcmenu_handler():
    """parse a rcmenu handler"""
    yield keyword("on")
    yield normalspaces()
    varname = yield var_name()
    yield normalspaces()
    vn2 = yield var_name()
    yield normalspaces()
    yield keyword("do")
    yield normalspaces()
    expr = yield expression
    return s.Construct(s.RCMENU_HANDLER, varname, vn2, expr)


@generate
def rcmenu_clause():
    """parse a rcmenu clause"""
    clause = yield (
        rcmenu_handler ^
        local_decl ^
        function_def ^
        struct_def ^
        rcmenu_item)
    return clause


@generate
def rcmenu_def():
    """parse an rc menu def"""
    yield keyword("rcmenu")
    yield normalspaces()
    vname = yield var_name()
    yield normalspaces()
    yield string("(")
    yield normalspaces()
    clauses = yield sepBy(rcmenu_clause, end_of_statement)
    yield normalspaces()
    yield string(")")
    return s.Construct(s.RCMENU_DEF, vname, clauses)

@generate
def on_do_handler():
    """parse a on do handler"""
    @generate
    def do_exprseq():
        yield keyword("do")
        yield normalspaces()
        handler = yield expression # expr_seq
        return handler

    yield keyword("on")
    yield normalspaces()
    event = yield var_name()
    yield normalspaces()
    handler = yield function_return | do_exprseq
    return s.Construct(s.ON_DO_HANDLER, event, handler)

@generate
def on_map_do_handler():
    """parse a on map do handler"""
    @generate
    def do_exprseq():
        yield keyword("do")
        yield normalspaces()
        handler = yield expression # expr_seq
        return handler

    yield keyword("on")
    yield normalspaces()
    yield keyword("map")
    yield normalspaces()
    event = yield var_name()
    yield normalspaces()
    varname = yield var_name() # pylint: disable=unused-variable
    yield normalspaces()
    handler = yield function_return | do_exprseq
    # this is definitely faulty, we ignore the varname
    return s.Construct(s.ON_MAP_DO_HANDLER, event, handler)

@generate
def on_clone_do_handler():
    """parse a on clone do handler"""
    @generate
    def do_exprseq():
        yield keyword("do")
        yield normalspaces()
        handler = yield expression # expr_seq
        return handler

    yield keyword("on")
    yield normalspaces()
    yield keyword("clone")
    yield normalspaces()
    thing = yield var_name()
    yield normalspaces()
    handler = yield function_return | do_exprseq
    return s.Construct(s.ON_CLONE_DO_HANDLER, thing, handler)


@generate
def macroscript_clause():
    """parse a macroscript clause"""
    @generate
    def handler_block_item():
        ret = yield on_do_handler ^ local_decl ^ function_def
        return ret
    yield lparen
    yield normalspaces()
    handlers = yield sepBy1(handler_block_item, normalspaces())
    yield normalspaces()
    yield rparen
    return s.Construct(s.MACROSCRIPT_CLAUSE, handlers)

@generate
def macroscript_def():
    """parse a macroscript def"""
    yield keyword("macroscript")
    yield normalspaces()
    vname = yield var_name()
    yield normalspaces()
    vnop = yield sepBy(named_argument, normalspaces())
    yield normalspaces()
    handlers = yield expr_seq ^ macroscript_clause

    return s.Construct(s.MACROSCRIPT_DEF, vname, vnop, handlers)

@generate
def tool_clause():
    """parse a tool clause"""
    yield (local_decl ^
        function_def ^
        struct_def ^
        tool_handler)

@generate
def tool_handler():
    """parse a tool handler"""
    yield keyword("on")
    yield normalspaces()
    yield var_name()
    yield normalspaces()
    yield optional(var_name())
    yield normalspaces()
    yield keyword("do")
    yield normalspaces()
    expr = yield expression
    return expr

@generate
def mousetool_def():
    """parse a mousetool def"""
    yield keyword("tool")
    yield normalspaces()
    vname = yield var_name()
    yield normalspaces()
    vnop = yield sepBy(named_argument, normalspaces())
    yield normalspaces()
    yield string("(")
    yield normalspaces()
    toolclauses = yield sepBy(tool_clause, normalspaces())
    yield normalspaces()
    yield string(")")
    return s.Construct(s.MOUSETOOL_DEF, vname, vnop, toolclauses)

# ----- parameters


@generate
def param_defs():
    """parse param defs"""
    @generate
    def param_def():
        yield var_name()
        yield singlelinespaces()
        # this looks faulty: we do nothing with vnop!?!?!
        vnop = yield sepBy(named_argument, singlelinespaces()) # pylint: disable=unused-variable
    defs = yield sepBy1(param_def, singlelinespaces())
    return defs

@generate
def param_handler():
    """parse a param handler"""
    yield keyword("on")
    yield normalspaces()
    hname = yield var_name()
    yield normalspaces()
    action = yield keyword("set|get|preset|postset")
    yield normalspaces()
    other = yield var_name()
    yield normalspaces()
    yield keyword("do")
    yield normalspaces()
    expr = yield expression
    return s.Construct(s.PARAMETERS_HANDLER, hname, action, other, expr)

@generate
def param_clause():
    """parse a param clause"""
    clause = yield (
        param_handler ^
        param_defs
        )
    return clause

@generate
def parameters_def():
    """parse a parametes def"""
    yield keyword("parameters")
    yield normalspaces()
    vname = yield var_name()
    yield normalspaces()
    vnop = yield sepBy(named_argument, normalspaces())
    yield normalspaces()
    yield string("(")
    yield normalspaces()
    paramclauses = yield sepBy1(param_clause, end_of_statement) # normalspaces())
    yield normalspaces()
    yield string(")")
    return s.Construct(s.PARAMETERS_DEF, vname, vnop, paramclauses)

# ----- plugin

@generate
def plugin_clause():
    """parse a plugin clause"""
    clause = yield (local_decl ^
        function_def ^
        struct_def ^
        parameters_def ^
        mousetool_def ^
        rollout_def ^
        on_map_do_handler ^
        on_clone_do_handler ^
        on_do_handler)
    return clause

@generate
def plugin_def():
    """parse a plugin def"""
    yield keyword("plugin")
    yield normalspaces()
    vname = yield var_name()
    yield normalspaces()
    vname = yield var_name()
    yield normalspaces()
    vnop = yield sepBy(named_argument, normalspaces())
    yield normalspaces()
    yield string("(")
    yield normalspaces()
    pluginclauses = yield sepBy(plugin_clause, normalspaces())
    yield normalspaces()
    yield string(")")
    return s.Construct(s.PLUGIN_DEF, vname, vnop, pluginclauses)

# ----------- attributes
@generate
def attributes_clause():
    """parse an attributes clause"""
    clause = yield (local_decl ^
        global_decl ^
        parameters_def ^
        rollout_def ^
        function_def ^
        on_do_handler)
    return clause

@generate
def attributes_def():
    """parse an attributes def"""
    yield keyword("attributes")
    yield normalspaces()
    attrname = yield expression
    yield normalspaces()
    vnop = yield sepBy(named_argument, normalspaces())
    yield normalspaces()
    yield string("(")
    yield normalspaces()
    attributesclauses = yield sepBy(attributes_clause, end_of_statement)
    yield normalspaces()
    yield string(")")
    return s.Construct(s.ATTRIBUTES_DEF, attrname, vnop, attributesclauses)

# when

@generate
def when_handler():
    """parse a when handler"""
    @generate
    def when_attribute():
        # pylint: disable=line-too-long
        yield keyword("when")
        yield normalspaces()
        kw = yield keyword("topology|geometry|names?|transform|select|parameters|subAnimStructure|controller|children|any")
        yield normalspaces()
        objects = yield factor
        yield normalspaces()
        yield keyword("changes?")
        yield normalspaces()
        vnop = yield sepBy(named_argument, normalspaces())
        yield normalspaces()
        objparam = yield optional(factor)
        yield normalspaces()
        yield keyword("do")
        yield normalspaces()
        expr = yield expression
        return s.Construct(s.WHEN_ATTRIBUTE, kw, objects, vnop, objparam, expr)

    @generate
    def when_objects():
        yield keyword("when")
        yield normalspaces()
        obj = yield factor
        yield normalspaces()
        yield keyword("deleted")
        yield normalspaces()
        vnop = yield sepBy(named_argument, normalspaces())
        yield normalspaces()
        objparam = yield optional(factor)
        yield normalspaces()
        yield keyword("do")
        yield normalspaces()
        expr = yield expression
        return s.Construct(s.WHEN_OBJECTS, obj, vnop, objparam, expr)

    when_thing = yield when_attribute ^ when_objects
    return when_thing

# ############## PROGRAM
@generate
def end_of_statement():
    '''Statement separator'''
    yield singlelinespaces()
    yield sepBy(statementsep(), singlelinespaces())
    yield singlelinespaces()

@mark
@generate
def program_step():
    """parse a program separator"""
    expr = yield expression
    return expr

@generate
def program():
    '''Parse an mxs program'''
    statements = yield sepBy(
        program_step,
        end_of_statement)
    yield many(statementsep())
    def mark_location(sloc):
        sloc[1].set_start_end(sloc[0], sloc[2])
        return sloc[1]
    lstatements = list(map(mark_location, statements))
    return s.Construct(s.PROGRAM, lstatements)

@generate
def expr_seq():
    '''Parse a expr_seq in parens'''
    yield lparen
    yield normalspaces()
    statements = yield program
    yield normalspaces()
    yield rparen
    return s.Construct(s.EXPR_SEQ, statements)

@mark
@generate
def file():
    """Parse the topmost file level"""
    yield normalspaces()
    p = yield program
    yield normalspaces()
    return p
