#!/usr/bin/python3

import pickledb
import sys
import os.path
from os import path

# pass 2 files to compare
try:
    left_file = sys.argv[1]
    right_file = sys.argv[2]
    new_file = sys.argv[3]
except:
    print("Supply two filenames to merge and a third to create the merged file as")
    exit(1)

if path.exists(new_file):
    print("file exists i refuse to overwrite it")
    exit(2)

leftdb = pickledb.load(left_file,False)
rightdb = pickledb.load(right_file,False)
newdb = pickledb.load(new_file,False)

left_keys = leftdb.getall()
right_keys = rightdb.getall()

for key in left_keys:
    newdb.set(key,leftdb.get(key))
    sys.stdout.write(".")
    sys.stdout.flush() # make sure dots show up one by one

    
newdb.dump()
print("\n")
print("there are " + str(len(left_keys)) + " in left file" )
print("there are " + str(len(right_keys)) + " in right file" )
print("there are " + str(len(newdb.getall())) + " in the new  file" )
