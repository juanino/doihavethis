#!/usr/bin/env python3

import pickledb
import sys

# pass file to list keys
try:
    pickle_file = sys.argv[1]
except:
    print("Supply a filename to list keys")
    exit()

print(pickle_file)
db = pickledb.load(pickle_file,False)

keys = db.getall()
for key in keys:
   print(key + " " + db.get(key))
print("there are " + str(len(keys)))
