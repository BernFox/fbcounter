#!/usr/bin/python
""" This script gets a list of story ids from cafe.com, then pushes them to a redis list"""

import redis 
import requests

redis_name = 'test_ids'
r = redis.StrictRedis(host='localhost',port=6379)

print "Getting data from the butler..."
data = requests.get("http://butler.cafe.com/stories?user=91").json()

ids = [item['id'] for item in data]

print "Pushing data to redis..."
map(lambda x: r.rpush(redis_name, x), ids)

r.persist(redis)