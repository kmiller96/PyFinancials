#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The `cell.py` module contains the logic of individual cells. Most cells are
pretty dumb, holding only a UID and a value. They are however crucial components
for the end compilation call.
"""

from . import primarykey as pk
from . import excel


class Cell:
    """Handles the logic for individual cells.

    Attributes:
        pk (PrimaryKey): A UID for the cell.
        value (optional): The current value of the cell.
    """

    def __init__(self, value=0):
        self.pk = pk.PrimaryKey()
        self.value = value
        return

    def __add__(self, other):
        return Cell(value=excel.add(self.pk, other.pk))
    def __sub__(self, other):
        return Cell(value=excel.sub(self.pk, other.pk))
    def __mul__(self, other):
        return Cell(value=excel.mul(self.pk, other.pk))
    def __floordiv__(self, other):
        return Cell(value=excel.floordiv(self.pk, other.pk))
    def __truediv__(self, other):
        return Cell(value=excel.div(self.pk, other.pk))
    def __mod__(self, other):
        return Cell(value=excel.mod(self.pk, other.pk))
    def __pow__(self, other):
        return Cell(value=excel.pow(self.pk, other.pk))
