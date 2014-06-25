#!/usr/local/bin/python3
"""
meta-assign.py

This script outputs assign-(schematic|board|library).scr, which defines key
binding setup for that particular environment in EAGLE CAD.  It relies upon
self-inspection, which is a little weird, but kinda cool.

Ryan Matlock
2014-06-25
"""

# format for lists of commands:
# <target>_<modifier key(s)>_<description> = [("<key1>", "<command1>"),
#                                             ...,
#                                             ("keyN>", "<commandN>")]
# TARGET options: common, schematic, board, library (common = latter 3)
# command should contain semicolon if you want it (you may not in some cases)
# if there are no  modifier keys, use a double underscore

_PREFIXES = ["common",
             "schematic",
             "library",
             "board"]
_MODIFIERS = ["C", "A", "S", "M"]

common_CA_alt_grid = [("F10", "Grid alt in 0.01;"),
                      ("F11", "Grid alt in 0.025;"),
                      ("F12", "Grid alt in 0.05;")]

# it looks like you have to initialize _var so that the locals() dict doesn't
# change size during iteration (it's prefixed with an underscore so you skip
# over it, too
#_var = None
# edit: never mind, you just have to copy locals() into a dict first
# this also means you don't need to prefix variables with an underscore now!
current_locals = dict(locals())
for _var in current_locals:
    if _var[0] != "_":
        # print(_var[0] + ": " + _var)
        for _pair in _var:
            print(_pair)
