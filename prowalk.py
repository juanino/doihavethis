#!/usr/bin/env python3

# getting a directory listing of all subdirs is kinda annoying on windows
# this utility helps us just blob the whole tree into a file for grepping somewhere

import os
import pprint
import sys
import time
from tqdm import tqdm
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

# walk the directory to inventory
count = 0
pbar = tqdm(total=236000,desc="Checking",bar_format="{l_bar}{bar}")
for root, dirs, files in os.walk(dir_to_inventory):
    count = len(files) + count
    pbar.update(len(files))
