"""
Define the limitations of the translator.
When something is not fully implemented, or if the translator knows
that it cannot deal with a situation it adds these explanations in the
generated code.
"""
# pylint: disable=bad-continuation

L1 = "L1"
L2 = "L2"
L3 = "L3"
L4 = "L4"
L5 = "L5"
L6 = "L6"
L7 = "L7"
L8 = "L8"
L9 = "L9"
L10 = "L10"
L11 = "L11"

LIMITATIONS = {
    L1:
"""Passing a parameter by reference to a maxscript function may fail.
in maxscript we can do:
    myfunction &a
This will currently be transalated to python as:
    myfunciton(pymxs.byref(a))
But should instead be translated as (if a is not yet defined):
    a=None
    myfunciton(byref(a))
Workaround: add a=None manually before the call if a is not defined
""",

    L2:
"""rt.free cannot operate on python strings because they are immutable
in maxscript we can do:
    a = "aaa"
    b = a
    free a
    print b -- will display ""
this means that the string itself has been emptied. But python strings
    are immutable and pymxs automatically converts maxscript strings
    to python strings in most situations (so expect rt.free to never work
    from a python program)
Workaround:
    in some cases, setting the string to "" may work depending on
    the logic of the program
""",
   L3:
"""
in maxscript you can "collect" the results of a for loop. This means
    that each iteration produces a value, and that the list of values is
    returned from the loop. This is somewhat similar to a list
    comprehension in python but max2py does not support this yet.
Workaround:
    Hand translation is needed, so something like this:
        for i = 1 to 10 collect i * 3
    Needs to be translated to
        [i * 3 for i in range(1, 11)]
""",
    L4:
"""
in maxscript, structs can have event handlers:
    struct foo2
    (
        A = 1,
        B = 3,
        fn error = throw "ZZZ",
        on create do format "Struct Created: %\n" this,
        on clone do format "Struct Cloned: %\n" this
    )
the translation of the these handlers to python code
    is not yet supported.
Workaround:
    - in the case of on create, the code could be added to the constructor
    - in other cases (clone) translation to python is more difficult
""",
    L5:
"""
maxscript code may use variable names that are reserved keywords in
python. To avoid syntax errors in the generated python code, the capitalization
of these names is changed. For example yield will be transformed to yIELD.
This will not impact calls into pymxs.runtime because on the maxscript side
things are case insensitive.
""",
    L6:
"""
(broken, limited support)
macroscripts use special MAXScript syntax (not a library call). They
are supported in python by code that internally generates maxscript
and then evaluates it. This code is in a very early form and does not
work in most situations.
""",
    L7:
"""
(broken, very limited support)
rollouts use special MAXScript syntax (not a library call). They
are supported in python by code that internally generates maxscript
and then evaluates it. This code is in a very early form and does not
work in most situations.
""",
    L8:
"""
(broken, very limited support)
plugins use special MAXScript syntax (not a library call). They
are supported in python by code that internally generates maxscript
and then evaluates it. This code is in a very early form and does not
work in most situations.
""",
    L9:
"""
(broken, very limited support)
attributes use special MAXScript syntax (not a library call). They
are supported in python by code that internally generates maxscript
and then evaluates it. This code is in a very early form and does not
work in most situations.
""",
    L10:
"""
(broken, very limited support)
tools use special MAXScript syntax (not a library call). They
are supported in python by code that internally generates maxscript
and then evaluates it. This code is in a very early form and does not
work in most situations.
""",
     L11:
"""
Unexpected construct in the syntax tree. Ignored. Nothing to do for
the user.
"""
}
