# Import Required Modules
import requests
import pprint
import json
import csv
import xml.etree.ElementTree as tree
import os
import datetime as date
	

def log(s):
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
	if fileLocation == None:
		log("file location could not be found in config.")
		return False
	elif fileCheck() == False:
		log("no file could be found at this location:"+fileLocation+".")
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
		print(rowCount)
		
		for row in csv_reader:
			if line > 0 and line < rowCount-1:
				rows.append(row)
			line=line+1
	return rows
			
def replaceHeadersWithMappings():
	headers2 = headers
	for h in headers2:
		for m in mappings:
			if h == m.get('name'):
				replaceHeader(h, m.get('value'))
				
def createProfile(headers, row):
	profile = {}
	i=0
	while i < len(row):
		column = row[i]
		if column != "" and column != None:
			profile[headers[i]] = column
		i = i + 1
	profile = {"profile":profile}
	profile = str(profile)
	profile = profile.replace("'", '"')
	return profile
	
def createUser(baseurl, apitoken, profile):
	headers = {
		'Accept': "application/json",
		'Content-Type': "application/json",
		'Authorization': "SSWS "+apitoken,
		'cache-control': "no-cache",
	}

	request = requests.post(baseurl+"/api/v1/users", headers=headers, params='"activate":"false"', data=profile)
	if request.status_code != 200:
		error = request.json()['errorSummary']
		log("The user ["+profile+"] could not be created. Error:"+error)
	
########Main#########
	
#global
log("_____Starting Program ("+str(date.datetime.now())+")_____")

fileLocation = getConfigValue("csvLocation")
oktaUrl = getConfigValue("oktaUrl")
apiToken = getConfigValue("apiToken")
headers = []
rows = []
mappings = []
check =checkGlobalValues()
	
if not check:
	log("Stopping as config file has not been set correctly")
	raiseConfigError()
else:
	headers = getHeaders();
	rows = getRows();
	mappings = getMappings();
	replaceHeadersWithMappings();
	for row in rows:
		profile = createProfile(headers, row)
		createUser(oktaUrl, apiToken, profile)
		
log("_____Program Ended ("+str(date.datetime.now())+")_____")

#######################

	