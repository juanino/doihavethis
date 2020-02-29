#!/usr/bin/env python3

import sys
import os
from os import path
import socket

hostname = (socket.gethostname())
try:
    ipaddr = socket.gethostbyname(socket.gethostname())
except:
    print("Couldn't get ip address of machine for slack message")
    ipaddr = "unknown"

# Purpose: Fetch a master DB file and compare to a filesystem
#          for purpose of regular auditing to detect bit rot or bit flips

# 1. Read master DB
# 2. Generate a DB to check (check_db)
# 3. Compare the two DBs, printing a summary
# 4. Post the results to s3
# 5. Trigger an alert if mismatch

# 1. Read master DB
try:
    master_db = sys.argv[1]
    check_dir = sys.argv[2]
except:
    print("Please supply a masterDB 1st and then a directory to check")
    sys.exit(2)
# input validate
if not path.exists(master_db):
    print("master db " + master_db + " missing or cannot open")
    sys.exit(2)

# 2. generate a DB to check (check_db)

# check.db is temporary so get rid of any old one
if path.exists("check.db"):
    print("removing old check.db file")
    os.remove("check.db")

# build the inventory of current reality
return_code = os.system("./inv2pickle.py check.db " +  check_dir)
print(return_code)
if return_code > 0:
    print("failed to inventory reality")
    sys.exit(2)

# 3. Compare the two DBs, printing a summary
return_code = os.system("./cmp_pickles.py check.db " + master_db)
if return_code > 0:
    print("Comparison failed with return code " + str(return_code))
    message = "./send_slack.py \"Validation failed on " + master_db + " hostname: " + hostname + " ipaddr: " + ipaddr + "\""
    print(message)
    os.system(message)
else:
    print(return_code) # should be 0
    message = "./send_slack.py \"Validation succeeded on " + master_db + " hostname: " + hostname + " ipaddr: " + ipaddr + "\""
    print(message)
    os.system(message)
