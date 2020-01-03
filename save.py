import os
import json
import requests

GH_TOKEN = os.getenv('GH_TOKEN')
BASE_URL = "https://api.github.com"
USER = os.getenv('USER')

gists = []
page = 1

while True:
	gists_input = requests.get("%s/users/%s/gists?page=%s" % (BASE_URL, USER, page), headers={"Authorization":"token %s" % (GH_TOKEN)}).json()
	page = page + 1
	if len(gists_input) == 0:
		break
	else:
		for in_gist in gists_input:
			gists.append(in_gist)

urls = []

for g in gists:
	if g['public'] == True:
		out_dir = "public"
	else:
		out_dir = "private"

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
			
			filename = "tmp/%s/" % (out_dir) + g['files'][uk]['filename']
			body = requests.get(url).text
			f = open(filename, "w")
			f.write(body)
			f.close()

	except Exception as e:
		print(e)
		continue
	


