"""
sexp.py
Copyright 2015 Adam Greig
Licensed under the MIT licence, see LICENSE file for details.

S-Expression parser/emitter
"""

from __future__ import print_function, division

import re
from decimal import Decimal


def parse(sexp):
    """
    Parse an S-expression into Python lists.
    """
    r = [[]]
    token = None
    quote = False
    for c in sexp:
        if c == '(' and not quote:
            r.append([])
        elif c in (')', ' ', '\n') and not quote:
            if token is not None:
                r[-1].append(token)
            token = None
            if c == ')':
                t = r.pop()
                r[-1].append(t)
        elif c == '"' and (token is None or token[-1] != '\\'):
            quote = not quote
            if not token and not quote:
                token = "~"
        else:
            if token is None:
                token = ''
            token += c
    return r[0][0]


def generate(sexp, depth=0):
    """Turn a list of lists into an s-expression."""
    single_word = re.compile("^-?[a-zA-Z0-9_*\.]+$")
    parts = []
    for node in sexp:
        if isinstance(node, str) and not single_word.match(node):
            node.replace("\"", "\\\"")
            node.replace("\n", "\\n")
            node = "\"{}\"".format(node)
        if isinstance(node, (int, Decimal)):
            node = str(node)
        if isinstance(node, float):
            node = "{:.4f}".format(node)
        if isinstance(node, (list, tuple)):
            node = generate(node, depth+1)
        parts.append(node)
    return "\n{}({})".format(" "*depth*2, " ".join(parts))


def find(sexp, *names):
    """Return the first node in `sexp` whose name is in `names`"""
    for child in sexp:
        if child[0] in names:
            return child


def find_all(sexp, *names):
    """Yield all nodes in `sexp` whose name is in `names`."""
    for child in sexp:
        if child[0] in names:
            yield child
