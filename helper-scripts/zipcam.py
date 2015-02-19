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

remove_cruft = True

# Gerber/Excellon file extensions for OSH Park and stencil making
GERBER_EXT = ["GBL",  # bottom layer
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

CAM_EXT = GERBER_EXT + MISC_CAM_EXT

CAM_DIR = "CAM"

remove_exiting_cam_dir = False

GERBER_DIR = "Gerbers"


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


def is_gerber_file(fname):
    return has_ext_in_list(fname, GERBER_EXT)


def full_cam_dir(base_dir):
    return os.path.join(os.path.expanduser(base_dir), CAM_DIR)


def cam_dir_exists(base_dir):
    return os.path.isdir(full_cam_dir(base_dir))


def remove_cam_dir(base_dir):
    # I'm just going to be paranoid about removing stuff
    if cam_dir_exists(base_dir) and remove_exiting_cam_dir:
        shutil.rmtree(full_cam_dir(base_dir))
        logging.info("Removed '{}'".format(full_cam_dir(base_dir)))


def is_eagle_project_folder(base_dir):
    return os.path.isfile(os.path.join(os.path.expanduser(base_dir),
                                       EAGLE_PROJECT_FOLDER_FILE))


def mkdir_if_nexists(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)
    return


def mkdir_catch_oserror(dir):
    try:
        mkdir_if_nexists(dir)
    except OSError as e:
        logging.warning("Something weird happened when trying to make '{}' "
                        "({})".format(dir, e))
        return 1
    return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir",
                        help="enter the directory on which you want to "
                        "operate")
    parser.add_argument("-C", "--rmcam",
                        help="remove existing CAM directory",
                        action="store_true")
    parser.add_argument("-k", "--keepcruft",
                        help="keep temporary save files and other cruft",
                        action="store_true")
    args = parser.parse_args()

    # set the base directory
    if args.dir is not None:
        base_dir = args.dir
    else:
        base_dir_input = input("Enter directory on which you want to operate "
                               "or leave blank to use the current directory: ")
        if base_dir_input:
            base_dir = base_dir_input
        else:
            base_dir = os.getcwd()
    base_dir = os.path.expanduser(base_dir)

    # ensure that it's actually an EAGLE project folder
    if not is_eagle_project_folder(base_dir):
        logging.warning("'{}' does not contained file named '{}'"
                        "".format(base_dir, EAGLE_PROJECT_FOLDER_FILE))
        if input("'{}' not found. Do you wish to proceed? (y/n)? "
                 "".format(EAGLE_PROJECT_FOLDER_FILE)).lower in ("y", "yes"):
            pass
        else:
            logging.info("Exiting on user's request due to '{}' not being "
                         "found".format(EAGLE_PROJECT_FOLDER_FILE))
            return 1

    # do all the stuff related to removing existing CAM dirs
    if args.rmcam is not None:
        remove_exiting_cam_dir = args.rmcam
    else:
        if cam_dir_exists(base_dir):
            if input("Remove existing subdirectory './{}' (y/n)? "
                     "".format(CAM_DIR)).lower() in ("y", "yes"):
                remove_exiting_cam_dir = True
            else:
                remove_exiting_cam_dir = False
    if remove_exiting_cam_dir:
        remove_cam_dir(base_dir)

    # keep cruft?
    if args.keepcruft:
        remove_cruft = False

    # now let's do the real stuff
    base_name = os.path.basename(base_dir)
    zipfile_name = base_name + "-gerbers.zip"
    files_written_to_zipfile = []

    cam_path = os.path.join(base_dir, CAM_DIR)
    gerber_path = os.path.join(cam_path, GERBER_DIR)

    # mkdir_if_nexists(cam_path)
    # mkdir_if_nexists(gerber_path)

    if mkdir_catch_oserror(cam_path):
        return 1
    if mkdir_catch_oserror(gerber_path):
        return 1

    # I'm pretty sure I can/should use context management here
    with zipfile.ZipFile(zipfile_name, "w") as zf:
        for element in os.listdir(base_dir):
            if is_cruft(element) and remove_cruft:
                os.remove(element)
                logging.info("Removed '{}'".format(element))
            if is_gerber_file(element):
                zf.write(element)
                logging.info("Wrote '{}' to '{}'"
                             "".format(element, zipfile_name))
                files_written_to_zipfile.append(element)
                shutil.move(os.path.join(base_dir, element), gerber_path)
                logging.info("Moved '{}' to '{}'"
                             "".format(element, gerber_path))
            if is_cam_file(element) and os.path.isdir(cam_path):
                shutil.move(os.path.join(base_dir, element), cam_path)
                logging.info("Moved '{}' to '{}'"
                             "".format(element, cam_path))

    shutil.move(os.path.join(base_dir, zipfile_name), gerber_path)
    logging.info("Moved '{}' to '{}'".format(zipfile_name, gerber_path))

    print("Looks like everything worked as expected.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
