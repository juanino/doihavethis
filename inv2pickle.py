#!/usr/bin/python3

import os
import pprint
import sys
import logging
import time
import pickledb
from filehash import FileHash
from os import path

# track runtime in case we change hash algorithms in future we can compare
# also when we switch computers this is a good benchmark of I/O for us

start_time = time.time()

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
        fullpath = root+"/"+file
        md5hasher = FileHash('md5')
        try:
            checksum = md5hasher.hash_file(fullpath)
        except:
            print("could not hash " + fullpath)
            skipped_hash = skipped_hash + 1
            logger.info("cannot hash a symlink at " + fullpath)
            q_link = os.path.islink(fullpath)
            if q_link:
                print("skipping a symlink at " + fullpath)
                skipped_symlink = skipped_symlink + 1
            else:
                print("could not hah a file and it is not a symlink. BAD bro")
                logger.info("could not has " + fullpath + " even though it is not a symlink. Super Bad.")
                sys.exit(3)
        logger.info("hash of file " + fullpath +  " is " + checksum)
        sys.stdout.write('F')
        sys.stdout.flush() # make sure dots show up one by one
        # write to dictionary with checksum as key
        write_to_db(checksum, fullpath)
    sys.stdout.write('-D-')
    sys.stdout.flush() # make sure dots show up one by one

# cleanm up
db.dump()
print("\nend")

# duplicate report
if duplicates > 0:
    print("Caution you have duplicates, check the log:" + log_file)
    print("Duplicates: " + str(duplicates))

# files that could not be hashed report
print("skipped hashes: " + str(skipped_hash))
print("skipped symlink: " + str(skipped_symlink))
if skipped_hash == skipped_symlink:
    print("GOOD: skipped files are all symlinks")
else:
    print("there are some skipped files that are not symlinks. Super bad")


runtime = time.time() - start_time
logger.info("Time done is -> " + str(runtime) + " seconds.")
