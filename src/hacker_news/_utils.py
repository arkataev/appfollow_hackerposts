from typing import List

from . import dataclasses as dc


def merge_longest_posts(a: List[dc.HackerPost], b: List[dc.HackerPost], limit=0):
    """
    Merge two lists of posts maintaining posts time order

    :param limit:   maximum length of resulting list, if not applied,
                    than maximum list length applied
    """
    i = j = 0
    m = []

    while len(m) <= (limit or len(a) + len(b)):
        if j == len(b) or (i < len(a) and a[i].time <= b[j].time):

            if m and m[-1].id == a[i].id:
                i += 1
                continue

            m.append(a[i])
            i += 1
        else:

            if m and m[-1].id == b[j].id:
                j += 1
                continue

            m.append(b[j])
            j += 1

    return m
