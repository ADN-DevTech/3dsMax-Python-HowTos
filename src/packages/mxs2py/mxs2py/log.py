"""
Simple logging utility (to stderr)
"""
import sys
def eprint(*args, **kwargs):
    """print to a file"""
    print(*args, file=sys.stderr, **kwargs)
