"""
set_board_color_layers.py

Reads in a plain text configuration file, does some minimal error checking on
it, and generates an EAGLE script file (.scr) that implements what's in the
configuration file
"""

import sys
from datetime import date as date

LAYER_MIN = 0
LAYER_MAX = 255
COLOR_MIN = 0
COLOR_MAX = 63
NAMED_COLORS = ["Black",
                "Blue",
                "Green",
                "Cyan",
                "Red",
                "Magenta",
                "Brown",
                "LGray",
                "DGray",
                "LBlue",
                "LGreen",
                "LCyan",
                "LRed",
                "LMagenta",
                "Yellow",
                "White"]
FILL_MIN = 0
FILL_MAX = 15
NAMED_FILLS = ["Empty",
               "Solid",
               "Line",
               "LtSlash",
               "Slash",
               "BkSlash",
               "LtBkSlash",
               "Hatch",
               "XHatch",
               "Interleave",
               "WideDot",
               "CloseDot",
               "Stipple1",
               "Stipple2",
               "Stipple3",
               "Stipple4"]


def valid_line(index, csv):
    """
    expects following format:
    [layer_num, layer_name, color, fill, display]
    """
    if len(csv) == 5:
        try:
            csv[0] = int(csv[0])
        except ValueError as e:
            print("line {}, [0]: {}".format(index, e))
            return False
        if csv[0] < LAYER_MIN or csv[0] > LAYER_MAX:
            print("line {}: outside layer boundaries".format(index))
            return False
        if csv[2] not in NAMED_COLORS:
            try:
                csv[2] = int(csv[2])
                if csv[2] < COLOR_MIN or csv[2] > COLOR_MAX:
                    print("line {}: color '{}' out of bounds"
                          "".format(index, csv[2]))
                    return False
            except ValueError as e:
                print("line {}, [2] not in NAMED_COLORS and : {}"
                      "".format(index, e))
                return False
        if csv[3] not in NAMED_FILLS:
            try:
                csv[3] = int(csv[3])
                if csv[3] < FILL_MIN or csv[3] > FILL_MAX:
                    print("line {}: fill '{}' out of bounds"
                          "".format(index, csv[3]))
                    return False
            except ValueError as e:
                print("line {}, [3] not in NAMED_FILLS and : {}"
                      "".format(index, e))
                return False
        try:
            # just checking for t or f in case of typos
            if csv[4].lower()[0] == "t":
                csv[4] = True
            elif csv[4].lower()[0] == "f":
                csv[4] = False
            else:
                print("line {}: [4] invalid display value '{}'"
                      "".format(index, csv[4]))
                return False
        except IndexError:
            print("line {}: empty display".format(index))
            return False
        return True
    else:
        print("wrong number of entries in line {}: '{}'".format(index, csv))
        return False


def main():
    # expects: set_board_color_layers.py <config_file> <output_scr>
    if len(sys.argv) == 3:
        config = []
        with open(sys.argv[1]) as f:
            for (i, line) in enumerate(f):
                l = line.strip()
                if l and l[0] != "#":
                    l = l.split(",")
                    if valid_line(i, l):
                        config.append(l)
        with open(sys.argv[2], "w") as out:
            header = """# {out_name}

# This script generates a script that sets the color and display of layers
# based on a configuration file.

# This script file was automatically generated by set_board_layer_colors.py.

# Ryan Matlock
# {date}

""".format(out_name=sys.argv[2], date=date.today())
            out.write(header)

            out.write("DISPLAY NONE;\n\n")

            out.write("# although it's more concise to address the layers by\n"
                      "# name instead of number, doing it by number prevents\n"
                      "# issues related to their being (re)named something\n"
                      "# unusual\n")
            for c in config:
                out.write("# {name}\n"
                          "SET COLOR_LAYER {layer} {color};\n"
                          "SET FILL_LAYER {layer} {fill};\n"
                          "".format(layer=c[0], name=c[1], color=c[2],
                                    fill=c[3]))
                if c[4]:
                    out.write("DISPLAY {layer};\n".format(layer=c[0]))
                out.write("\n")
    else:
        print("improper number of arguments passed; exiting.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
