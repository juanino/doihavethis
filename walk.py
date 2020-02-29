#!/usr/bin/env python3

# getting a directory listing of all subdirs is kinda annoying on windows
# this utility helps us just blob the whole tree into a file for grepping somewhere

import os
import pprint
import sys
import time
from os import path

# track runtime in case we change hash algorithms in future we can compare
# also when we switch computers this is a good benchmark of I/O for us

start_time = time.time()

# first arg is the pickle to save
# second arg is the path to walk
try:
    dir_to_inventory = sys.argv[1]
except:
    print("Supply the directory to scan")
    sys.exit()

global output_file
output_file = "output.txt"
fh = open(output_file,"w")

# walk the directory to inventory
file = open("output.txt","w")
for root, dirs, files in os.walk(dir_to_inventory):
    for file in files:
        fullpath = root+"/"+file
        sys.stdout.write('F')
        sys.stdout.flush() # make sure dots show up one by one
        fh.write(fullpath + "\n")
    sys.stdout.write('-D-')
    sys.stdout.flush() # make sure dots show up one by one

runtime = time.time() - start_time
fh.close
print("Time done is -> " + str(runtime) + " seconds.")


