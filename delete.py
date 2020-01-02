import os
import json
import requests

GH_TOKEN = os.getenv('GH_TOKEN')
BASE_URL = "https://api.github.com"
USER = os.getenv('USER')

gists = requests.get("%s/users/%s/gists" % (BASE_URL, USER), headers={"Authorization":"token %s" % (GH_TOKEN)}).json()
ids = []

if __name__ == "__main__":
	for g in gists:
        	key = str(g['files'].keys()).replace("dict_keys(['","").replace("'])","")
        	try:
                	url = g['files']['%s' % (key)]['raw_url']
        	except:
                	continue
        	if "Week%20of%20" in url:
                	ids.append(g['id'])
	for gid in ids:
                #id = g['id']
                print("Deleting gist#%s" % gid)
                d = requests.delete("%s/gists/%s" % (BASE_URL, gid), headers={"Authorization":"token %s" % (GH_TOKEN)})
                print(d.status_code)
