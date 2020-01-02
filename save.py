import os
import json
import requests

GH_TOKEN = os.getenv('GH_TOKEN')
BASE_URL = "https://api.github.com"
USER = os.getenv('USER')

gists = requests.get("%s/users/%s/gists" % (BASE_URL, USER), headers={"Authorization":"token %s" % (GH_TOKEN)}).json()
urls = []

for g in gists:
	key = str(g['files'].keys()).replace("dict_keys(['","").replace("'])","")
	try:
		url = g['files']['%s' % (key)]['raw_url']
	except:
		continue
	if "Week%20of%20" in url:
		urls.append(url)

for u in urls:
	filename = str("Week%20of" + u.split('Week%20of',-1)[1]).replace("%20","-")
	body = requests.get(u).text
	f = open(filename, "w")
	f.write(body)
	f.close()
