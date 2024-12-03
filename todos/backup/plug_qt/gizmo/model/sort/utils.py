import re

_escape = dict(
    (c, "\\" + c)
    for c in [
        "^",
        "$",
        ".",
        "{",
        "}",
        "(",
        ")",
        "[",
        "]",
        "\\",
        "/",
        "+",
    ]
)


def score(result, line, text):
    text = text.lower()
    lower = line.lower()
    if not text:
        return 1000.0 / len(line)
    elif text == lower:
        return 1000.0
    else:
        w = len(result)
        w += len(lower) / 100.0
        w += len(line) / 1000.0
        return 1000.0 / w


def update(fltr=""):
    if fltr:
        escaped = [_escape.get(c, c) for c in fltr]
        if len(fltr) > 1:
            tmp = []
            for c in escaped[:-1]:
                tmp += [c + "[^" + c + "]*"]
            fltr = "".join(tmp)
        fltr += escaped[-1]
    return fltr


def SortRegex(astr):
    r = ""
    p = astr.lower()
    e = [_escape.get(c, c) for c in p]
    if len(p) > 1:
        r = "".join([c + "[^" + c + "]*" for c in e[:-1]])
    if len(p) > 0:
        r += e[-1]
    r = r.lower()
    return p, re.compile(r)


def SortMatch(rgx, text, line):
    l = line.lower()

    if text in line:
        if text == line:
            return 1000.0
        else:
            return 500.0 + 500.0 * len(text) / len(line)
    r = rgx.search(l)
    if r:
        s = r.end() - r.start() + 1
        s = s + (len(l) + 1) / 100.0
        s = s + (len(line) + 1) / 1000.0
        return 1000.0 / s
    return -1
