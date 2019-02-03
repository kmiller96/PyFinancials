#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A commonly used file. It contains the python wrappers for Excel.
"""

#################################
## BUILD THE COMMON OPERATIONS ##
#################################
def add(lhs, rhs):
    return "({})+({})".format(lhs, rhs)

def sub(lhs, rhs):
    return "({})-({})".format(lhs, rhs)

def mul(lhs, rhs):
    return "({})*({})".format(lhs, rhs)

def floordiv(lhs, rhs):
    return "ROUNDDOWN(({})/({}),0)".format(lhs, rhs)

def div(lhs, rhs):
    return "({})/({})".format(lhs, rhs)

def mod(lhs, rhs):
    return "MOD({},{})".format(lhs, rhs)


##################################
## BUILD THE EQUALITY OPERATORS ##
##################################
def eq(lhs, rhs):
    return "({})=({})".format(lhs, rhs)

def ne(lhs, rhs):
    return "({})<>({})".format(lhs, rhs)

def lt(lhs, rhs):
    return "({})<({})".format(lhs, rhs)

def gt(lhs, rhs):
    return "({})>({})".format(lhs, rhs)

def le(lhs, rhs):
    return "({})<=({})".format(lhs, rhs)

def ge(lhs, rhs):
    return "({})>=({})".format(lhs, rhs)


##############################
## BUILD THE EXCEL FORMULAS ##
##############################
def IF(conditional, value_if_true, value_if_false):
    return "IF({}, {}, {})".format(conditional, value_if_true, value_if_false)
