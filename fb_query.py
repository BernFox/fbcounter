#!/usr/bin/python

import redis 
import requests
import datetime
import time
import pika
import logging
import os
import json


class fbcounter():

	"""	
	This class acts as a facebook data collector.

	It gets uses Cafe story ids stored in redis to get the category & slug of a story from butler
	(a story's URL is composed of its category and slug). After we have that we hit facebook's API 
	for data concerning the number of shares, likes, and comments each story has. This is then sent 
	to RabbitMQ to be persisted with redshift.
	"""

	#Uncomment out the line below for local testing, and comment out the os.env line below that. 
	#rabbit = 'amqp://kaqsfgjd:LtpjQjpOk4ecWqfke23NI3cG9Esmu3uh@hyena.rmq.cloudamqp.com:5672/kaqsfgjd'
	rabbit = os.environ['RABBITMQ_URI']
	connection = pika.BlockingConnection(pika.URLParameters(rabbit))
	channel = connection.channel()
	logging.basicConfig()

	#Uncomment the two lines below for testing, comment out the two lines after that get values from env variables
	#redis_host = 'dover.somespider.com'
	#redis_port = 49195
	redis_host = os.environ['REDIS_HOST']
	redis_port = int(os.environ['REDIS_PORT'])
	r = redis.StrictRedis(host=redis_host, port=redis_port)

	fb_items = ['url', 'comment_count', 'like_count', 'share_count']

	def __init__(self, red_name, rab_name):
		
		self.redis_name = red_name
		self.rab_name = rab_name
		self.channel.queue_declare(queue=rab_name)
		

	def butler(self, cur_id):
		return requests.get("http://butler.cafe.com/stories/{}/draft?user=fbcounter".format(cur_id)).json()

	def fb_query(self, cat, slug):

		fb_data = requests.get("http://api.facebook.com/method/links.getStats?urls=http://www.cafe.com/{}/{}&format=json".format(cat,slug)).json()
		if len(fb_data) == 1:
			data = fb_data[0]
			send_data = {key:data[key] for key in self.fb_items}
			return send_data
		else:
			print "List has length longer than 1, please inspect!"

	def collect(self, exchange = ''):

		go = True
		while go:

			print "Popping item from Redis"
			#print r.ping()
			current = self.r.lpop(self.redis_name)
			butler_cur = self.butler(current)

			category = butler_cur['section']['term']
			slug = butler_cur['slug']

			fb_data = self.fb_query(category,slug)
			fb_data['story_id'] = current
			fb_data['datetime'] = str(datetime.datetime.now())

			print "Current:"
			print str(fb_data)

			print "Sending message to RabbitMQ..."
			self.channel.basic_publish(exchange=exchange, routing_key=self.rab_name, body=json.dumps(fb_data))

			self.r.rpushx(redis_name,current)
			print "Item pushed back to Redis\n"
			time.sleep(2)

		connection.close()

if __name__ == '__main__':
	redis_name = 'test_ids'
	rab_name = 'events.share.accounts.fb'

	test = fbcounter(redis_name, rab_name)
	print test.redis_name
	test.collect('topics')




