"""
Contains the logic for the model's line items.
"""

from . import virtualsheet, helpers
from . import cell

class LineItem:
    """Core logic for individual line items in the model."""

    def __init__(self, name, periods):
        """Initialises the line item."""
        self.name = name
        self.cell = [cell.Cell() for _ in range(periods)]
        return

    def equals(self, operation):
        """Sets the line item to equal the output of some operation."""
        self.cell = operation
        return self

    def dt(self, offset_amount: int):
        """
        Offsets a line item by a set amount.

        A typical example of where this function would be used is in a corkscrew
        formula such as a end-of-month to start-of-month carry forward or a
        month-on-month difference in an equation.

        Positive values indicate a forward-looking offset whereas negative
        values indicate a backward-looking offset.

        Note that any undefined cells will still create a Cell-like object, but
        this object will throw an exception if you try to do anything with it.
        These missing entries have to be defined manually using the __setitem__
        method.
        """
        return self  # TODO 

    @property
    def next(self):
        """Handy shorthand property to select the next month's values."""
        return self.dt(+1)

    @property
    def previous(self):
        """Handy shorthand property to select the previous month's values."""
        return self.dt(-1)

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


class LineItemSection:
    """Formats the line item into a nice looking "table" (aka section)."""
    periods = 36  # HACK: Make a set number of periods while I think.

    def __init__(self):
        """Creates the line item storage."""
        self.lineitems = []
        return

    def addLineItem(self, name):
        """Creates a line item."""
        item = LineItem(
            name=name,
            periods=self.periods
        )
        self.lineitems.append(item)
        return item

    def compile(self):
        """Compiles the line items into a VirtualWorksheet."""
        section = virtualsheet.VirtualWorksheet()
        for i, item in enumerate(self.lineitems):
            c2r = helpers.coords2ref
            section[c2r((i, 0))] = item.name
            for j, entry in enumerate(item.cell):
                # TODO: Add a method that does this remembering of pks automatically.
                section[c2r((i, j+2))] = f"={entry.value}"
                section.pks[str(entry.pk)] = c2r((i, j+2))
        return section
