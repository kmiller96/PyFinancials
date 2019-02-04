#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module acts as the translator between Python code and Excel formulas.
PyFinancials comes with all simple operators out-of-the-box as well as some of
the more commonly used formulas such as ``IF`` and ``SUM``.

The operators that come included are (as expressed in Python notation):
    - Addition (``+``)
    - Subtraction (``-``)
    - Multiplication (``*``)
    - Division (``/``)
    - Floor Division (``//``)
    - Modulus (``%``)
    - Exponent (``**``)

The conditionals that come included:
    - Equals (``==``)
    - Not-Equals (``!=``)
    - Less-Than (``<``)
    - Greater-Than (``>``)
    - Less-Than-Equals-To (``<=``)
    - Greater-Than-Equals-To (``>=``)

All other functions are listed as a part of the documentation.
"""

#################################
## BUILD THE COMMON OPERATIONS ##
#################################
def add(lhs, rhs):      return "({})+({})".format(lhs, rhs)
def sub(lhs, rhs):      return "({})-({})".format(lhs, rhs)
def mul(lhs, rhs):      return "({})*({})".format(lhs, rhs)
def floordiv(lhs, rhs): return "ROUNDDOWN(({})/({}),0)".format(lhs, rhs)
def div(lhs, rhs):      return "({})/({})".format(lhs, rhs)
def mod(lhs, rhs):      return "MOD({},{})".format(lhs, rhs)
def pow(lhs, rhs):      return "({})^({})".format(lhs, rhs)


##################################
## BUILD THE EQUALITY OPERATORS ##
##################################
def eq(lhs, rhs): return "({})=({})".format(lhs, rhs)
def ne(lhs, rhs): return "({})<>({})".format(lhs, rhs)
def lt(lhs, rhs): return "({})<({})".format(lhs, rhs)
def gt(lhs, rhs): return "({})>({})".format(lhs, rhs)
def le(lhs, rhs): return "({})<=({})".format(lhs, rhs)
def ge(lhs, rhs): return "({})>=({})".format(lhs, rhs)


##############################
## BUILD THE EXCEL FORMULAS ##
##############################
def IF(conditional, value_if_true, value_if_false):
    """Excel ``IF`` statement.

    Args:
        conditional (str): An excel-interpretable conditional.
        value_if_true: To be returned if conditional evaluates as True
        value_if_false: To be returned if conditional evaluates as False
    """
    return "IF({}, {}, {})".format(conditional, value_if_true, value_if_false)
