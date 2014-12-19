#!/usr/bin/python

import requests
import sys
import feedparser as fp
import pandas as pd

def get_rss(url):
	data = fp.parse(url)
	return data

def get_fb_data(url):
	fb_items = ['url', 'comment_count', 'like_count', 'share_count']
	fb_data = requests.get("http://api.facebook.com/method/links.getStats?urls={}&format=json".format(url)).json()
	if len(fb_data) == 1:
		data = fb_data[0]
		send_data = {key:data[key] for key in fb_items}
		return send_data

def main(url, name, csv=True,):
	url = str(url)
	rss = get_rss(url)
	entries = rss['entries']

	print "\nGetting data from facebook..."
	fb_matrix = pd.DataFrame([get_fb_data(entry['link']) for entry in entries])
	if csv:
		print "Outputting csv...\n"
		#print fb_matrix
		fb_matrix.to_csv('{}.csv'.format(name))
		print "Done!"
	else:
		return fb_matrix

if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2], True)