#!/usr/bin/env python
# -*- coding: utf-8 -*-
import config
from requests_oauthlib import OAuth1Session
import json
import numpy as np
import matplotlib
matplotlib.colors.cnames
import matplotlib.pyplot as plt
import seaborn as sns



screen_name = "philosophy092"
type = "morning"

def get_all_tweet():
	CK = config.CONSUMER_KEY
	CS = config.CONSUMER_SECRET
	AT = config.ACCESS_TOKEN
	ATS = config.ACCESS_TOKEN_SECRET

	# OAuth認証
	twitter = OAuth1Session(CK, CS, AT, ATS)
	#timelineのURL
	url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
	#対象者のTwitterID
	max_id = None
	timeCounter = [0 for i in range(24)]
	morning = []
	evening = []
	for i in range(16):
		#パラメータ指定
		params = {"count" : 200 ,"screen_name": screen_name,"max_id":max_id}
		req = twitter.get(url, params = params)
		# レスポンスを確認
		if req.status_code == 200:
			tweets = json.loads(req.text)
			max_id = tweets[-1]["id"]-1
			for tweet in tweets:
				# TimeZoneをAsia/Tokyoにする
				if "おはにゃ" in tweet["text"]:
					time = tweet["created_at"].split()
					hour = int(time[3][0:2]) + 9
					hour = hour -24 if hour >= 24 else hour
					minute = int(time[3][3:5])
					second = int(time[3][6:8])
					# timeCounter[hour].append(tweet)
					times = hour*3600 + minute*60 + second
					morning.append(times)
					# timeCounter[hour]+=1
		else:
			print ("Error: %d" % req.status_code)
	return morning
	#for i in range(len(timeCounter)):
		#print(len(timeCounter[i]))

def plot_bar_chart(x,y):
	plt.title(screen_name+type)
	#カラー指定してbar plot
	plt.bar(x,y,color="gold",alpha=0.7)
	plt.xticks(x)
	plt.xlabel('Hour')
	plt.ylabel('Tweets')
	#画像として保存
	plt.savefig(screen_name+"_.png")
	plt.show()

if __name__ == '__main__':
	x_axis = range(24)
	y_axis = get_all_tweet()
	totals = int(sum(y_axis) / len(y_axis))
	print(y_axis)
	h = divmod(totals, 3600)
	m = divmod(h[1],60)
	print(h[0])
	print(m[0])
	print(m[1])

	# print(str(hour)+":"+str(m[0])+":"+str(m[1]))
	# plot_bar_chart(x_axis,y_axis)
