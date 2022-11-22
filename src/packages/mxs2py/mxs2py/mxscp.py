"""
Parsing of comments (and only comments)
in maxscript files. The goal with this (to be revisited maybe).
is to leave the comments out of the syntax tree. Our first processing
step consists in stripping out the comments but keeping the info or
where they are in the original source file.
"""
# pylint: disable=invalid-name,import-error
from parsec import * # pylint: disable=wildcard-import,redefined-builtin, unused-wildcard-import

SINGLE="SINGLE"
MULTI="MULTI"
STRING="STRING"
OTHER="OTHER"

@mark
@generate
def singlecomment():
    """parse a single mxs comment"""
    c = yield regex(r"--.*$", re.MULTILINE)
    return (SINGLE, c[2:])

@mark
@generate
def multicomment():
    """parse a multiline mxs comment"""
    z = yield regex("/\\*.*?\\*/",re.MULTILINE | re.DOTALL)
    return (MULTI, z[2:-2])

@mark
@generate
def qstring():
    '''Parse quoted string.'''
    @generate
    def normal():
        body = yield regex(r'"([^"\\]|\\.)*"')
        return body

    @generate
    def verbatim():
        body = yield regex(r'@"[^"]*"')
        return body

    body = yield verbatim | normal

    return (STRING, body)


@mark
@generate
def other():
    """Parse non commment section"""
    o = yield regex('([^-/"@]|-(?!-)|/(?!\\*))*', re.MULTILINE | re.DOTALL)
    return (OTHER, o)

@generate
def anycomment():
    """Parse a comment, single or multiline"""
    yield other
    c = yield sepBy(
        singlecomment^multicomment^qstring,
        other)
    yield other
    return c

def blank_comments(inp, comments):
    """Replace comments by spaces"""
    lines = inp.split('\n')

    comments = list(filter(lambda c: c[1][0] in [SINGLE, MULTI], comments))

    def blankline(line, number):
        for c in comments:
            (fl,fc)=c[0]
            (tl,tc)=c[2]
            if tl >= number >= fl:
                f = fc if number == fl else 0
                t = tc if number == tl else len(line)
                line = line[0:f] + " " * (t-f) + line[t:]
        return line

    return '\n'.join([blankline(l,i) for i,l in enumerate(lines)])
