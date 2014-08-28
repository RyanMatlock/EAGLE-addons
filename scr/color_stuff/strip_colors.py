import re

hex_p = re.compile("#([a-z0-9]{6})$")

with open("sm_color_palette.txt") as f:
    with open("../palette.txt", "w") as out:
        for line in f:
            m = hex_p.match(line.strip().split(",")[2])
            if m is not None:
                out.write("{}\n".format(m.group(1).upper()))
