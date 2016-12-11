import requests
from HTMLParser import HTMLParser
from BeautifulSoup import BeautifulSoup
import sys
import pandas as pd
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
headers = {'content-type': 'application/json'}
page='fsfhh5r8'
url='https://www.gofundme.com/mvc.php?route=donate/pagingdonationsb&url='+page+'&idx=1'
response=requests.post(url, headers=headers)
soup = BeautifulSoup(response.text)
links = soup.findAll("div", { "class" : "section_head" })
c=int(str(links).split(' DONATIONS')[0].split('[<div class="section_head">')[1].strip())
print c
	

pd.DataFrames
for i in reversed(range(c/10+1)):
	idx=i*10
	url='https://www.gofundme.com/mvc.php?route=donate/pagingdonationsb&url='+page+'&idx='+str(idx)
	response=requests.post(url, headers=headers)
	soup = BeautifulSoup(response.text)
	donors = soup.findAll("div", { "class" : "doner" })
	for d in reversed(donors):
		line=str(d.findAll("div", { "class" : "dtime" })).split('[<div class="dtime">')[1].split('</div>]')[0].strip()
		out=open(page+'.csv','a')
		out.write(line+'\n')



