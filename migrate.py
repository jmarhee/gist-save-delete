import os
import json
import requests
from requests.auth import HTTPBasicAuth

GH_TOKEN = os.getenv('GH_TOKEN')
BASE_URL = "https://api.github.com"
USER = os.getenv('USER')
GL_URL = "https://gitlab.com"
GL_TOKEN = os.getenv('GITLAB_TOKEN')

urls = []
snips = []

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

for g in gists:
	if g['public'] == True:
		privacy = "public"
	else:
		privacy = "private"

	snip = { "visibility": privacy }

	keys = []

	for k in g['files'].keys():
		if k in keys:
			continue
		else:
			keys.append(k)

	for key in keys:
		try:
			url = g['files']['%s' % (key)]['raw_url']
			urls.append(url)
			for f in g['files'][key]:
				filename = g['files'][key]['filename']
				snip["description"] = g['description']
				snip["file_name"] = filename
				snip["title"] = filename
				content = requests.get(url).text
				snip["content"] = content
			snips.append(snip)
			print("%s: Ready" % filename)
		except Exception as e:
			print(e)
			continue

for snip in snips:
	r = requests.post("%s/api/v4/snippets" % (GL_URL), headers={"PRIVATE-TOKEN": "%s" % (GL_TOKEN), "application":"json"}, data=snip).json()
	print(r)
