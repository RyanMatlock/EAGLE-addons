"""
generate_palette.py

let's see how generating 48 colors goes (hacked together from some other work
along this line)
"""

import re


hex_p = re.compile("^0x(?P<red>[A-Fa-f0-9]{2})"
                   "(?P<green>[A-Fa-f0-9]{2})"
                   "(?P<blue>[A-Fa-f0-9]{2})$")

rgb_p = re.compile("^\((?P<red>\d{1,3}),\s*"
                   "(?P<green>\d{1,3}),\s*"
                   "(?P<blue>\d{1,3})\)$")


class InvalidError(Exception):
    def ___init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvalidHexError(InvalidError):
    pass


class InvalidRGBError(InvalidError):
    pass


def iterable_truth(iterable):
    """
    Is there a Pythonic way to return the union of the truth value of every
    element in an interable?  It seems like a semi-common thing to have to do.
    """
    truth = True
    for element in iterable:
        truth = truth and element
    return truth


def is_valid_rgb(rgb):
    return iterable_truth([True if 0 <= color <= 255 else False
                           for color in rgb])


def hex_to_int(hex_color):
    return int("0x{}".format(hex_color), 16)


def int_to_bare_hex(x, upper=False):
    bare_hex = hex(x)[2:]
    if len(bare_hex) == 1:
        bare_hex = "0" + bare_hex
    if upper:
        bare_hex = bare_hex.upper()
    return bare_hex


def hex_to_rgb(hex_color):
    hex_m = hex_p.match(hex_color)
    (r, g, b) = (hex_m.group("red"),
                 hex_m.group("green"),
                 hex_m.group("blue"))
    return (hex_to_int(r),
            hex_to_int(g),
            hex_to_int(b))


def rgb_to_hex(rgb, prefix="0x"):
    hex_color = prefix
    for color in rgb:
        hex_color += int_to_bare_hex(color)
    return hex_color


def spaced_rgb(rgb):
    return "({} {} {})".format(rgb[0], rgb[1], rgb[2])


def brighten(rgb, amount):
    MAX_COLOR = 255
    new_c = []
    for c in rgb:
        c_bright = c + amount
        if c_bright > MAX_COLOR:
            new_c.append(MAX_COLOR)
        else:
            new_c.append(c_bright)
    return tuple(new_c)


def is_grey(rgb):
    (r, g, b) = rgb
    return r == g == b


def main():
    colors = []
    start = 60
    stop = 256
    step = int((256-start)/2.3)
    for r in range(start, stop, step):
        for g in range(start, stop, step):
            for b in range(start, stop, step):
                c = (r, g, b)
                if is_grey(c):
                    pass
                else:
                    colors.append(rgb_to_hex(c, prefix="#"))
                    colors.append(rgb_to_hex(brighten(c, 30), prefix="#"))
    # print(colors)
    with open("sm_color_palette.txt", "w") as f:
        for (i, color) in enumerate(colors):
            f.write("color-{},{},{}\n"
                    "".format(i,
                              color,
                              color))


if __name__ == "__main__":
    main()
