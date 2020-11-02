import feedparser
import requests
import json
import re
from dateutil import parser
from datetime import datetime
from datetime import timedelta
# global definitions for pulling data from the RSS feed
rss = feedparser.parse('https://politepol.com/fd/t7mbrmTixBei')
title=[]
dates=[]
link=[]
newdates = []
datesafter=[]
datesbefore=[]
today = (datetime.now()-timedelta(days=1))
future = (datetime.now()+timedelta(days=7))

print(today)

# defines webex API definitions
url_message = ('https://webexapis.com/v1/messages')
url_rooms = ('https://webexapis.com/v1/rooms?type=group')
headers = {
		"Authorization": "Bearer MWE4MjNlNzItYmY4NS00NmIxLTg5YzktZTRlZTE1NjM1ZTBhMDgwZmIyODgtMzUx_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f",
		"Content-Type": "application/json"
		}

# loop to parse and append the data from the RSS feed into a list
for y in range (0,10):
	title.append(rss['entries'][y]['title'])
	dates.append(rss['entries'][y]['summary'])
	link.append(rss['entries'][y]['links'][0]['href'])
	newdates.append(parser.parse(re.sub('\s\S\s\S(.*)', '', rss['entries'][y]['summary'])))

# check which dates are in the next 7 days
for x in range (0, len(dates)):
	if newdates[x] > future:
		datesafter.append(newdates[x])
	if newdates[x] < today:
		datesbefore.append(newdates[x])

# message payload that the bot will send, formatted in MD
intro = ("### Hello! This is your weekly Webinar update.\n\n #### The webinars for this week are:\n\n")
for x in range (len(datesbefore), len(dates)-len(datesafter)):
	message = ("**"+dates[x]+"**: ["+title[x]+"]("+link[x]+")\n\n")
	intro = intro + message

# pulling IDs for all the rooms a bot is in (DO NOT CHAT 1-TO-1)
room_response = requests.request("GET", url_rooms, headers=headers)
room_obj = room_response.text
room_parsed = json.loads(room_obj)
rooms = [item.get('id') for item in room_parsed['items']]

# loop to message each room the bot is in with the payload
for x in range(0, len(rooms)):
	payload = {
		"roomId": rooms[x],
		# "toPersonEmail": 'sahastin@cisco.com',
		"markdown": intro,
		}
	response = requests.post(url_message, data=json.dumps(payload), headers=headers)
