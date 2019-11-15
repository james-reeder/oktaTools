 # Okta Export All Users Script

This script will export a list of all users and their associated attributes into a CSV file.

## Getting Started

Download the **oktaExportAllUsers.py** file and **config.json** to your working directory. 

## Running the Script

Add your Okta Org Base URL and Okta API Key to your **config.json** file. Thens simply run **oktaExportAllUsers.py** script. All users will then be exported to a CSV **named allOktaUsers.csv**

## Mac Key Support

You can choose what will replace the Mac only keys at the top of the script by changing the replacment key value. The current default will change it to an apostrophe (').

## Export with Specific App Profiles

**oktaExportAllUsers.py** will allow you to export the users with a specific app profile. Add 'appId' to the **config** and add the app ID as it's value. The app profile of the user will show up to the right of the of the 'app' column.
If the user does not have a profile with the app then the app column will be empty otherwise it will be filled with the appId of the app it is associated with.
You must set 'appId' in the **config** otherwise the following error will be display: 'Your config has not been set correctly'.
If you alter the config incorrectly the error above can also be displayed. Try redownloading the config if you are persistantly getting this error.
If you want to use this script to export all users then leave 'appId' value in the config to '' and it will work.
