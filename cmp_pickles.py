#!/usr/bin/python3

import pickledb
import sys

# pass 2 files to compare
try:
    left_file = sys.argv[1]
    right_file = sys.argv[2]
except:
    print("Supply two filenames to compare")
    exit()

db = pickledb.load(left_file,False)
db2 = pickledb.load(right_file,False)

keys1 = db.getall()
keys2 = db2.getall()

print("there are " + str(len(keys1)) + " in left file" )
print("there are " + str(len(keys2)) + " in right file" )

for key in keys1:
    if db.exists(key) and db2.exists(key):
        print("Duplicate " + key + " -> " + str(db.exists(key)) + " - " +  str(db2.exists(key)) + " file left: " + str(db.get(key)) + " file right: " + str(db2.get(key)) )
    else:
        print("Preserve  " + key + " -> " + str(db.exists(key)) + " - " +  str(db2.exists(key)) + " file left: " + str(db.get(key)) + " file right: " + str(db2.get(key))  ) 
    
#for key in keys2:
   #print(key + " " + db2.get(key))

print("there are " + str(len(keys1)) + " in left file" )
print("there are " + str(len(keys2)) + " in right file" )
