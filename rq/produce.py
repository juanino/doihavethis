#!/usr/local/bin/python3

# sample producer to push onto the queue

from redis import Redis
from rq import Queue
from time import sleep

q = Queue(connection=Redis())

from funcs import count_words_at_url
result = q.enqueue(
             count_words_at_url, 'http://nvie.com')
