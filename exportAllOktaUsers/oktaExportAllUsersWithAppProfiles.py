# Import Required Modules
import requests
import time
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
	
#get the ids and profile of a user's app profile
def loadUserAppProfile(json):
	json['profile']['externalId'] = json['externalId']
	return json['profile']

#pri nt the okta error with status code
def printError(s, json, status_code):
	error = json['errorSummary']
	causes = json['errorCauses']
	errorCauses = ""
	for cause in causes:
		errorCauses = errorCauses+cause['errorSummary']+","
	if errorCauses != "":
		errorCauses = errorCauses[0:errorCauses.rfind(",")]
		errorCauses = ", Causes:"+errorCauses
	print(s+": ["+str(status_code)+"] Error:"+error+". "+errorCauses)
	
#get the column (key) names from the object provided
#(adds the app column to the object and retrieves the header names under the 'app' key as well)
#(places id first and all app values last)
def getColumnHeaders(jobject):
	keys = []
	for x in jobject:
		for k in x.keys():
			if not k in keys:
				keys.append(k)
	
	if "id" in keys:
		if keys.index("id") != 0:
			keys.insert(0, keys.pop(keys.index("id")))
			
	##add app column
	for x in jobject:
		if 'app' in x:
			for y in x['app']:
				for k in x['app'].keys():
					if not k in keys:
						if k != 'externalId':
							keys.append(k)
	return keys;
	
#replaces the annoying mac only key value with the replacement character provided
def replaceOddCharacter(string, replacementKey):
	if string.find("�") != -1:
		string = string.replace("�", replacementKey)
	return string
	
#get a list of the app values from the user and returns a list (ordered according to the headers)
def getAppUserList(hs, aindex, user):
	u = [];
	if 'app' in user:
		for key in hs:
			if key not in user['app']:
				u.append(str())
			else:
				if user['app'][key] == None:
					u.append(str())
				else:
					user['app'][key] = replaceOddCharacter(user['app'][key], replacementKey)
					u.append(user['app'][key]);
	return u;
	
#get a list of the user values (ordered according to header)
def getUserList(hs, user):
	userHeaders = []
	appHeaders = []
	if "app" in hs:
		userHeaders = hs[0:hs.index("app")]
		appHeaders = hs[hs.index("app")+1:len(hs)]
	else:
		userHeaders = hs

	u = list();
	for key in userHeaders:
		if key not in user:
			u.append(str())
		else:
			if user[key] == None:
				u.append(str())
			else:
				if key != "app":
					user[key] = replaceOddCharacter(user[key], replacementKey)
					u.append(user[key]);
				
	if "app" in hs and "app" in user:
		u.append(user['app']['externalId'])
		user['app']['externalId'] = ''
		u.extend(getAppUserList(appHeaders, hs.index(key), user))
	return u
replacementKey = "'"

def getUsers(oktaOrgURL, headers, appId):
	link = oktaOrgURL+"/api/v1/users?limit=200"
	jobject = list()
	while link != None:
		print("loading...")
		while True:
			request = requests.get(oktaOrgURL+"/api/v1/users", headers=headers)
			if request.status_code == 200:
				jobject = loadUserProfile(jobject, request.json())
				l = request.headers['link']
				if l != None:
					link = getLinkHeaderValue(l)
				else:
					link = None
				break
			elif request.status_code != 429:
				printError("Could not retrieve users", request.json(), request.status_code)
				link= None
				break
			else:
				print("Rate limit has been hit. Waiting 10 seconds and retrying.")
				time.sleep(10)
		
	return jobject
	
def getUserAppProfile(oktaOrgURL, headers, appId, id):
	print("retrieving app profile for "+id+"...")
	while True:
		request = requests.get(oktaOrgURL+"/api/v1/apps/"+appId+"/users/"+id, headers=headers)
		if request.status_code == 200:
			return loadUserAppProfile(request.json())
		elif request.status_code != 429:
			printError("Could not retrieve users's app profile (id=["+str(id)+"])", request.json(), request.status_code)
			break
		else:
			print("Rate limit has been hit. Waiting 10 seconds and retrying.")
			time.sleep(10)

# Import Okta Config Details
with open('config.json') as json_file:
    config = json.load(json_file)

# Set Okta Org Connection Details
if 'oktaOrgURL' in config and 'oktaAPIKey' in config:
	oktaOrgURL = config['oktaOrgURL']
	oktaAPIKey="SSWS "+config['oktaAPIKey']
	appId = config['appId']
	
	headers = {
		'Accept': "application/json",
		'Content-Type': "application/json",
		'Authorization': oktaAPIKey,
		'cache-control': "no-cache",
	}
	
	jobject = getUsers(oktaOrgURL, headers, appId)
	if appId != None:
		for user in jobject:
			appProfile = getUserAppProfile(oktaOrgURL, headers, appId, user['id'])
			if appProfile != None:
				user['app'] = appProfile
				
	else:
		print("App id was not found. App profiles were not retrieved")

	hs = getColumnHeaders(jobject)
	print("columns found:")
	print(str(hs))
	print("Users found:")
	print(str(len(jobject)))

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
			



