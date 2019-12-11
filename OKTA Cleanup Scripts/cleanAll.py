from time import sleep
import datetime as date

def log(s):
	print(s)
	today = date.datetime.today()
	filename = str(today.day)+str(today.month)+str(today.year)+".txt"
	f = open(filename, "a")
	f.write("\n"+s)
	f.close()

log("---Cleaning All---")

log("Clean all catagories has started. This may take a while.")
log("===================================================================")
exec(open(r"cleanApps.py").read())
sleep(60)
log("===================================================================")
exec(open(r"cleanAuthorizationServers.py").read())
sleep(60)
log("===================================================================")
exec(open(r"cleanGroupRules.py").read())
sleep(60)
log("===================================================================")
exec(open(r"cleanGroups.py").read())
sleep(60)
log("===================================================================")
exec(open(r"cleanIdps.py").read())
sleep(60)
log("===================================================================")
exec(open(r"cleanUsers.py").read())
sleep(60)
log("===================================================================")
exec(open(r"cleanZone.py").read())
log("===================================================================")


log("---Cleaning All Complete---")
log("")
