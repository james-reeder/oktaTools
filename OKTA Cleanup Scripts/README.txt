**********************************************
Python Cleanup Tools

Created By Distology
Documentation Author: Alice Broadhurst
Developer: Alice Broadhurst

The following folder should include:
cleanAll.py
cleanApps.py
cleanAuthorizationServers.py
cleanGroupRules.py
cleanGroups.py
cleanIdps.py
cleanUsers.py
cleanZone.py
README.txt
**********************************************

		//// Tool Notes \\\\
		
=======
Logging
=======
A log file will be created/added to each time a script is run. The filename is based of the date of when the script is ran. For example: '16102019.txt' means the script was ran on the 16/10/2019. The logs 
will display the following contents:
	*Which script was ran
	*The ignored objects (by identifying information)
	*Which objects were deleted/deactivated
	*Which objects failed to be deleted/deactivated
	*How many objects were found
	*How many objects were ignored
	*How many objects remain in the tenant

=====
Zones
=====
Zones API was in early access during creation. The tools was constructed based on the logic of other API formats and should not break from any future changes.
The feature must be enabled in the tenant for the cleanup script to work, otherwise it will be ignored and display an appropiate message. 
However should it break please; refer to the Okta documentation for the fix: https://developer.okta.com/docs/reference/api/zones/ .

===================
Authorization Servers
===================
The cleanup script will only work if the feature is enable otherwise it is ignored and will display the appropiate message.

================
Clean All Script
================
The clean up all script contains 60 seconds breaks inbetween each script. This will stop any errors from happening if the scripts reach the API limit.

===========
All Scripts
===========
The script individually are not programmed to take in account for limits as they don't reach the limits while being run however if you run them one after another or alongside each other on the same Okta Organisation 
then you may hit these limits. If the command window does not display any new information for 5-10 minutes then close the command windows and rerun the script.

================
Ignoring Objects
================
To ignore objects, you will need to place them inbetween the <ignore> tags in your config. Please do the delete the ignore tags as it may stop the script from functioning however you can delete all objects inbetween 
the ignore tags. Please double check the information you place in the ignore tags as it must be the absolute values to work(do not add any unnecessary spacing) Please see 'Setting up' for more information.

		//// Setting up \\\\
		
================
Okta Information
================
You need to replace the information in the config.xml file to run the scripts on a particular OKTA tenant. 

You will need the following
	*Okta Tenant URL (For Example: https://test.oktapreview.com )
	*API Token
	
Ensure you Okta Tenant URL contains 'https://' at the start and does not have a '/' at the end.
Ensure that the API Token supplied does not have the suffix at the start (i.e. SSWS)

[STEP 1]
Place the Okta Tenant URL in the <oktaUrl> tags:
	
	<oktaUrl>https://test.oktapreview.com</oktaUrl>
	
[STEP 2]
Place the API token in the <oktaToken> tags:

	<oktaToken>000000000000</oktaToken>
	
[STEP 3]
Place the objects identifying information in between the <ignore> tags with the appropiate tags.

--To ignore a user, place the user's login inbetween <user> tags.

	<user>abroadhurst@distology.com</user>
	
--To ignore a group, place the groups's name inbetween <group> tags.

	<group>Admins</group>

--To ignore a rule, place the rule's name inbetween <rule> tags.

	<rule>ToAdminGroup</rule>
	
--To ignore an app, place the app's id inbetween <app> tags.

	<app>0oanskx4b0ML1i6Hq0h7</app>
	
--To ignore an idp, place the idp's name inbetween <idp> tags.

	<idp>MainProfileMaster</idp>
	
--To ignore an authorization server, place the server's name inbetween <server> tags.

	<server>default</server>
	
--To ignore an zone, place the zone's name inbetween <zone> tags.

	<zone>Main Site</zone>
	
The main config should look something like below once you have place the appropiate information:

<config>
	<oktaUrl>https://test.oktapreview.com</oktaUrl>
	<oktaToken>000000000000</oktaToken>
	<ignore>
		<user>abroadhurst@distology.com</user>
		<group>Admins</group>
		<rule>ToAdminGroup</rule>
		<app>0oanskx4b0ML1i6Hq0h7</app>
		<idp>MainProfileMaster</idp>
		<server>default</server>
		<zone>Main Site</zone>
	</ignore>
</config>

or:

<config>
	<oktaUrl>https://test.oktapreview.com</oktaUrl>
	<oktaToken>000000000000</oktaToken>
	<ignore></ignore>
</config>

[STEP 4]
Run the appropiate scripts in the command line

When in current working directory:
python <scriptFileName>.py 
or
python <locationOfScripts>/<scriptFileName>.py 
***************************************************************************************************************


	
	
