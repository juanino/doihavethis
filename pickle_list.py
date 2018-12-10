#!/usr/bin/python3

import pickledb

db = pickledb.load('db_s3.pickle',False)

keys = db.getall()
for key in keys:
   print(key + " " + db.get(key))
print("there are " + str(len(keys)))
