#!/usr/local/bin/python3
"""
meta-assign.py

This script outputs assign-(schematic|board|library).scr, which defines key
binding setup for that particular environment in EAGLE CAD.  It relies upon
self-inspection, which is a little weird, but kinda cool.

Ryan Matlock
2014-06-25
"""

from datetime import date as _date

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

common_CA_altgrid = [("F10", "Grid alt in 0.01;"),
                     ("F11", "Grid alt in 0.025;"),
                     ("F12", "Grid alt in 0.05;")]
foo_FU_whatever = [("BS", "backspace 20;")]
# it looks like you have to initialize var so that the locals() dict doesn't
# change size during iteration (it's prefixed with an underscore so you skip
# over it, too
#var = None
# edit: never mind, you just have to copy locals() into a dict first
# this also means you don't need to prefix variables with an underscore now!
local_vars = dict(locals())

common = []
schematic = []
board = []
library = []
foo = []
for var in local_vars:
    assign  = "Assign "
    if var[0] != "_":
        # it would be better to use a regex for this so your description can
        # contain underscores, but that's for later
        target, modifiers, description = var.split("_")
        # print(target)
        # print(modifiers)
        # print(description)
        for modifier in modifiers:
            assign += modifier + "+"
        for pair in eval(var):
            eval(target).append(assign + pair[0] + " " + pair[1])

#print(common)
schematic += common
board += common
library += common

for editor_type in ['schematic', 'board', 'library']:
    with open("assign-" + editor_type + ".scr", "w") as output:
        header = """# assign-{editor_type}.scr

# This script sets the key bindings in the {editor_type} editor.  It only needs
# to be run as new features are added or when EAGLE is upgraded.

# Ryan Matlock
# {date}

""".format(editor_type=editor_type, date=_date.today())

        output.write(header)

        for command in eval(editor_type):
            output.write(command + "\n")
