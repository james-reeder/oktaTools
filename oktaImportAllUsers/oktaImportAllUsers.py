# Import Required Modules
import requests
import json
import csv
import xml.etree.ElementTree as tree
import os
import datetime as date
	
logBool = None
def log(s):
	if logBool == None or str(logBool).lower() == "true":
		print(s)
		today = date.datetime.today()
		filename = str(today.day)+str(today.month)+str(today.year)+".txt"
		f = open(filename, "a")
		f.write("\n"+s)
		f.close()

def getConfigValue(s):
	root = tree.parse("config.xml").getroot();
	if root.find(s) != None:
		return root.find(s).text
	else:
		return None
		
def getMappings():
	mappings = []
	root = tree.parse("config.xml").getroot();
	ms = root.find("mappings")
	if ms != None:
		for m in ms:
			if m.tag == "mapping":
				try:
					header = m.find("csvHeader").text
					value = m.find("oktaAttribute").text
					m = {"name":header, "value":value}
					mappings.append(m)
				except:
					log("One of the mappings could not be read. Stopping program.");
					raiseConfigError();
	return mappings
				
def checkGlobalValues():
	global logBool
	if fileLocation == None:
		log("file location could not be found in config.")
		return False
	elif fileCheck() == False:
		log("no file could be found at this location:"+fileLocation+".")
		return False
	elif logBool == None:
		logBool = True
		log("log results could not be found in config.")
		return False
	elif oktaUrl == None:
		log("okta url could not be found in config.")
		return False
	elif apiToken == None:
		log("api token could not be found in config.")
		return False
	else: 
		return True

def replaceHeader(h, v):
	headers[headers.index(h)] = v
		
def raiseConfigError():
	log("_____Program Ended ("+str(date.datetime.now())+")_____")
	raise Exception("Config is not correctly set. Please check log for details")
	
def fileCheck():
	if os.path.exists(fileLocation):
		if os.path.isfile(fileLocation):
			return True;
	return False
		
def getHeaders():
	with open(fileLocation) as csvFile:
		csv_reader = csv.reader(csvFile, delimiter=',')
		line = 0;
		for row in csv_reader:
			row_new = row
			count = 0;
			for column in row:
				s = column.strip();
				
				row_new[count] = s
				if '"' in row_new[count]:
					row_new[count] = row_new[count].replace('"', "'")
				count = count + 1
			if line == 0:
				return row

def countRows():
	with open(fileLocation) as csvFile:
		csv_reader = csv.reader(csvFile, delimiter=',')
		rowCount = sum(1 for row in csv_reader)
		return rowCount
				
def getRows():
	rows = []
	with open(fileLocation) as csvFile:
		csv_reader = csv.reader(csvFile, delimiter=',')
		line = 0;
		rowCount = countRows()
		
		for row in csv_reader:
			if line > 0 and line <= rowCount:
				rows.append(row)
			line=line+1
	log("rows found:"+str(len(rows)))
	return rows
			
def replaceHeadersWithMappings():
	headers2 = headers
	for h in headers2:
		for m in mappings:
			if h == m.get('name'):
				replaceHeader(h, m.get('value'))
				
def checkValid(headers, row):
	i=0
	if "login" not in headers or "firstName" not in headers or "email" not in headers or "lastName" not in headers:
		return False
	for column in row:#remove , column
		if headers[i] == "login":
			if column == "" or column == None or column == ",":
				return False
		if headers[i] == "firstName":
			if column == "" or column == None or column == ",":
				return False
		if headers[i] == "lastName":
			if column == "" or column == None or column == ",":
				return False
		if headers[i] == "email":
			if column == "" or column == None or column == ",":
				return False
		i = i + 1;
	return True

def createProfile(headers, row):
	profile = {}
	i=0
	if not checkValid(headers, row):
		return None
	for column in row:
		if column != "" and column != None:
			column = column.strip();
			if column == "TRUE" or column == "FALSE":
				column = column.lower()
			profile[headers[i]] = column	
		i = i + 1
	return profile
	
def createUser(baseurl, apitoken, profile):
	headers = {
		'Accept': "application/json",
		'Content-Type': "application/json",
		'Authorization': "SSWS "+apitoken,
		'cache-control': "no-cache",
	}
	profile = {"profile":profile}
	profile = json.dumps(profile)

	request = requests.post(baseurl+"/api/v1/users?activate=false", headers=headers, data=str(profile))
	if request.status_code != 200:
		error = request.json()['errorSummary']
		causes = request.json()['errorCauses']
		errorCauses = ""
		for cause in causes:
			errorCauses = errorCauses+cause['errorSummary']+","
		if errorCauses != "":
			errorCauses = errorCauses[0:errorCauses.rfind(",")]
			errorCauses = ", Causes:"+errorCauses
			
		
		log("The user ["+profile+"] could not be created. Error:"+error+errorCauses)
		
def updateUser(baseurl, apitoken, profile, id):
	headers = {
		'Accept': "application/json",
		'Content-Type': "application/json",
		'Authorization': "SSWS "+apitoken,
		'cache-control': "no-cache",
	}
	profile = {"profile":profile}
	profile = json.dumps(profile)

	request = requests.post(baseurl+"/api/v1/users/"+id, headers=headers, data=str(profile))
	if request.status_code != 200:
		error = request.json()['errorSummary']
		causes = request.json()['errorCauses']
		errorCauses = ""
		for cause in causes:
			errorCauses = errorCauses+cause['errorSummary']+","
		if errorCauses != "":
			errorCauses = errorCauses[0:errorCauses.rfind(",")]
			errorCauses = ", Causes:"+errorCauses
			
		log("The user ["+profile+"] could not be updated. Error:"+error+errorCauses)
		
def userExist(baseurl, apitoken, profile):
	headers = {
		'Accept': "application/json",
		'Content-Type': "application/json",
		'Authorization': "SSWS "+apitoken,
		'cache-control': "no-cache",
	}
	
	request = requests.get(baseurl+"/api/v1/users?q="+profile.get('login'), headers=headers)
	if request.status_code == 200:
		json = request.json()
		for user in json:
			if user['profile']['login'].lower() == profile.get('login').lower():
				return user['id']
				
		return None
	else:
		log("unable to check for users:"+str(request.json()))
		raise Exception("Unable to check if users exist")
	return None
	
########Main#########
	
#global
logBool = getConfigValue("logResults")
log("_____Starting Program ("+str(date.datetime.now())+")_____")

fileLocation = getConfigValue("csvLocation")
oktaUrl = getConfigValue("oktaUrl")
apiToken = getConfigValue("apiToken")
headers = []
rows = []
mappings = []
check =checkGlobalValues()
	
if not check:
	logBool = True
	log("Stopping as config file has not been set correctly")
	raiseConfigError()
else:
	headers = getHeaders();
	rows = getRows();
	mappings = getMappings();
	replaceHeadersWithMappings();
	for row in rows:
		profile = createProfile(headers, row)
		if profile != None:
			id = userExist(oktaUrl, apiToken, profile)
			if id != None:
				updateUser(oktaUrl, apiToken, profile, id)
			else:
				createUser(oktaUrl, apiToken, profile)
				
log("_____Program Ended ("+str(date.datetime.now())+")_____")

#######################

	