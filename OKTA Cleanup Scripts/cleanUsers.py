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

log("-Cleaning Users-")

#get config details
root = tree.parse("config.xml").getroot();
url =root.find("oktaUrl").text
token = root.find("oktaToken").text
ignoreUsers = []
users = root.find("ignore")
if users.find("user") != None:
	log("Ignoring the following users:")
	for user in users.iter('user'):
		ignoreUsers.append(user.text)
else:
	log("No users are ignored")

for user in ignoreUsers:
	log("\t*"+user)

getAllUsersUrl = url+"/api/v1/users?filter=status eq \"STAGED\" or status eq \"SUSPENDED\" or status eq \"PROVISIONED\" or status eq \"ACTIVE\" or status eq \"RECOVERY\" or status eq \"PASSWORD_EXPIRED\" or status eq \"LOCKED_OUT\" or status eq \"DEPROVISIONED\"";
r = requests.get(url = getAllUsersUrl, headers={"Authorization":"SSWS "+token})
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
log("Users found:"+str(len(json)))

jsonComplete = json
#log(json)
count = len(json)
log("------------------------------------------------")
for obj in json:
	
	id = obj['id']
	login = obj['profile']['login']
	
	for u in ignoreUsers:
		if u == login:
			id = None
			log(login+" has been ignored");
	
	if id != None:
		
		if obj["status"] != "DEPROVISIONED":
			deleteUrl = url+"/api/v1/users/"+id
			r = requests.delete(url = deleteUrl, headers={"Authorization":"SSWS "+token})
			if r.status_code != 204 :
				log(login+" could not be deactivated");
			else:
				log(login+" was deactivated")
		
		deleteUrl = url+"/api/v1/users/"+id
		r = requests.delete(url = deleteUrl, headers={"Authorization":"SSWS "+token})
		if r.status_code != 204 :
			log(login+" could not be deleted");
		else:
			count = count - 1;
			log(login+" was deleted")
			
	log("------------------------------------------------")
log("Starting users:"+str(len(jsonComplete)))
log("Remaining users:"+str(count));
log("Ignored users:"+str(len(ignoreUsers)))
		
log("-Cleaning Users Complete-")
log("")
