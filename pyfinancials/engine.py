"""
Contains the core engine - the FinancialModel object.

It also contains the wrapper utilities for things such as the Worksheet object.
"""

import openpyxl as pyxl
from . import primarykey as pk
from . import virtualsheet
from . import assumptions, lineitems

class FinancialModel:
    """The core engine of the program - the financial model."""

    def __init__(self):
        """Initialises the engine."""
        self.wb = pyxl.Workbook()
        self.wb.remove(self.wb.get_sheet_by_name("Sheet")) # Remove initialisation sheet.
        self.sheets = []
        return

    def addSheet(self, tab_name):
        """Adds a new sheet to the financial model."""
        new_sheet = Worksheet(
            tab_name=tab_name
        )
        self.sheets.append(new_sheet)
        return new_sheet

    def build(self, save_file, verbose=False):
        """
        Compiles the financial model into excel.

        Although this method may look deceptively simple, this is where all of
        the grunt work is being done. It takes in the written code (which is all
        being stored in a giant tree) and compiles it down into working excel
        formulas.
        """
        # Compile the sheets.
        for sheet in self.sheets:
            pyxl_sheet = self.wb.create_sheet(title=sheet.tab_name)
            pyxl_sheet = sheet.build(pyxl_sheet)

        # Save the model.
        self.wb.save(save_file)
        return True


class Worksheet:
    """Utility class around the VirtualWorksheet. Stores metadata."""

    def __init__(self, tab_name):
        """Stores the metadata."""
        self.worksheet = virtualsheet.VirtualWorksheet()
        self.tab_name = tab_name
        self.assumption_tables = []
        self.lineitem_sections = []
        return

    def __str__(self):
        """Builds the primary key string."""
        return self.pk

    def __getitem__(self, key):
        """Pushes getitem requests to VirtualWorksheet."""
        return self.worksheet[key]

    def __setitem__(self, key, value):
        """Pushes setitem requests to VirtualWorksheet."""
        self.worksheet[key] = value
        return

    def addAssumptionsTable(self):
        """Adds an assumptions table to the financial model."""
        assumpt_tbl = assumptions.AssumptionsTable()
        self.assumption_tables.append(assumpt_tbl)
        return assumpt_tbl

    def addLineItemSection(self):
        """Adds a section for line items to the financial model."""
        lineitem = lineitems.LineItemSection()
        self.lineitem_sections.append(lineitem)
        return lineitem

    def build(self, pyxl_sheet):
        """Builds the worksheet."""
        # TODO: Generalise for any number of tables/sections.
        assumpt_tbl = self.assumption_tables[0]
        lineitem_sect = self.lineitem_sections[0]

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
        """Allows for particular styles to be defined for the worksheet."""
        return self  # TODO
