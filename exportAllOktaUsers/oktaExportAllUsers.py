# Import Required Modules
import requests
import pprint
import json
import csv

# Import Okta Config Details
with open('config.json') as json_file:
    configFileData = json.load(json_file)

# Set Okta Org Connection Details
oktaOrgURL = configFileData['oktaOrgURL']+"/api/v1/users"
oktaAPIKey="SSWS "+configFileData['oktaAPIKey']

# Set Headers for Get Users Request
headers = {
    'Accept': "application/json",
    'Content-Type': "application/json",
    'Authorization': oktaAPIKey,
    'cache-control': "no-cache",
    }

# Make Inital Get Users Request
initialOktaGetUserRequest = requests.get(oktaOrgURL, headers=headers, params='"limit":"200"')

# Extract Initial Get User Request Response
userslist=[]
userslist=initialOktaGetUserRequest.json()
print("Processed ",len(userslist) ," Users")

if len(initialOktaGetUserRequest.headers['link'].split(","))>=2: # Check if a pagination cursor was set in the return headers
    paginationCursor=(initialOktaGetUserRequest.headers['link'].split(",")[1].split("?after=")[1].split("&limit")[0]) # Get Pagination Cursor
    # Loop through making get user calls while a pagination cursor stil exists
    while len(paginationCursor)>=21:
        querystring = {"limit":"200","after":paginationCursor} # Set Next Query String with Pagination Cursor
        oktaGetUserRequest = requests.get(oktaOrgURL, headers=headers, params=querystring)
        userslist=userslist+oktaGetUserRequest.json() # extract JSON response
        print("Processed ",len(userslist) ," Users")
        if len(oktaGetUserRequest.headers['link'].split(","))>=2:
            paginationCursor=(oktaGetUserRequest.headers['link'].split(",")[1].split("?after=")[1].split("&limit")[0])
        else:
            break

# Add ID attribute to headers list
masterProfileHeadersList=["id"]

# As Okta only shows set attributes, loop through all users to get all attributes (to save having to go through user schema and process it API call)
for user in userslist:
    for profileItem in user['profile']:
        masterProfileHeadersList.append(profileItem)
        masterProfileHeadersList=list(set(masterProfileHeadersList))


userListNoKeys=[]

# Remove keys from users list
for user in userslist:
    rowData=[]
    for attribute in masterProfileHeadersList:
        if attribute == "id":
            rowData.append(user['id'])
        elif attribute in user['profile']:
            rowData.append(user['profile'][attribute])
        else:
            rowData.append(" ")
    userListNoKeys.append(rowData)

# Write to CSV
with open('allOktaUsers.csv', 'w', newline='') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(masterProfileHeadersList)
    for user in userListNoKeys:
        writer.writerow(user)
    totalUsersRow="Total Users: ",len(userslist)
    writer.writerow(totalUsersRow)
csvFile.close()