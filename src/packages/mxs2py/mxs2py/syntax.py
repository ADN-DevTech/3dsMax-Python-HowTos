"""
Definition of the various syntax constructs in the  syntax tree.
"""
ARRAY = "ARRAY"
ASSIGNMENT = "ASSIGNMENT"
BITARRAY = "BITARRAY"
BITARRAY_RANGE = "BITARRAY_RANGE"
CALL = "CALL"
CASE_EXPR = "CASE_EXPR"
CASE_ITEM = "CASE_ITEM"
COMPUTATION = "COMPUTATION"
CONTEXT_ABOUT = "CONTEXT_ABOUT"
CONTEXT_AT = "CONTEXT_AT"
CONTEXT_EXPR = "CONTEXT_EXPR"
CONTEXT_IN_COORDSYS = "CONTEXT_IN_COORDSYS"
CONTEXT_IN_NODE = "CONTEXT_IN_NODE"
CONTEXT_WITH = "CONTEXT_WITH"
DO_LOOP = "DO_LOOP"
DECL = "DECL"
FOR_LOOP = "FOR_LOOP"
FOR_LOOP_FROM_TO_SEQUENCE = "FOR_LOOP_FROM_TO_SEQUENCE"
FUNCTION_DEF = "FUNCTION_DEF"
FUNCTION_RETURN = "FUNCTION_RETURN"
GLOBAL = "GLOBAL"
VAR_NAME = "VAR_NAME"
IF_EXPR = "IF_EXPR"
LOCAL = "LOCAL"
LOCAL_DECL = "LOCAL_DECL"
GLOBAL_DECL = "GLOBAL_DECL"
LOOP_CONTINUE = "LOOP_CONTINUE"
LOOP_EXIT = "LOOP_EXIT"
MAX_COMMAND = "MAX_COMMAND"
MOUSETOOL_DEF = "MOUSETOOL_DEF"
NAME = "NAME"
ARGUMENT = "ARGUMENT"
NAMED_ARGUMENT = "NAMED_ARGUMENT"
NUMBER = "NUMBER"
OPERATOR = "OPERATOR"
PATH_NAME = "PATH_NAME"
PARAMETERS_DEF = "PARAMETERS_DEF"
PARAMETERS_HANDLER = "PARAMETERS_HANDLER"
PERSISTENTGLOBAL = "PERSISTENTGLOBAL"
ATTRIBUTES_DEF = "ATTRIBUTES_DEF"
POINT2 = "POINT2"
POINT3 = "POINT3"
POINT4 = "POINT4"
PROGRAM = "PROGRAM"
PROPERTY = "PROPERTY"
PROPERTY_ACCESSOR_INDEX = "PROPERTY_ACCESSOR_INDEX"
PROPERTY_ACCESSOR_MEMBER = "PROPERTY_ACCESSOR_MEMBER"
QUESTION = "QUESTION"
RCMENU_ITEM = "RCMENU_ITEM"
RCMENU_HANDLER = "RCMENU_HANDLER"
RCMENU_DEF = "RCMENU_DEF"
REFERENCE = "REFERENCE"
ROLLOUT_CLAUSE = "ROLLOUT_CLAUSE"
ROLLOUT_DEF = "ROLLOUT_DEF"
ROLLOUT_GROUP = "ROLLOUT_GROUP"
ROLLOUT_HANDLER = "ROLLOUT_HANDLER"
ROLLOUT_ITEM = "ROLLOUT_ITEM"
SET_CONTEXT = "SET_CONTEXT"
SINGLECOMMENT = "SINGLECOMMENT"
STRING = "STRING"
STRUCT_DEF = "STRUCT_DEF"
STRUCT_MEMBER_ASSIGN = "STRUCT_MEMBER_ASSIGN"
STRUCT_MEMBER_DATA = "STRUCT_MEMBER_DATA"
STRUCT_MEMBER_METHOD = "STRUCT_MEMBER_METHOD"
EXPR_SEQ = "EXPR_SEQ"
THROW = "THROW"
TIME = "TIME"
SMPTE_TIME = "SMPTE_TIME"
TRY_EXPR = "TRY_EXPR"
UNARY_MINUS = "UNARY_MINUS"
UNARY_NOT = "UNARY_NOT"
VARIABLE_DECL = "VARIABLE_DECL"
WHEN_ATTRIBUTE = "WHEN_ATTRIBUTE"
WHEN_OBJECTS = "WHEN_OBJECTS"
WHILE_LOOP = "WHILE_LOOP"
MACROSCRIPT_DEF = "MACROSCRIPT_DEF"
ON_DO_HANDLER = "ON_DO_HANDLER"
ON_CLONE_DO_HANDLER = "ON_CLONE_DO_HANDLER"
ON_MAP_DO_HANDLER = "ON_MAP_DO_HANDLER"
MACROSCRIPT_CLAUSE = "MACROSCRIPT_CLAUSE"
PLUGIN_DEF = "PLUGIN_DEF"
UTILITY_DEF = "UTILITY_DEF"

# the following syntax appears as a result of transforming
# the mxs tree. So this syntax does not come from mxs but instead
# is python syntax generated during tree transformation
PY_SHIM_VAR_NAME = "PY_SHIM_VAR_NAME"
PY_BUILTIN_VAR_NAME = "PY_BUILTIN_VAR_NAME"
PY_RT_VAR_NAME = "PY_RT_VAR_NAME"
PY_NONLOCAL = "PY_NONLOCAL"
PY_GLOBAL = "PY_GLOBAL"
PY_MACROSCRIPT_CLASS = "PY_MACROSCRIPT_CLASS"
PY_ROLLOUT_CLASS = "PY_ROLLOUT_CLASS"
PY_PLUGIN_CLASS = "PY_PLUGIN_CLASS"
PY_ATTRIBUTES_CLASS = "PY_ATTRIBUTES_CLASS"
PY_TUPLE = "PY_TUPLE"
PY_NOVAR = "PY_NOVAR"

# levels of comments
COMMENT_WARNING = "WARNING"
COMMENT_ERROR= "ERROR"
COMMENT_INFO = "INFO"


class Construct:
    """Syntactical construct"""
    def __init__(self, construct, *args):
        self.construct = construct
        self.args = list(args)
        self.start = None
        self.end = None
        self.comments = []

    def set_start_end(self, start, end):
        """Set delimitation position of the construct"""
        self.start = start
        self.end = end

    # pylint: disable=unused-argument
    def warning_comment(self, new_comment, addendum=None):
        """Add a warning comment"""
        self.comments.append((COMMENT_WARNING, new_comment))
    def error_comment(self, new_comment, addendum=None):
        """Add an error comment"""
        self.comments.append((COMMENT_ERROR, new_comment))
    def info_comment(self, new_comment, addendum=None):
        """Add an info comment"""
        self.comments.append((COMMENT_INFO, new_comment))

    def __str__(self):
        """Convert to a string"""
        tab = "."
        def indent(lines):
            return "\n".join(map (lambda toindent : tab + toindent, lines.split("\n")))

        def stritem(i):
            if isinstance(i, list):
                return "(list)\n" + indent("\n".join(map(stritem, i)))
            if isinstance(i, tuple):
                return "(tuple)\n" + indent("\n".join(map(stritem, list(i))))
            return str(i)

        construct = (f"{self.construct}\n"
                if self.start is None
                else f"{self.construct} {self.start} {self.end}\n")
        return (
            construct +
            indent("\n".join(
                map(
                    stritem,
                    self.args)
                ))
            )
