# Import Required Modules
import requests
import pprint
import json
import csv

#get the next link headers from the link headers
def getLinkHeaderValue(link):
	if link.find('next') > 0:
		link = link[link.rfind("<")+1:link.rfind(">")]
		return link;
	else:
		return None

#get the ids and profile of all the users
def loadUserProfile(jobject, responseText):
	for x in responseText:
		x['profile']['id'] = x['id']
		jobject.append(x['profile'])
	return jobject

#get the column (key) names from the object provided
#(adds the app column to the object and retrieves the header names under the 'app' key as well)
#(places id first and all app values last)
def getColumnHeaders(jobject):
	keys = list()
	for x in jobject:
		for k in x.keys():
			if not k in keys:
				keys.append(k)
				
	if keys.index("id") != 0:
		keys.insert(0, keys.pop(keys.index("id")))
	##add app column
	
	keys.remove("app");
	keys.append("app");
	for x in jobject:
		if 'app' in x:
			for y in x['app']:
				for k in x['app'].keys():
					if not k in keys:
						keys.append(k)
	return keys;
	
#replaces the annoying mac only key value with the replacement character provided
def replaceOddCharacter(string, replacementKey):
	if string.find("�") != -1:
		string = string.replace("�", replacementKey)
	return string
	
#get a list of the app values from the user and returns a list (ordered according to the headers)
def getAppUserList(hs, aindex, user):
	u = list();
	if 'app' in user:
		for key in hs:
			if hs.index(key) > aindex:
				if key not in user['app']:
					u.append(str())
				else:
					if user['app'][key] == None:
						u.append(str())
					else:
						if key == "app":
							u.append(appId)
						else:
							user['app'][key] = replaceOddCharacter(user['app'][key], replacementKey)
							u.append(user['app'][key]);
	return u;
	
#get a list of the user values (ordered according to header)
def getUserList(hs, user):
	#print(user)
	appIdIndex = -1
	u = list();
	for key in hs:
		if key not in user:
			u.append(str())
		else:
			if user[key] == None:
				u.append(str())
			else:
				if key == "app":
					u.append(appId)
					u.extend(getAppUserList(hs, hs.index(key), user))
				else:
					user[key] = replaceOddCharacter(user[key], replacementKey)
					u.append(user[key]);
	return u
replacementKey = "'"

# Import Okta Config Details
with open('config.json') as json_file:
    config = json.load(json_file)

# Set Okta Org Connection Details
if 'oktaOrgURL' in config and 'oktaAPIKey' in config and 'AppId' in config:
	oktaOrgURL = config['oktaOrgURL']
	oktaAPIKey="SSWS "+config['oktaAPIKey']
	appId = config['AppId']

	# Set Headers for Get Users Request
	headers = {
		'Accept': "application/json",
		'Content-Type': "application/json",
		'Authorization': oktaAPIKey,
		'cache-control': "no-cache",
		}

	# Make Inital Get Users Request
	request = requests.get(oktaOrgURL+"/api/v1/users", headers=headers, params='"limit":"200"')
	link = request.headers['link']
	if link != None:
		link = getLinkHeaderValue(link)
		
	jobject = list()
	jobject = loadUserProfile(jobject, request.json())

	#loop over link 'next' headers to get all users
	while link != None:
		print("loading...")
		request = requests.get(link, headers=headers)
		link2 = request.headers['link']
		if link2 != None:
			link = getLinkHeaderValue(link2)
		jobject = loadUserProfile(jobject, request.json())


	#get the app data for each user
	if appId != None:
		for user in jobject:
			print("getting app data for "+user['id']+"...")
			request = requests.get(oktaOrgURL+"/api/v1/apps/"+appId+"/users/"+user['id'], headers=headers)
			if request.status_code == 200:
				user['app'] = request.json()['profile']

	hs = getColumnHeaders(jobject)
	print(hs)
	print(len(jobject))

	#write results to csv
	with open('allOktaUsers.csv', 'w', newline='') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerow(hs)
		for user in jobject:
			u = getUserList(hs, user)
			
			writer.writerow(u)
		totalUsersRow="Total Users: ",len(jobject)
		writer.writerow(totalUsersRow)
	csvFile.close()
else:
	print("Your config has not been set correctly")
			



