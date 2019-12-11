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

log("-Cleaning GroupRules-")

#get config details
root = tree.parse("config.xml").getroot();
url =root.find("oktaUrl").text
token = root.find("oktaToken").text
ignorerules = []
rules = root.find("ignore")
if rules.find("rule") != None:
	log("Ignoring the following rules:")
	for rule in rules.iter('rule'):
		ignorerules.append(rule.text)
else:
	log("No rules are ignored")

for rule in ignorerules:
	log("\t*"+rule)

getAllrulesUrl = url+"/api/v1/groups/rules?limit=300"
r = requests.get(url = getAllrulesUrl, headers={"Authorization":"SSWS "+token})
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
log("rules found:"+str(len(json)))

jsonComplete = json
#log(json)
count = len(json)
log("------------------------------------------------")
for obj in json:
	
	id = obj['id']
	name = obj['name']
	
	for g in ignorerules:
		if g == name:
			id = None
			log(name+" has been ignored");
	
	if id != None:
		
		deleteUrl = url+"/api/v1/groups/rules/"+id
		r = requests.delete(url = deleteUrl, headers={"Authorization":"SSWS "+token})
		if r.status_code != 202 :
			log(name+" could not be deleted");
		else:
			count = count - 1;
			log(name+" was deleted")
			
	log("------------------------------------------------")
log("Starting rules:"+str(len(jsonComplete)))
log("Remaining rules:"+str(count));
log("Ignored rules:"+str(len(ignorerules)))
		
log("-Cleaning GroupRules Complete-")
log("")
