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

log("-Cleaning Authorization Servers-")

#get config details
root = tree.parse("config.xml").getroot();
url =root.find("oktaUrl").text
token = root.find("oktaToken").text
ignoreauthorizationServers = []
authorizationServers = root.find("ignore")
if authorizationServers.find("server") != None:
	log("Ignoring the following Authorization Servers:")
	for authorizationServer in authorizationServers.iter('server'):
		ignoreauthorizationServers.append(authorizationServer.text)
else:
	log("No authorizationServers are ignored")

for authorizationServer in ignoreauthorizationServers:
	log("\t*"+authorizationServer)

getAllauthorizationServersUrl = url+"/api/v1/authorizationServers?limit=200"
r = requests.get(url = getAllauthorizationServersUrl, headers={"Authorization":"SSWS "+token})
if r.status_code != 401:
	json = r.json();

	next = None;

	if 'link' in r.headers != None:
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
	log("authorizationServers found:"+str(len(json)))

	jsonComplete = json
	#log(json)
	count = len(json)
	log("------------------------------------------------")
	for obj in json:
		
		id = obj['id']
		name = obj['name']
		
		for g in ignoreauthorizationServers:
			if g == name:
				id = None
				log(g+" has been ignored");
		
		if id != None:
		
			if obj["status"] != "INACTIVE":
				deleteUrl = url+"/api/v1/authorizationServers/"+id+"/lifecycle/deactivate"
				r = requests.post(url = deleteUrl, headers={"Authorization":"SSWS "+token})
				if r.status_code != 200 :
					log(name+" could not be deactivated");
				else:
					log(name+" was deactivated")
					
			deleteUrl = url+"/api/v1/authorizationServers/"+id
			r = requests.delete(url = deleteUrl, headers={"Authorization":"SSWS "+token})
			if r.status_code != 204 :
				log(name+" could not be deleted");
			else:
				count = count - 1;
				log(name+" was deleted")
				
		log("------------------------------------------------")
	log("Starting authorizationServers:"+str(len(jsonComplete)))
	log("Remaining authorizationServers:"+str(count));
	log("Ignored authorizationServers:"+str(len(ignoreauthorizationServers)))
else:
	log("This feature is not enabled in your enviroment");
		

log("-Cleaning Authorization Servers Complete-")
log("")