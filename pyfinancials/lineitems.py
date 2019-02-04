#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module concerns itself with line items. This includes things such as
individual line items and line item sections. Typical examples of this would be
end-of-month profit, interest accumulated or the number of customers.
"""

from . import virtualsheet, helpers
from . import cell

class LineItem:
    """Core logic for individual line items in the model.

    The `LineItem` object behaves similarly to a `Assumption` object. The key
    differences come down to the fact that an assumption can't reference
    previous or future ideals of itself (given that it is a fixed value) where
    a LineItem can - or will be able to eventually.

    Todo:
        Implement the `dt` method!

    Attributes:
        name (str): The name of the line item, which will be listed alongside
            the line in the Excel workbook.
        periods (int): The number of entries. Currently this attribute is
            required, but future versions will infer this value automatically.
    """

    def __init__(self, name, periods):
        self.name = name
        self._cell = [cell.Cell() for _ in range(periods)]
        return

    def equals(self, operation):
        """Sets the assumption to be equal to the output of some operation.

        Args:
            operation (Cell): A `Cell` object. The typical way this is passed
                into the method is through a `Cell` operation such as
                ``Cell() + Cell()``.

        Returns:
            Self, enabling equals to be set during initialisation.
        """
        self._cell = operation
        return self

    def dt(self, offset_amount: int):
        """Offsets a line item by a set amount.

        A typical example of where this function would be used is in a corkscrew
        formula such as a end-of-month to start-of-month carry forward or a
        month-on-month difference in an equation.

        Positive values indicate a forward-looking offset whereas negative
        values indicate a backward-looking offset.

        Note that any undefined cells will still create a Cell-like object, but
        this object will throw an exception if you try to do anything with it.
        These missing entries have to be defined manually using the __setitem__
        method.

        Todo:
            This entire method! It hasn't been implemented yet.

        Args:
            offset_amount (int): The amount to offset by. Positive values
                indicate a forward-looking offset whereas negative values
                indicate a backward-looking offset (e.g. +1 gets the next
                entry where as -1 gets the previous entry).

        Returns:
            Self, while a WIP.
        """
        return self  # TODO

    @property
    def next(self):
        """Handy shorthand property to select the next period's values."""
        return self.dt(+1)

    @property
    def previous(self):
        """Handy shorthand property to select the previous period's values."""
        return self.dt(-1)

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


class LineItemSection:
    """Formats the line item into a nice looking "table" (aka section).

    The `LineItem` class is relatively low-level. Without wrapper classes such
    as this, the user would have to define where the LineItems end up in the
    final notebook. This class has the benefit of handling that formatting.

    Attributes:
        lineitems (list): An ordered list of assumptions, which are stored in
            the same order they were initialised.
    """
    periods = 36  # HACK: Make a set number of periods while I think.

    def __init__(self):
        self.lineitems = []
        return

    def addLineItem(self, name):
        """Creates a line item."""
        """Creates a line item.

        Args:
            name (str): the name of the item, which will be inserted into the
                final workbook alongside the input field.

        Returns:
            (LineItem): An instance of the `LineItem` object.
        """
        item = LineItem(
            name=name,
            periods=self.periods
        )
        self.lineitems.append(item)
        return item

    def compile(self):
        """Compiles the assumptions table into a VirtualWorksheet.

        Although nothing becomes "used" or "corrupted" by calling this method
        prematurely, often the user shouldn't be concerned with calling this
        method. Instead it is better to let the engine handle when to call this
        and what to do with it.

        Returns:
            (VirtualWorksheet): An instance of the `VirtualWorksheet` class.
        """
        section = virtualsheet.VirtualWorksheet()
        for i, item in enumerate(self.lineitems):
            c2r = helpers.coords2ref
            section[c2r((i, 0))] = item.name
            for j, entry in enumerate(item.cell):
                # TODO: Add a method that does this remembering of pks automatically.
                section[c2r((i, j+2))] = f"={entry.value}"
                section.pks[str(entry.pk)] = c2r((i, j+2))
        return section
