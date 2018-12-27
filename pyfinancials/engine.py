"""
Implements the core engine - the `FinancialModel` object.

This object handles the management, storage and construction of the final
excel spreadsheet. Think of it as the puppet-master.
"""

import openpyxl as pyxl
from . import sheets

class FinancialModel:
    """The final excel spreadsheet, but in Python code."""

    def __init__(self):
        """Initialises the spreadsheet controlling the model."""
        self.wb = pyxl.Workbook()
        return

    def build(self, save_file, verbose=False):
        """
        Compiles the financial model into excel.

        Although this method may look deceptively simple, this is where all of
        the grunt work is being done. It takes in the written code (which is all
        being stored in a giant tree) and compiles it down into working excel
        formulas.
        """
        self.wb.save(save_file)
        return  # It actually does nothing currently...

    def addSheet(self, sheet_name):
        """Adds a new sheet to the financial model."""
        return sheets.Worksheet()

    def findSheets(self, regex):
        """Looks for sheets based off a regex query."""
        return []  # WIP!
