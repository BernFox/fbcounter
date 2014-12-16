#!/usr/bin/python

#print "\ndoes this work in the container???"

import redis 
import requests
import datetime
import time
import pika
import logging
import os

#print os.environ['RABBITMQ_URI']
#print "Ok, we get past the imports......\n"
rabbit = os.environ['RABBITMQ_URI']
redis_host = os.environ['REDIS_HOST']
redis_port = int(os.environ['REDIS_PORT'])
redis_name = 'test_ids'


print redis_host
print redis_port

logging.basicConfig()
r = redis.StrictRedis(host=redis_host, port=redis_port)
connection = pika.BlockingConnection(pika.URLParameters(rabbit))
channel = connection.channel()
channel.queue_declare(queue='events.shareaccounts.fb')

def butler(cur_id):
	return requests.get("http://butler.cafe.com/stories/{}/draft?user=fbcounter".format(cur_id)).json()

def fb_query(cat, slug):
	items = ['url', 'comment_count', 'like_count', 'share_count']

	fb_data = requests.get("http://api.facebook.com/method/links.getStats?urls=http://www.cafe.com/{}/{}&format=json".format(cat,slug)).json()
	if len(fb_data) == 1:
		data = fb_data[0]
		send_data = {key:data[key] for key in items}
		return send_data
	else:
		print "List is has length longer than 1, please inspect!"

while True:

	print "Popping item from Redis"
	#print r.ping()
	current = r.lpop(redis_name)
	butler_cur = butler(current)

	category = butler_cur['section']['term']
	slug = butler_cur['slug']

	fb_data = fb_query(category,slug)
	fb_data['datetime'] = str(datetime.datetime.now())

	print "Current:"
	#print current
	#print "{}/{}".format(category,slug)
	print fb_data

	print "Sending message to RabbitMQ..."
	channel.basic_publish(exchange='', routing_key='events.shareaccounts.fb', body=str(fb_data))

	r.rpushx(redis_name,current)
	print "Item pushed back to Redis\n"
	time.sleep(2)

connection.close()
