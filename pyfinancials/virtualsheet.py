"""
Builds the VirtualWorksheet object - a core concept for PyFinancials.
"""

from . import helpers

class VirtualWorksheet:
    """
    Creates a memory-only worksheets in a workbook.

    This class acts similar to openpyxl's worksheets. It enables memory-only
    worksheets to be built in a modular and extendable manner. This has the
    benefit of a program creating excel building-blocks of sections, tables
    and diagrams.
    """

    def __init__(self):
        """Initialises the worksheet."""
        self.worksheet = {}
        self.pks = {}
        return

    def __getitem__(self, coordinate):
        """Enables querying a notebook with openpyxl notation."""
        helpers.assert_valid_cell_reference(coordinate)
        return self.worksheet[coordinate]

    def __setitem__(self, coordinate, value):
        """Sets a cell to a particular value."""
        helpers.assert_valid_cell_reference(coordinate)
        self.worksheet[coordinate] = value
        return

    def compile(self):
        """Compiles the VirtualWorksheet into a openpyxl sheet."""
        # Apply styling
        return self  # WIP!

    def insert(self, virtual_sheet, anchor_ref='A1'):
        """Inserts a VirtualWorksheet object into this VirtualWorksheet."""
        compiled_sheet = virtual_sheet.compile()
        anchor_row, anchor_col = helpers.ref2coords(anchor_ref)

        # Update the virtual worksheet locations.
        for loc, val in compiled_sheet.items():
            offset_loc = helpers.offset(loc, anchor_row, anchor_col)
            self.worksheet[offset_loc] = val

        # Update the other pks locations and add to this pks
        for pk, loc in compiled_sheet.pks.items():
            offset_loc = helpers.offset(loc, anchor_row, anchor_col)
            self.pks[pk] = offset_loc
        return

    def items(self):
        """Nice utility wrapper around the `items` generator."""
        return self.worksheet.items()
