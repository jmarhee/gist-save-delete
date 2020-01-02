import os
import json
import requests

GH_TOKEN = os.getenv('GH_TOKEN')
BASE_URL = "https://api.github.com"
USER = os.getenv('USER')

gists = requests.get("%s/users/%s/gists" % (BASE_URL, USER), headers={"Authorization":"token %s" % (GH_TOKEN)}).json()
urls = []

for g in gists:
	keys = []
	for k in g['files'].keys():
		if k in keys:
			continue
		else:
			keys.append(k)

	try:
		for uk in keys:
			url = g['files']['%s' % (uk)]['raw_url']
			urls.append(url)
			
			filename = "tmp/" + g['files'][uk]['filename']
			body = requests.get(url).text
			f = open(filename, "w")
			f.write(body)
			f.close()

	except Exception as e:
		print(e)
		continue
	


