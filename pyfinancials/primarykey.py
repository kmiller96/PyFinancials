#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The entire engine hinges upon invarient UIDs - rather than cell references - to
empower the lego-esque building of financial models. To help encapsulate
behaviour, and make the keys "smart", the PrimaryKey class was implemented.
"""

import re
import uuid

PK_TAGS_LEFT = '<<<'
PK_TAGS_RIGHT = '>>>'


def find_pks(string):
    """Looks for primary keys in a string and returns them.

    PyFinancials' cell definitions contain UIDs which enable them to eventually
    be compiled into Excel references. This function identifies which UIDs are
    present.

    Args:
        string (str): The Excel formula.

    Returns:
        (list): A collection of the UID strings including formatting.
    """
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
    """Removes the formatting on a UUID.

    Examples:
        >>> parse_pk("<<<7134ab2ff9eac11>>>")
        7134ab2ff9eac11

    Args:
        string (str): The UID with formatting.

    Returns:
        (str): The UID without formatting.
    """
    return string.replace(PK_TAGS_LEFT, "").replace(PK_TAGS_RIGHT, "")


class PrimaryKey:
    """A unique identifier with some handy utilities.

    The reason this class exists over just using a UID comes down to the
    encapsulation. For the moment a UID is being used, but eventually we might
    want to insert more expressive UIDs without changing much else of the
    project.

    Attributes:
        id (uuid.uuid4): A hexidecimal representation of the UUID.
    """

    def __init__(self):
        self.id = uuid.uuid4().hex  # Get hexidecimal string only
        return

    def __str__(self):
        """Returns the ID with the standard, uniform styling of the pk."""
        return f"{PK_TAGS_LEFT}{self.id}{PK_TAGS_RIGHT}"

    def __eq__(self, other): return self.id == other.id
    def __ne__(self, other): return self.id != other.id
    def __lt__(self, other): return self.id <  other.id
    def __gt__(self, other): return self.id >  other.id
    def __le__(self, other): return self.id <= other.id
    def __ge__(self, other): return self.id >= other.id
