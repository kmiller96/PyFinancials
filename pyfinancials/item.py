"""
Implements the logic for the line items.
"""

import openpyxl as pyxl

class _LineItemOperators:
    """Contains the logic for the line item operators."""

    ## IMPLEMENT THE SIMPLE OPERATORS ##
    def __add__(self, other):
        return self  # WIP!
    def __sub__(self, other):
        return self  # WIP!
    def __mul__(self, other):
        return self  # WIP!
    def __floordiv__(self, other):
        return self  # WIP!
    def __div__(self, other):
        return self  # WIP!
    def __mod__(self, other):
        return self  # WIP!
    def __pow__(self, other):
        return self  # WIP!

    ## IMPLEMENT SELF-OPERATORS (+=, -=. etc) ##
    def __iadd__(self, other):
        return self  # WIP!
    def __isub__(self, other):
        return self  # WIP!
    def __imul__(self, other):
        return self  # WIP!
    def __idiv__(self, other):
        return self  # WIP!
    def __ifloordiv__(self, other):
        return self  # WIP!
    def __imod__(self, other):
        return self  # WIP!
    def __ipow__(self, other):
        return self  # WIP!

    ## IMPLEMENT THE EQUALITY OPERATORS
    def __eq__(self, other):
        return self  # WIP!
    def __ne__(self, other):
        return self  # WIP!
    def __lt__(self, other):
        return self  # WIP!
    def __gt__(self, other):
        return self  # WIP!
    def __le__(self, other):
        return self  # WIP!
    def __ge__(self, other):
        return self  # WIP!


class LineItem(_LineItemOperators):
    """Creates a new line item - the most important part of any model."""

    def equals(self, formula_object):
        """
        Adds a new line item into the spreadsheet.

        The important concept to grasp with this method is that it does _not_
        take in a function. Rather, it takes in a special PyFinancials object
        which is then compiled down into the excel formulas.
        """
        return self

    def dt(self, offset_amount):
        """
        Offsets a line item by a set amount.

        A typical example of where this function would be used is in a corkscrew
        formula such as a end-of-month to start-of-month carry forward or a
        month-on-month difference in an equation.

        Positive values indicate a forward-looking offset whereas negative
        values indicate a backward-looking offset.
        """
        return self

    @property
    def next(self):
        """Handy shorthand property to select the next month's values."""
        return self.dt(+1)

    @property
    def previous(self):
        """Handy shorthand property to select the previous month's values."""
        return self.dt(-1)
