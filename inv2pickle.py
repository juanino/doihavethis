#!/usr/bin/env python3

import os
import pprint
import sys
import logging
import time
import pickledb
from filehash import FileHash
from os import path
from redis import Redis
from rq import Queue
from funcs import make_hash

# setup python-rq
q = Queue(connection=Redis())

# track runtime in case we change hash algorithms in future we can compare
# also when we switch computers this is a good benchmark of I/O for us

start_time = time.time()
total_files = 0

# first arg is the pickle to save
# second arg is the path to inventory
try:
    pickle_file = sys.argv[1]
    dir_to_inventory = sys.argv[2]
except:
    print("Supply two args, the pickle filename to save and then the directory to scan")
    sys.exit(2)

if path.exists(pickle_file):
    print("pickle file exists already, probably want to wipe it out or move it")
    print("especially since I do not delete rows that are gone")
    sys.exit(2)

db = pickledb.load(pickle_file, False)
duplicates = 0
skipped_hash = 0
skipped_symlink = 0

def write_to_db(checksum, fullpath):
    if db.exists(checksum):
        sys.stdout.write('-Duplicate-')
        sys.stdout.flush() # make sure dots show up one by one
        logger.info(fullpath + ' is a duplicate to ' + db.get(checksum) )
        global duplicates
        duplicates = duplicates + 1
    db.set(checksum,fullpath)
    
# setup logging
log_file = 'inventory.log'
logger = logging.getLogger('inv2json ' + __name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler(log_file)
handler.setLevel(logging.INFO)

# format for logging
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add handlers to logger
logger.addHandler(handler)

logger.info('Starting utility')
logger.debug('Debug logging must be on')

# walk the directory to inventory
for root, dirs, files in os.walk(dir_to_inventory):
    logger.info("Working on the directory for inventory")
    logger.info("root dir " +  root)
    for file in files:
        total_files = total_files + 1
        fullpath = root+"/"+file
        #md5hasher = FileHash('md5')
        # Instead of generating hash
        # We queue this for workers
        
        result = q.enqueue(
                make_hash, fullpath)

# clean up
db.dump()
print("\nend")

# duplicate report
if duplicates > 0:
    print("Caution you have duplicates, check the log:" + log_file)
    print("Duplicates: " + str(duplicates))

# files that could not be hashed report
print("skipped hashes: " + str(skipped_hash))
print("skipped symlink: " + str(skipped_symlink))
print("Inspected " + str(total_files) + " files")
if skipped_hash == skipped_symlink:
    print("GOOD: skipped files are all symlinks")
else:
    print("there are some skipped files that are not symlinks. Super bad")


runtime = time.time() - start_time
logger.info("Time done is -> " + str(runtime) + " seconds.")
logger.info("Inspected " + str(total_files) + " files")
