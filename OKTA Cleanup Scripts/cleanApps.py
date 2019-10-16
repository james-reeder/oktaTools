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

#get config details
log("-Cleaning Apps-")

root = tree.parse("config.xml").getroot();
url =root.find("oktaUrl").text
token = root.find("oktaToken").text
ignoreapps = []
apps = root.find("ignore")
if apps.find("app") != None:
	log("Ignoring the following apps:")
	for app in apps.iter('app'):
		ignoreapps.append(app.text)
else:
	log("No apps are ignored")

for app in ignoreapps:
	log("\t*"+app)

getAllappsUrl = url+"/api/v1/apps?limit=200"
r = requests.get(url = getAllappsUrl, headers={"Authorization":"SSWS "+token})
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
log("apps found:"+str(len(json)))

jsonComplete = json
#print(json)
count = len(json)
log("------------------------------------------------")
for obj in json:
	
	id = obj['id']
	
	for g in ignoreapps:
		if g == id:
			id = None
			log(g+" has been ignored");
	
	if id != None:
	
		if obj["status"] != "INACTIVE":
			deleteUrl = url+"/api/v1/apps/"+id+"/lifecycle/deactivate"
			r = requests.post(url = deleteUrl, headers={"Authorization":"SSWS "+token})
			if r.status_code != 200 :
				log(id+" could not be deactivated");
			else:
				log(id+" was deactivated")
				
		deleteUrl = url+"/api/v1/apps/"+id
		r = requests.delete(url = deleteUrl, headers={"Authorization":"SSWS "+token})
		if r.status_code != 204 :
			log(id+" could not be deleted");
		else:
			count = count - 1;
			log(id+" was deleted")
			
	log("------------------------------------------------")
log("Starting apps:"+str(len(jsonComplete)))
log("Remaining apps:"+str(count));
log("Ignored apps:"+str(len(ignoreapps)))

log("-Cleaning Apps Complete-")
log("")
