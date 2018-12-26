"""
The classes that handle the sheets in a workbook. Does majority of the heavy
lifting.
"""

from . import assumptions, section

class Worksheet:
    """The parent object to all sheets who handles the children (sections)."""

    def __init__(self):
        """Build the worksheet."""
        self._title = None
        return

    def addAssumptionsSection(self):
        """Generates an assumptions section for the sheet."""
        return assumptions.AssumptionsSection()

    def addMetric(self, pretty_name):
        """Creates a new metric for the worksheet."""
        return

    def addSection(self):
        """Creates a new section in the financial model."""
        return section.Section()

    def setStyle(self, style_type):
        """Sets the style design for the sheet."""
        return

    @property
    def title(self):
        """A property for the sheet's title."""
        return self._title

    @title.setter
    def title(self, value):
        """Enables the sheet title to be set."""
        self._title = value
        return
