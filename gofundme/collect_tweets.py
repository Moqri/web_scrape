import json
import sys
import pymongo
from datetime import datetime
import time
from twython import TwythonStreamer, TwythonError
import pprint as pp
import string
import os
import pandas as pd
import requests
import json
import sys
import linecache
from datetime import datetime
from pytz import timezone

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)


headers = {'content-type': 'application/json'}
url = 'https://www.gofundme.com/helpsaverileytheig'
response=requests.post(url, headers=headers)
wd=os.path.abspath(os.path.join('..', os.pardir))
auth=pd.read_csv(wd+'//auth.csv',dtype='str',index_col='user')
[access_key,access_secret,consumer_key,consumer_secret] = auth.loc['gofundme']

class MyStreamer(TwythonStreamer):
	def on_success(self, data):
		try:
			user=data['user']['screen_name']
			followers=data['user']['followers_count']	
			print followers,'-------------',user, datetime.now()
			dump=json.dumps(data, ensure_ascii=False)
			db=pymongo.MongoClient('10.247.69.18').crowd
			now_time = datetime.now(timezone('US/Eastern'))
			day= now_time.strftime("%d")
			col_name='gofundme_jan'+day
			db[col_name].insert(json.loads(dump))
			if 'entities' in data:
				if 'urls' in data['entities']:
					text=data['text']
					if ('Check it out! I donated to' in text) and ('RT @' not in text):
						if text[0]!='@' and text[0:4]!='RT @':
							url= data['entities']['urls'][0]['expanded_url']
							created_at=data['created_at']
							id=data['id']	
							db.gofundme_donated.insert({"created_at":created_at,
															"url":url,
															"user":user,
															"followers":followers,
															"text":text,
															"id":id})
							response=requests.post(url, headers=headers)
							out=open('htmls/'+user+'.html','w')
							print text
							out.write(response.text)
		except:
			print 'on_success ERROR'
			PrintException()
			pass
	def on_error(self, status_code, data):
		print status_code
		print "on_error"
stream = MyStreamer(consumer_key, consumer_secret, access_key, access_secret)
while True:
	try:	
		stream.statuses.filter(languages=["en"],track=
		['gofundme', 'gofund me'])
	except TwythonError as e:
		print e
		continue