#! /usr/bin/env python3
"""
Program to transfom maxscript code to python code.
"""
# pylint: disable=invalid-name,import-error, bad-continuation
import re
import os
import sys
from parsec import ParseError
from mxs2py import mxsp
from mxs2py import pyout
from mxs2py import mxscp
from mxs2py.log import eprint
def preprocess(inputbuf:str, filename:str) -> str:
    """
    Preprocess the inputbuf, replaceing \r\n by \n, etc.
    """
    dirname = os.path.dirname(filename)
    # pretty bogus just strip out include directives (what we should do is read the
    # refernced file and insert it. Would not be more difficult but let's keep it simple for now)
    includeregex = re.compile(r'include +"([^"]*)"')
    def expandmatch(mpath:str) -> str:
        # pylint: disable=invalid-name, line-too-long
        """Read file mpath, replacing \r\n by \n and \t by four spaces and returning the resulting buffer"""
        fn = mpath[1]
        fullfn = os.path.join(dirname,fn)
        with open(fullfn, encoding="utf-8") as f:
            buf = f.read().replace("\r\n", "\n").replace("\t", "    ")
            return (mpath[0], buf)

    for path_rep in map(expandmatch, re.finditer(includeregex, inputbuf)):
        inputbuf = inputbuf.replace(path_rep[0], path_rep[1])

    return inputbuf


def topy(inputstr, file_header=None, snippet=False):
    """
    Convert some mxs inputstr to py.
    """
    eprint("------ input mxs program ----")
    eprint(inputstr)
    # we don't want to mix the comments whith the
    # syntax tree. So we parse the comments first,
    # and then the syntax tree, and keep locations
    # if we want to keep the comments when producing
    # the output we are able
    eprint("------ parse comments -------")
    comments = mxscp.anycomment.parse(inputstr)
    eprint(comments)
    eprint("------ replace comments with white space")
    stripped = mxscp.blank_comments(inputstr, comments)
    eprint(stripped)
    eprint("------- parse tree ------")
    parsed = mxsp.file.parse(stripped)
    eprint(parsed[1])
    lines = stripped.split("\n")
    numlines = len(lines)
    output = pyout.out_py(parsed[1], comments, file_header, snippet)
    parsedlines, dummy = parsed[2]
    parsedlines = parsedlines + 1
    error = None
    if parsedlines < numlines:
        error = f"partial parse parsedlines = {parsedlines}, numlines = {numlines} {parsed}\n"
        toreparse = '\n'.join(lines[parsedlines:])
        try:
            mxsp.program_step.parse(toreparse)
        except ParseError as e:
            error = f"{error}\n\n{e}\n\nin:\n\n<pre>{toreparse}</pre>"

    eprint("------- output ----------")
    eprint(output)
    eprint("------- done ----------")
    return (output, error)

def main():
    """
    Main program
    All (optional) args are file name.
    If no args are provided the code operates on stdin.
    """
    if len(sys.argv) > 1:
        for fname in sys.argv[1:]:
            with open(fname, encoding="utf-8") as f:
                buf = f.read().replace("\r\n", "\n")
                buf = preprocess(buf, fname)
                with open("outfile", "w", encoding="utf-8") as of:
                    of.write(buf)
                (output, error) = topy(buf, f"Automatically converted {fname}")
                if error is not None:
                    sys.exit(-1)
                print(output)
    else:
        inputstr = sys.stdin.read()
        (output, error) = topy(inputstr, "Automatically converted stdin")
        if error is not None:
            sys.exit(-1)
        print(output)
        sys.exit(0)

if __name__ == "__main__":
    main()
