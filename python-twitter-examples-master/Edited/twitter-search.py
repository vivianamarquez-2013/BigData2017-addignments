#!/usr/bin/python

#-----------------------------------------------------------------------
# twitter-search
#  - performs a basic keyword search for tweets containing the keywords
#    "lazy" and "dog"
#-----------------------------------------------------------------------

from twitter import *
import re

search_term = "matematicas"

from time import strftime
from textwrap import fill
from termcolor import colored
from email.utils import parsedate

#-----------------------------------------------------------------------
# load our API credentials 
#-----------------------------------------------------------------------
config = {}
execfile("config.py", config)

#-----------------------------------------------------------------------
# create twitter API object
#-----------------------------------------------------------------------
twitter = Twitter(
		        auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))


#-----------------------------------------------------------------------
# perform a basic search 
# Twitter API docs:
# https://dev.twitter.com/docs/api/1/get/search
#-----------------------------------------------------------------------
search_term = "mathematics"
query = twitter.search.tweets(q = search_term)

#-----------------------------------------------------------------------
# How long did this query take?
#-----------------------------------------------------------------------
print colored("Search complete (%.3f seconds)" % (query["search_metadata"]["completed_in"]),"blue", attrs = [ "bold" ])

#-----------------------------------------------------------------------
# Loop through each of the results, and print its content.
#-----------------------------------------------------------------------
pattern = re.compile("%s" % search_term, re.IGNORECASE)

for tweet in query["statuses"]:
	#print "(%s) @%s %s" % (result["created_at"], result["user"]["screen_name"], result["text"])
	# turn the date string into a date object that python can handle
	timestamp = parsedate(tweet["created_at"])

	# now format this nicely into HH:MM:SS format
	timetext = strftime("%H:%M", timestamp)

	# colour our tweet's time, user and text
	time_colored = colored(timetext, color = "white", attrs = [ "bold" ])
	user_colored = colored(tweet["user"]["screen_name"], "green")
	text_colored = tweet["text"]

	# replace each instance of our search terms with a highlighted version
	text_colored = pattern.sub(colored(search_term.upper(), "magenta"), text_colored)

	# add some indenting to each line and wrap the text nicely
	indent = " " * 11
	text_colored = fill(text_colored, 80, initial_indent = indent, subsequent_indent = indent)

	# now output our tweet
	print "(%s) @%s" % (time_colored, user_colored)
	print "%s" % (text_colored)

