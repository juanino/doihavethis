#!/usr/bin/env python3
# get all the results from the jobs

from redis import Redis
from rq.job import Job
from rq.registry import FinishedJobRegistry

redis = Redis()
#job = Job.fetch('019bf56a-4a4c-4440-9205-94d5f0022175', connection=redis)
#print('Status: %s' % job.result)

registry = FinishedJobRegistry('default', connection=redis)
job_ids = registry.get_job_ids() # You can then turn these into Job instances

for id in job_ids:
    job = Job.fetch(id, connection=redis)
    print('Result is: %s' % job.result)
