#!/usr/bin/python3
"""
zipcam.py

This script is for zipping up EAGLE CAM files for OSH Park (and further record
keeping). Just point this at an EAGLE project folder and you're good to go. (It
takes inspiration from my earlier script---zipboard.py--- for Magzor that
checked for naming compliance and a bunch of other things, but I don't need all
of that these days.)

TODOs:
- [ ] use textwrap module for pretty output
- [ ] add more logging info
"""

import re
import os
import shutil
import zipfile
import logging
import argparse
import sys

EAGLE_PROJECT_FOLDER_FILE = "eagle.epf"

# delete files with these extensions -- you don't need them
CRUFT_EXT = ["s#\d",  # schematic auto save files
             "b#\d",  # board auto save files
             ]

# Gerber/Excellon file extensions for OSH Park and stencil making
OSH_PARK_EXT = ["GBL",  # bottom layer
                "GBO",  # bottom silkscreen
                "GBS",  # bottom soldermask
                "GKO",  # dimension
                "GTL",  # top layer
                "GTO",  # top silkscreen
                "GTS",  # top soldermask
                "XLN",  # Excellon drill file
                ]

# I've heard you don't really need these, but I see no reason to delete them
MISC_CAM_EXT = ["dri",  # drill file verification
                "gpi",  # Gerber file verification?
                ]

CAM_EXT = OSH_PARK_EXT + MISC_CAM_EXT

CAM_DIR = "CAM"

remove_exiting_cam_dir = False

OSH_PARK_DIR = "OSH-Park"


def has_ext(fname, ext):
    """
    better implementation than endswith() because I can pass in regexs for ext
    """
    p = re.compile(".*\.{ext}$".format(ext=ext))

    if p.match(fname) is not None:
        return True
    return False


def has_ext_in_list(fname, ext_list):
    for ext in ext_list:
        if has_ext(fname, ext):
            return True
    return False


# these next few aren't great, but it's better
def is_cruft(fname):
    return has_ext_in_list(fname, CRUFT_EXT)


def is_cam_file(fname):
    return has_ext_in_list(fname, CAM_EXT)


def is_in_osh_zip(fname):
    return has_ext_in_list(fname, OSH_PARK_EXT)


def remove_cruft(fname):
    if is_cruft(fname):
        os.remove(fname)
        return
    else:
        return


def full_cam_dir(base_dir):
    return os.path.join(os.path.expanduser(base_dir), CAM_DIR)


def cam_dir_exists(base_dir):
    return os.path.isdir(full_cam_dir(base_dir))


def remove_cam_dir(base_dir):
    if cam_dir_exists(base_dir) and remove_exiting_cam_dir:
        shutil.rmtree(full_cam_dir(base_dir))
        logging.info("Removed '{}'".format(full_cam_dir(base_dir)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir",
                        help="enter the directory on which you want to "
                        "operate")
    parser.add_argument("-C", "--rmcam",
                        help="remove existing CAM directory",
                        action="store_true")
    args = parser.parse_args()

    if args.dir is not None:
        base_dir = args.dir
    else:
        base_dir_input = input("Enter directory on which you want to operate "
                               "or leave blank to use the current directory: ")
        if base_dir_input:
            base_dir = base_dir_input
        else:
            base_dir = os.getcwd()
    if args.rmcam is not None:
        remove_exiting_cam_dir = args.rmcam
    
    print("base_dir: '{}'".format(args.dir))
    return 0


if __name__ == "__main__":
    sys.exit(main())
