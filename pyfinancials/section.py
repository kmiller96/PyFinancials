"""
Creates, stores and handles the individual sections.
"""

import openpyxl as pyxl
from . import item

class Section:
    """The parent class to all sections."""
    # raise NotImplementedError("We can't build sections yet!")

    def addLine(self, pretty_name):
        """Adds a new line item into the spreadsheet."""
        return item.LineItem()


    def addLineChart(self, lines):
        """Adds a line chart given a matrix of values."""
        return

    def addMetricTable(self, rows, columns):
        """Creates a metric table on the sheet."""
        return
