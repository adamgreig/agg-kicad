"""
sexp.py
Copyright 2015 Adam Greig

S-Expression parser/emitter
"""

import re
from decimal import Decimal


def sexp_parse(sexp):
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
        elif c == '"':
            quote = not quote
            if not token and not quote:
                token = "~"
        else:
            if token is None:
                token = ''
            token += c
    return r[0][0]


def sexp_generate(sexp, depth=0):
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
            node = sexp_generate(node, depth+1)
        parts.append(node)
    return "\n{}({})".format(" "*depth*2, " ".join(parts))
