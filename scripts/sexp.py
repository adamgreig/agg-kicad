"""
sexp.py
Copyright 2015-2022 Adam Greig
Licensed under the MIT licence, see LICENSE file for details.

S-Expression parser/emitter
"""

import re
from decimal import Decimal


def parse(sexp, parse_nums=False):
    """
    Parse an S-expression into Python lists.
    """
    r = [[]]
    token = None
    quote = False
    quoted = False
    empty_string = object()
    for c in sexp:
        if c == '(' and not quote:
            r.append([])
        elif c in (')', ' ', '\n') and not quote:
            if token is not None and (token == empty_string or token.strip() != ""):
                if token == empty_string:
                    token = ""
                else:
                    token = token.strip()
                if parse_nums and not quoted:
                    if re.match("^[\+\-]?[0-9]+$", token):
                        token = int(token)
                    elif re.match("^[\+\-]?[0-9]+\.?[0-9]*$", token):
                        try:
                            token = float(token)
                        except ValueError:
                            pass
                r[-1].append(token)
            token = None
            quoted = False
            if c == ')':
                t = r.pop()
                r[-1].append(t)
        elif c == '"' and (token is None or token[-1] != '\\'):
            quote = not quote
            if token and not quote:
                quoted = True
            if not token and not quote:
                token = empty_string
        else:
            if token is None:
                token = ''
            token += c
    return r[0][0]


def generate(sexp, depth=0):
    """Turn a list of lists into an s-expression."""
    single_word = re.compile("^-?[a-zA-Z_*\.]+$")
    parts = []
    for idx, node in enumerate(sexp):
        if isinstance(node, str) and idx > 0 and not single_word.match(node):
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
    out = "\n{}({})".format(" "*depth*2, " ".join(parts)).splitlines()
    return "\n".join(l.rstrip() for l in out)


def find(sexp, *names):
    """Return the first node in `sexp` whose name is in `names`"""
    for child in sexp:
        if len(child) and child[0] in names:
            return child


def find_all(sexp, *names):
    """Yield all nodes in `sexp` whose name is in `names`."""
    for child in sexp:
        if len(child) and child[0] in names:
            yield child
