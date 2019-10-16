import xml.etree.ElementTree as tree
import requests
import json
import datetime as date

def log(s):
	print(s)
	today = date.datetime.today()
	filename = str(today.day)+str(today.month)+str(today.year)+".txt"
	f = open(filename, "a")
	f.write("\n"+s)
	f.close()

log("-Cleaning Groups-")

#get config details
root = tree.parse("config.xml").getroot();
url =root.find("oktaUrl").text
token = root.find("oktaToken").text
ignoreGroups = []
groups = root.find("ignore")
if groups.find("group") != None:
	log("Ignoring the following groups:")
	for group in groups.iter('group'):
		ignoreGroups.append(group.text)
else:
	log("No groups are ignored")

for group in ignoreGroups:
	log("\t*"+group)

getAllGroupsUrl = url+"/api/v1/groups?limit=200"
r = requests.get(url = getAllGroupsUrl, headers={"Authorization":"SSWS "+token})
json = r.json();

next = None;

if 'link' in r.headers:
	if "next" in r.headers["link"]:
		u = r.headers["link"].split(",")[1];
		u = u[u.index("<")+1:u.index(">")]
		next = u;
	else:
		next = None
else:
	next = None

while next != None:
	log("loading...")
	r = requests.get(url = next, headers={"Authorization":"SSWS "+token})
	json =json + r.json();
	if 'link' in r.headers:
		if "next" in r.headers["link"]:
			u = r.headers["link"].split(",")[1];
			u = u[u.index("<")+1:u.index(">")]
			next = u;
		else:
			next = None
	else:
		next = None;
log("Groups found:"+str(len(json)))

jsonComplete = json
#log(json)
count = len(json)
log("------------------------------------------------")
for obj in json:
	
	id = obj['id']
	name = obj['profile']['name']
	
	for g in ignoreGroups:
		if g == name:
			id = None
			log(name+" has been ignored");
	
	if id != None:
		
		deleteUrl = url+"/api/v1/groups/"+id
		r = requests.delete(url = deleteUrl, headers={"Authorization":"SSWS "+token})
		if r.status_code != 204 :
			log(name+" could not be deleted");
		else:
			count = count - 1;
			log(name+" was deleted")
			
	log("------------------------------------------------")
log("Starting groups:"+str(len(jsonComplete)))
log("Remaining groups:"+str(count));
log("Ignored groups:"+str(len(ignoreGroups)))
		
log("-Cleaning Groups Complete-")
log("")
