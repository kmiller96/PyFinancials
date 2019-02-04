#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The `pyfinancials.engine` module contains the highest level object - the
FinancialModel. This is the root of the entire model tree and controls most of
the workbook settings such as the ordering of sheets, the global styling, etc.

It also contains the wrapper utility object: `Worksheet`.
"""

import openpyxl as pyxl
from . import primarykey as pk
from . import virtualsheet
from . import assumptions, lineitems

class FinancialModel:
    """The core engine of the program - the financial model.

    This `FinancialModel` class is the root of the model tree. This, in the end,
    is what is called to compile the entire workbook and recursively search down
    through the objects. For the moment its functionality is quite limited,
    being restricted to only creating new sheets and the `build` method.

    Attributes:
        wb: an openpyxl `Workbook` object.
    """

    def __init__(self):
        self.wb = pyxl.Workbook()
        self.wb.remove(self.wb.get_sheet_by_name("Sheet")) # Remove initialisation sheet.
        self.sheets = []
        return

    def addSheet(self, tab_name):
        """Adds a new sheet to the financial model.

        Returns:
            (Worksheet): An instance of the `Worksheet` class.
        """
        new_sheet = Worksheet(
            tab_name=tab_name
        )
        self.sheets.append(new_sheet)
        return new_sheet

    def build(self, save_file, verbose=False):
        """Compiles the financial model into a working excel file.

        Note:
            The save_file argument **must** include the .xlsx extension!

        Args:
            save_file (str): The path for the .xlsx file to be saved.
            verbose (bool): Currently not implemented.

        Returns:
            (bool): Returns True to indicate a successful build.
        """
        # Compile the sheets.
        for sheet in self.sheets:
            sheet.build(
                pyxl_sheet=self.wb.create_sheet(title=sheet.tab_name)
            )

        # Save the model.
        self.wb.save(save_file)
        return True


class Worksheet:
    """Utility class around the VirtualWorksheet.

    The VirtualWorksheet is designed in such a way that it actually `isn't` like
    an Excel worksheet at all. It was only named so for convienience. This class
    is what actually handles the worksheets. In effect, it is just a wrapper
    around a complete VirtualWorksheet and contains additional information such
    as the metadata and styling.

    Attributes:
        worksheet (VirtualWorksheet): The current VirtualWorksheet.
        tab_name (str): The name of the sheet in the compilied workbook.
    """

    def __init__(self, tab_name):
        self.worksheet = virtualsheet.VirtualWorksheet()
        self.tab_name = tab_name
        self._assumption_tables = []
        self._lineitem_sections = []
        return

    def __getitem__(self, key):
        """Syntaxic sugar for accessing the VirtualWorksheet."""
        return self.worksheet[key]

    def __setitem__(self, key, value):
        """Syntaxic sugar for accessing the VirtualWorksheet."""
        self.worksheet[key] = value
        return

    def addAssumptionsTable(self):
        """Initialises an assumptions table for the worksheet.

        Returns:
            (AssumptionsTable): A new instance of an AssumptionsTable.
        """
        assumpt_tbl = assumptions.AssumptionsTable()
        self._assumption_tables.append(assumpt_tbl)
        return assumpt_tbl

    def addLineItemSection(self):
        """Initialises a section for line items on the worksheet.

        Returns:
            (LineItemSection): A new instance of a LineItemSection.
        """
        lineitem = lineitems.LineItemSection()
        self._lineitem_sections.append(lineitem)
        return lineitem

    def build(self, pyxl_sheet):
        """Compiles the Worksheet into an openpyxl worksheet.

        This method has been deliberately named `build` and not `compile`. That
        is because this method actually "writes" to an openpyxl worksheet,
        whereas a `compile` method only returns a VirtualWorksheet.

        Args:
            pyxl_sheet: An openpyxl worksheet.

        Returns:
            A compiled version of the openpyxl worksheet.
        """
        # TODO: Generalise for any number of tables/sections.
        assumpt_tbl = self._assumption_tables[0]
        lineitem_sect = self._lineitem_sections[0]

        self.worksheet.insert(assumpt_tbl, anchor_ref='B2')
        self.worksheet.insert(lineitem_sect, anchor_ref='B10')

        for loc, val in self.worksheet.items():
            # Find the primary keys and replace them.
            pks_in_formula = pk.find_pks(val)
            for pks in pks_in_formula:
                val = val.replace(pks, self.worksheet.pks[pks])

            # Finally write to the sheet.
            pyxl_sheet[loc] = val
        return pyxl_sheet

    def setStyle(self, style_obj):
        """Allows for particular styles to be defined for the worksheet.

        Todo:
            Currently there is no styling in PyFinancials - This is a stub!
        """
        return self  # TODO
