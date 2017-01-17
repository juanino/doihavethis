#!/usr/bin/python3

import os
import hashlib
import pprint
import sys
import doihavethisconfig as cfg

# Author: Jerry Uanino
# Purpose: Do I have this file in my picture library?

# Story: During undelete recovery, hard drive recovery, cd/dvd merging
#        or otherwise combining old drives it is hard to tell
#        if you already saved some files off a chip.
#        especially because you might have changed the filename.
#        
#        This script is intended to use md5 as a good enough mathematical 
#        match to make sure you can safely avoid duplicates

# the top level where you store most of your files
master_dir = cfg.directories['master_dir']

# directory containing files you just found
# and have no idea if you already downloaded them
questionable_dir = cfg.directories['questionable_dir']

masterlibrary = dict()
queslibrary = dict()


def write_to_master_dict(checksum, fullpath):
    # print "Writing", checksum, " as the key for", fullpath
    masterlibrary[checksum] = fullpath


def write_to_ques_dict(checksum,fullpath):
    # print "Writing", checksum, " as the key for", fullpath
    queslibrary[checksum]=fullpath


def dump_library(libraryname, description):
    num_items = len(libraryname)
    print(".")
    print("\t\t", description + " has " + str(num_items) + " items in the hash table")


def compare():
    print("\nRunning compare")
    print("---------------")
    # start with the questionable dataset as the master
    for key in queslibrary:
        # debug ## print "Looking up key " + key
        # go to the master to see if it's there
        if key in masterlibrary.keys():
            # print " ---- This file is in the master ----- "
            # print "Master library file is " + masterlibrary[key]
            # print "Questionable library file is " + queslibrary[key]
            print(queslibrary[key] + " is a dup to " + masterlibrary[key])
        else:
            print("You should preserve " + queslibrary[key] + " because it is not in the master")

#
# MAIN
#
# walk the master dir 
for root, dirs, files in os.walk(master_dir):
    print("\nroot dir",  root)
    print("computing ", len(files), " chksums")
    for file in files:
        fullpath = root+"/"+file
        checksum = hashlib.md5(open(fullpath, 'rb').read()).hexdigest()
        # debug ## print "hash of file", fullpath, "is ", checksum
        sys.stdout.write('.')
        sys.stdout.flush() # make sure dots show up one by one
        # write to dictionary with checksum as key
        write_to_master_dict(checksum, fullpath)
    dump_library(masterlibrary, "master")

# walk the questionable dir
for root, dirs, files in os.walk(questionable_dir):
    print("root dir",  root)
    for file in files:
        fullpath = root+"/"+file
        checksum = hashlib.md5(open(fullpath, 'rb').read()).hexdigest()
        print("hash of file", fullpath, "is ", checksum)
        # write to dictionary with checksum as key
        write_to_ques_dict(checksum, fullpath)
    dump_library(queslibrary, "questionable")

compare()
