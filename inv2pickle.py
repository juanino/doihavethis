#!/usr/bin/env python3

import os
import pprint
import sys
import logging
import time
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

# first arg is the path to inventory
try:
    dir_to_inventory = sys.argv[1]
except:
    print("Supply the directory to scan")
    sys.exit(2)

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
# use logger.debug for adding more details
logger.debug('Debug logging must be on')

# walk the directory to inventory
print("Adding.....")
for root, dirs, files in os.walk(dir_to_inventory):
    logger.info("Working on the directory for inventory")
    logger.info("root dir " +  root)
    for file in files:
        total_files = total_files + 1
        sys.stdout.write(str(total_files))
        sys.stdout.write('\r')
        fullpath = root+"/"+file
        # Instead of generating hash right here
        # We queue this for workers
        
        result = q.enqueue(
                make_hash, fullpath, result_ttl=-1)
                # keep redis results "forever"

runtime = time.time() - start_time
logger.info("Time done is -> " + str(runtime) + " seconds.")
logger.info("Inspected " + str(total_files) + " files")
print('\n\nAdded ' + str(total_files) + ' files to the queue')