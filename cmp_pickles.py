#!/usr/bin/env python3

import pickledb
import sys
from tqdm import tqdm

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

estimated_keys = len(keys1)

dup_counter = 0
keep_counter = 0
pbar = tqdm(total=estimated_keys,desc="Checking",bar_format="{l_bar}{bar}")

for key in keys1:
    pbar.update(1)
    pbar.set_description("Checking ....." + db.get(key)[1:30] + "...." + db.get(key)[-30:])
    if db.exists(key) and db2.exists(key):
        tqdm.write("Duplicate " + key + " -> " + str(db.exists(key)) + " - " +  str(db2.exists(key)) + " file left: " + str(db.get(key)) + " file right: " + str(db2.get(key)) )
        dup_counter = dup_counter + 1
    else:
        tqdm.write("Preserve  " + key + " -> " + str(db.exists(key)) + " - " +  str(db2.exists(key)) + " file left: " + str(db.get(key)) + " file right: " + str(db2.get(key))  ) 
        log_output.append(("Preserve  " + key + " -> " + str(db.exists(key)) + " - " +  str(db2.exists(key)) + " file left: " + str(db.get(key)) + " file right: " + str(db2.get(key))  ) )
        keep_counter = keep_counter + 1
    
print("there are " + str(len(keys1)) + " in left file" )
print("there are " + str(len(keys2)) + " in right file" )
print("Duplicates (matches) : " + str(dup_counter))
print("Ones you should keep (new files): " + str(keep_counter))

# build a return code for validator to use
global audit_value
audit_value = 0
if len(keys1) == len(keys2):
    print("file counts: PASS")
else:
    audit_value = audit_value + 1
if dup_counter == len(keys1) and dup_counter == len(keys2):
    print("they are all dups: PASS")
else:
    audit_value = audit_value +1
sys.exit(audit_value)
