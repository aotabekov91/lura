import re
import itertools
import typing as tp
from collections import deque


def parse_tag(
    tags: tp.Union[str, tp.List[str]] = None,
) -> tp.List[tp.Tuple[str, str, str]]:
    parsed_tags = set()
    if type(tags) != list:
        tags = [
            tags,
        ]
    for tag in tags:
        key, mkey, vkey = parse_parts(tag)
        mode_part = parse_vimo(mkey)
        view_part = parse_vimo(vkey)
        key_part = parse_key(key)
        args = key_part, mode_part, view_part
        for i in itertools.product(*args):
            parsed_tags.add(i)
    return parsed_tags


def parse_parts(key: str) -> tp.Tuple[str]:
    rkey: str = key[::-1]
    idx = getIndex(rkey, opening="]", closing="[")
    if idx:
        vkey = rkey[0 + 1 : idx][::-1]
        rkey = rkey[idx + 1 :]
    else:
        vkey = "any"
    idx = getIndex(rkey, opening=")", closing="(")
    if idx:
        mkey = rkey[0 + 1 : idx][::-1]
        rkey = rkey[idx + 1 :]
    else:
        mkey = "any"
    return rkey[::-1], mkey, vkey


def parse_vimo(key: str) -> tp.List[tp.Tuple[str, str]]:
    klist = []
    alist = key.split("/")
    for key in alist:
        rkey = key[::-1]
        idx = getIndex(rkey, opening="]", closing="[")
        sub = None
        if idx:
            sub = rkey[0 + 1 : idx][::-1]
            rkey = rkey[idx + 1 :]
        else:
            sub = "any"
        sup = rkey[::-1]
        klist += [(sup, sub)]
    return klist


def parse_key(key: str) -> tp.List[str]:
    if not "{" in key:
        return key.split("/")
    else:
        klist = []
        alist = key.split("}/{")
        for i in alist:
            klist += [re.sub("[{}]", "", i)]
        return klist


def getIndex(
    astring: str,
    idx: int = 0,
    opening: str = "[",
    closing: str = "]",
) -> tp.Union[int, None]:
    if astring[idx] != opening:
        return
    d = deque()
    for k in range(idx, len(astring)):
        if astring[k] == closing:
            d.popleft()
        elif astring[k] == opening:
            d.append(astring[idx])
        if not d:
            return k
