import os
import json
import requests

GH_TOKEN = os.getenv('GH_TOKEN')
BASE_URL = "https://api.github.com"
USER = os.getenv('USER')

ids = []
gists = []

if __name__ == "__main__":

	page = 1

	while True:
        	gists_input = requests.get("%s/users/%s/gists?page=%s" % (BASE_URL, USER, page), headers={"Authorization":"token %s" % (GH_TOKEN)}).json()
        	page = page + 1
        	if len(gists_input) == 0:
                	break
        	else:
                	for in_gist in gists_input:
                        	gists.append(in_gist)

	for g in gists:
		keys = []
		for k in g['files'].keys():
			if k in keys:
				continue
			else:
				keys.append(k)
		try:
			url = g['files']['%s' % (k)]['raw_url']
			ids.append(g['id'])
		except Exception as e:
			print(e)
			continue

	for gid in ids:
                print("Deleting gist#%s" % gid)
                d = requests.delete("%s/gists/%s" % (BASE_URL, gid), headers={"Authorization":"token %s" % (GH_TOKEN)})
                print(d.status_code)
