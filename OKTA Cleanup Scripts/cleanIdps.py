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

log("-Cleaning IDPs-")

#get config details
root = tree.parse("config.xml").getroot();
url =root.find("oktaUrl").text
token = root.find("oktaToken").text
ignoreidps = []
idps = root.find("ignore")
if idps.find("idp") != None:
	log("Ignoring the following idps:")
	for idp in idps.iter('idp'):
		ignoreidps.append(idp.text)
else:
	log("No idps are ignored")

for idp in ignoreidps:
	log("\t*"+idp)

getAllidpsUrl = url+"/api/v1/idps?limit=20"
r = requests.get(url = getAllidpsUrl, headers={"Authorization":"SSWS "+token})
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
log("idps found:"+str(len(json)))

jsonComplete = json
#log(json)
count = len(json)
log("------------------------------------------------")
for obj in json:
	
	id = obj['id']
	name = obj['name']
	
	for g in ignoreidps:
		if g == name:
			id = None
			log(g+" has been ignored");
	
	if id != None:
	
		if obj["status"] != "INACTIVE":
			deleteUrl = url+"/api/v1/idps/"+id+"/lifecycle/deactivate"
			r = requests.post(url = deleteUrl, headers={"Authorization":"SSWS "+token})
			if r.status_code != 200 :
				log(name+" could not be deactivated");
			else:
				log(name+" was deactivated")
				
		deleteUrl = url+"/api/v1/idps/"+id
		r = requests.delete(url = deleteUrl, headers={"Authorization":"SSWS "+token})
		if r.status_code != 204 :
			log(name+" could not be deleted");
		else:
			count = count - 1;
			log(name+" was deleted")
			
	log("------------------------------------------------")
log("Starting idps:"+str(len(jsonComplete)))
log("Remaining idps:"+str(count));
log("Ignored idps:"+str(len(ignoreidps)))
		
log("-Cleaning IDPs Complete-")
log("")
