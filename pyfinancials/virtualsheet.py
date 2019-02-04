#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module only concerns itself with the VirtualWorksheet - a core concept for
PyFinancials.

A VirtualWorksheet can be thought of as a theoretical single-sheet workbook
stored entirely in memory. What makes the VirtualWorksheet so powerful is its
ability to act as a "lego brick" for a financial model. Tables, sections, line
items and even entire worksheets can be built and designed in a VirtualWorksheet
before having to be written to the disk.

The reason this exists is a result of the UIDs and the dynamic cell locations
pre-compilation.
"""

from . import helpers

class VirtualWorksheet:
    """Creates a memory-only worksheet.

    This class acts similar to openpyxl's worksheets. It enables memory-only
    worksheets to be built in a modular and extendable manner. This has the
    benefit of a program creating excel building-blocks of sections, tables
    and diagrams.

    Attributes:
        worksheet (dict): A dictionary of cells and their values, styling, etc.
        pks (dict): A collection of pks and the mapping to their current sheet
            location (e.g. 7145aaf1e8dd maps to 'B2' in the current
            VirtualWorksheet)
    """

    def __init__(self):
        self.worksheet = {}
        self.pks = {}
        return

    def __getitem__(self, coordinate):
        helpers.assert_valid_cell_reference(coordinate)
        return self.worksheet[coordinate]

    def __setitem__(self, coordinate, value):
        helpers.assert_valid_cell_reference(coordinate)
        self.worksheet[coordinate] = value
        return

    def insert(self, virtual_sheet, anchor_ref='A1'):
        """Inserts a VirtualWorksheet object into this VirtualWorksheet.

        This is one of the "power" methods in PyFinancials. It makes it possible
        to insert an entire VirtualWorksheet into the current VirtualWorksheet,
        meaning that sheets can be built with a collection of lego blocks.

        Args:
            virtual_sheet (VirtualWorksheet): The VirtualWorksheet you wish to
                insert into the current VirtualWorksheet.
            anchor_ref (str): The top-left-most cell where you'd like to paste
                the new VirtualWorksheet into.

        Returns:
            Self.
        """
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
        return self

    def items(self):
        """Utility wrapper around the `items` generator.

        Yields:
            Key-value pairs of cell references and Cell objects.
        """
        return self.worksheet.items()
