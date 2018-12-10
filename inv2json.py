#!/usr/bin/python3

import os
import hashlib
import pprint
import sys
import doihavethisconfig as cfg
import logging
import time
import pickledb

dir_to_inventory = '/data/zips//albums/feb07/'

db = pickledb.load('db_s3.pickle', False)

def write_to_db(checksum, fullpath):
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
        checksum = hashlib.md5(open(fullpath, 'rb').read()).hexdigest()
        logger.info("hash of file " + fullpath +  " is " + checksum)
        sys.stdout.write('F')
        sys.stdout.flush() # make sure dots show up one by one
        # write to dictionary with checksum as key
        write_to_db(checksum, fullpath)
    sys.stdout.write('-D-')
    sys.stdout.flush() # make sure dots show up one by one

# cleanm up
db.dump()
