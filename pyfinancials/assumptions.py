#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Contains the Assumption object and any other related logic.
"""

from . import virtualsheet, helpers
from . import cell


class Assumption:
    """An individual assumption."""

    def __init__(self, name, value, periods):
        """Stores the data about the assumption."""
        self.name = name
        self.value = value
        self.cell = [cell.Cell()] * periods # HACK: Makes identical copies of the reference
        return

    def equals(self, operation):
        """Sets the assumption to be equal to the output of some operation."""
        self.cell = operation
        return self

    def __add__(self, other):
        return [x+y for x,y in zip(self.cell, other.cell)]
    def __sub__(self, other):
        return [x-y for x,y in zip(self.cell, other.cell)]
    def __mul__(self, other):
        return [x*y for x,y in zip(self.cell, other.cell)]
    def __floordiv__(self, other):
        return [x//y for x,y in zip(self.cell, other.cell)]
    def __truediv__(self, other):
        return [x/y for x,y in zip(self.cell, other.cell)]
    def __mod__(self, other):
        return [x%y for x,y in zip(self.cell, other.cell)]
    def __pow__(self, other):
        return [x**y for x,y in zip(self.cell, other.cell)]


class AssumptionsTable:
    """Formats the assumptions into a nice-looking table."""
    periods = 36  # HACK: Make a set number of periods while I think.

    def __init__(self):
        """Creates the assumptions storage."""
        self.assumptions = []
        return

    def __str__(self):
        """Builds the primary key string."""
        return self.pk

    def addAssumption(self, name, initial_value=0):
        """Creates an assumptions."""
        assumpt = Assumption(
            name=name,
            value=initial_value,
            periods=self.periods
        )
        self.assumptions.append(assumpt)
        return assumpt

    def compile(self):
        """Compiles the assumptions into a VirtualWorksheet."""
        table = virtualsheet.VirtualWorksheet()
        for i, assumpt in enumerate(self.assumptions):
            c2r = helpers.coords2ref
            table[c2r((i, 0))] = assumpt.name
            # TODO: Add a method that does this remembering of pks automatically.
            table[c2r((i, 1))] = f"={assumpt.value}"
            table.pks[str(assumpt.cell[0].pk)] = c2r((i, 1))
            # All of the cells have the same pk.
        return table
