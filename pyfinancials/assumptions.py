"""
Adds the assumptions object, which is used on the assumptions sheet and in
assumption sections for calculation sheets.
"""

import openpyxl as pyxl
from . import section


class _AssumptionOperators:
    """Implements the operator logic for assumptions."""

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


class Assumption(_AssumptionOperators):
    """Class that handles the assumptions defined."""

    def __init__(self, starting_value):
        """Stores the passed values internally into the class."""
        self.value = starting_value
        return


class AssumptionsSection(section.Section):
    """Handles the user creating assumptions in the model."""

    def __init__(self):
        """Builds the assumptions section."""
        self._assumptions = {}
        return

    def __getitem__(self, key):
        """Access any defined assumptions from the object."""
        return self._assumptions[key]

    def __setitem__(self, key, value):
        """Access any defined assumptions from the object."""
        self._assumptions[key].value = value
        return

    def addAssumption(self, pretty_name, initial_value=0):
        """Creates an assumptions section."""
        self._assumptions[pretty_name] = Assumption(initial_value)
