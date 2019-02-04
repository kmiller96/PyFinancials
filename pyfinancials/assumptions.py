#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The assumptions module concerns itself with building global, or local,
assumptions in the model. Good examples of this would be a global assumption
such as the principle on a loan or the discount rate or a local assumption such
as the interest rate per annum on a particular loan.
"""

from . import virtualsheet, helpers
from . import cell


class Assumption:
    """An individual assumption in a model.

    The `Assumption` object behaves similarly to a `LineItem` object. The key
    differences come down to the fact that an assumption can't reference
    previous or future ideals of itself (given that it is a fixed value).

    Attributes:
        name (str): The name of the assumption, which will be listed alongside
            the input in the Excel workbook.
        value: The starting value of the assumption. Typically this would be the
            mean-case or the mode-case of a model.
        periods (int): The number of entries. Currently this attribute is
            required, but future versions will infer this value automatically.
    """

    def __init__(self, name, value, periods):
        self.name = name
        self.value = value
        self._cell = [cell.Cell()] * periods # HACK: Makes identical copies of the same cell reference
        return

    def equals(self, operation):
        """Sets the assumption to be equal to the output of some operation.

        Args:
            operation (Cell): A `Cell` object. The typical way this is passed
                into the method is through a `Cell` operation.

        Returns:
            Self, enabling equals to be set during initialisation.
        """
        self._cell = operation
        return self

    def __add__(self, other):
        return [x+y for x,y in zip(self._cell, other._cell)]
    def __sub__(self, other):
        return [x-y for x,y in zip(self._cell, other._cell)]
    def __mul__(self, other):
        return [x*y for x,y in zip(self._cell, other._cell)]
    def __floordiv__(self, other):
        return [x//y for x,y in zip(self._cell, other._cell)]
    def __truediv__(self, other):
        return [x/y for x,y in zip(self._cell, other._cell)]
    def __mod__(self, other):
        return [x%y for x,y in zip(self._cell, other._cell)]
    def __pow__(self, other):
        return [x**y for x,y in zip(self._cell, other._cell)]


class AssumptionsTable:
    """A wrapper around the `Assumption` class which groups them into a table.

    The `Assumption` class is relatively low-level. Without wrapper classes such
    as this, the user would have to define where the assumptions end up in the
    final notebook. This class has the benefit of handling that formatting.

    Attributes:
        assumptions (list): An ordered list of assumptions, which are stored in
            the same order they were initialised.
    """
    periods = 36  # HACK: Make a set number of periods while I think.

    def __init__(self):
        self.assumptions = []
        return

    def addAssumption(self, name, initial_value=0):
        """Creates an assumption.

        Args:
            name (str): the name of the assumption, which will be inserted into
                the final workbook alongside the input field.
            initial_value (optional): Defines an initial value for the
                assumption. It defaults to 0.

        Returns:
            (Assumption): An instance of the `Assumption` object.
        """
        assumpt = Assumption(
            name=name,
            value=initial_value,
            periods=self.periods
        )
        self.assumptions.append(assumpt)
        return assumpt

    def compile(self):
        """Compiles the assumptions table into a VirtualWorksheet.

        Although nothing becomes "used" or "corrupted" by calling this method
        prematurely, often the user shouldn't be concerned with calling this
        method. Instead it is better to let the engine handle when to call this
        and what to do with it.

        Returns:
            (VirtualWorksheet): An instance of the `VirtualWorksheet` class.
        """
        table = virtualsheet.VirtualWorksheet()
        for i, assumpt in enumerate(self.assumptions):
            c2r = helpers.coords2ref
            table[c2r((i, 0))] = assumpt.name
            # TODO: Add a method that does this remembering of pks automatically.
            table[c2r((i, 1))] = f"={assumpt.value}"
            table.pks[str(assumpt.cell[0].pk)] = c2r((i, 1))
            # All of the cells have the same pk.
        return table
