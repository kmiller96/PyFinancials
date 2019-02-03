#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Implements the primary key store.
"""

import re
import uuid

PK_TAGS_LEFT = '<<<'
PK_TAGS_RIGHT = '>>>'


def find_pks(string):
    """Looks for primary keys and returns them."""
    try:
        left_tags = [m.start() for m in re.finditer(PK_TAGS_LEFT, string)]
        right_tags = [m.start() for m in re.finditer(PK_TAGS_RIGHT, string)]
        tag_slices = [(l, r+len(PK_TAGS_RIGHT)) for l,r in zip(left_tags, right_tags)]
        substrings = [string[l:r] for l,r in tag_slices]
    except TypeError as e:  # Not a string i.e. a defined cell.
        return []  # That's okay - pass through an empty find.
    else:
        return substrings

def parse_pk(string):
    """Removes the formatting on a UUID."""
    return string.replace(PK_TAGS_LEFT, "").replace(PK_TAGS_RIGHT, "")


class PrimaryKey:
    """Creates a unique identifier for the final compiler."""

    def __init__(self):
        """Stores the pk parameters."""
        self.id = uuid.uuid4().hex  # Get hexidecimal string only
        return

    def __str__(self):
        """Runs the standard, uniform styling of the pk."""
        return f"{PK_TAGS_LEFT}{self.id}{PK_TAGS_RIGHT}"

    def __eq__(self, other): return self.id == other.id
    def __ne__(self, other): return self.id != other.id
    def __lt__(self, other): return self.id <  other.id
    def __gt__(self, other): return self.id >  other.id
    def __le__(self, other): return self.id <= other.id
    def __ge__(self, other): return self.id >= other.id
