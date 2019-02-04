#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This moduel contains functions that are used throughout the PyFinancials
package, either internally or as a part of the exposed API.
"""

import re  # NORMIES GET OUT!!

###############################
## MODULE-SPECIFIC "GLOBALS" ##
###############################

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
MAX_SHEET_ROWS = 1048576
MAX_SHEET_COLUMNS = 16384

#######################
## HELPFUL FUNCTIONS ##
#######################

def ref2coords(cell_reference):
    """Converts a cell reference to a set of coordinates (row, column).

    As per in line with most modern programming languages, the (row, column)
    tuple starts at 0. Hence 'A1' returns (0, 0).

    Examples:
        >>> ref2coords('A1')
        (0, 0)
        >>> ref2coords('AA10')
        (9, 26)

    Args:
        cell_reference (str): The excel cell reference.

    Returns:
        (tuple): A tuple of integers in the format (row, column).
    """
    column_letters = cell_reference.rstrip('0123456789')
    row = int(cell_reference[len(column_letters):]) - 1
    column = 0  # Calculated below.

    for i, letter in enumerate(column_letters[::-1]):
        alphabet_pos = ALPHABET.index(letter) + 1
        column += alphabet_pos*(26**i)
    return (row, column-1)


def coords2ref(coordinates):
    """Converts a set of coordinates to a cell reference.

    As per in line with most modern programming languages, the coordinates
    passed are indexed at 0. Hence (0, 0) returns 'A1'.

    Examples:
        >>> coords2ref((0, 0))
        'A1'
        >>> coords2ref((25, 25))
        'Z26'
        >>> coords2ref((0, 26))
        'AA1'

    Args:
        coordinates (tuple): A tuple of integers in the format (row, column).

    Returns:
        (str): The excel cell reference.
    """
    row, column = coordinates
    row, column = row+1, column+1  # Excel has a 1-index (unlike python).

    # Look and see if there are any additional letters (e.g. AB1 or AAC1).
    column_letters = ''
    for order in [2, 1]:
        divisor = 26**order
        k = column // divisor
        if k > 0:  # i.e. we need that letter.
            column_letters += ALPHABET[k-1]
            column -= k*divisor

    # Then get the final letter.
    column_letters += ALPHABET[column-1]
    return "{}{}".format(column_letters, row)


def assert_valid_cell_reference(cell_reference):
    """Asserts that the format of the cell reference is valid.

    Todo:
        Confirm that this function is being used, or where it should be used.

    Raises:
        ValueError: If the cell reference passed is not valid.

    Args:
        cell_reference (str): A potentially valid excel reference.

    Returns:
        (bool): True if the input is valid.
    """
    # First assert that it is a good input.
    r = re.compile("([a-zA-Z]+)([0-9]+)")
    if re.match(r, cell_reference) is None:
        raise ValueError(
            "The input '{}' is not a valid excel cell reference."
            .format(cell_reference)
        )

    # Now assert that the value is within a good range.
    row_index, column_index = ref2coords(cell_reference)
    if row_index > MAX_SHEET_ROWS:
        raise ValueError(
            "{} has a row reference larger than the max, {}."
            .format(cell_reference, max_rows)
        )
    elif row_index < 0:  # ref2coords('A1') => (0, 0)
        raise ValueError(
            "{} has a row reference smaller than the minimum, 1."
            .format(cell_reference)
        )
    elif column_index > MAX_SHEET_COLUMNS:
        raise ValueError(
            "{} has a column reference larger than the max, {}."
            .format(cell_reference, max_columns)
        )
    elif column_index < 0:
        raise ValueError(
            "{} has a column reference smaller than the minimum, 'A'."
            .format(cell_reference)
        )
    return True


def offset(excel_reference, offset_rows=0, offset_cols=0):
    """Offsets an excel reference by the amount specified.

    This general logic behind this function is to convert an Excel reference
    (e.g. 'A1') into a vector of (row, column) so that it can be moved with
    another relative vector, before being converted back into Excel format.

    Args:
        excel_reference (str): The excel reference you wish to offset.
        offset_rows (optional): How much to move the row reference by. Defaults
            as 0.
        offset_cols (optional): How much to move the column reference by.
            Defaults as 0.

    Returns:
        (str): An excel reference.
    """
    # TODO: Optimise this function.
    coordinate = ref2coords(excel_reference)
    new_coordinate = (
        coordinate[0] + offset_rows,
        coordinate[1] + offset_cols
    )
    return coords2ref(new_coordinate)
