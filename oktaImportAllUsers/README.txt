**********************************************
Python Okta Users Importing Tool

Created By Distology
Documentation Author: Alice Broadhurst
Developer: Alice Broadhurst

The following folder should include:
config.xml
oktaImportAllUsers.py
README.txt

Verison 2:
Added updating users
Added validity checks

**********************************************

		//// Tool Notes \\\\
		
=======
Logging
=======
A log file will be created/added to each time a script is run. The filename is based of the date of when the script is ran. For example: '16102019.txt' means the script was ran on the 16/10/2019. The logs 
will display the following contents:
	*When the script was ran
	*When the script ended
	*Any errors produced such as
		*any users that failed to be created (and why)
		*if the csv file could not be found
		*if the config was set incorrectly
		*if any mappings were set incorrectly
		

========
Mappings
========
Mappings are not required to be in the config however you can include it to override the headers within the csv file.
When adding a mapping you will need to place the column name and okta's equivalent name into the mapping values. Please note that you can only include Okta's profile variables. Any other Okta variables such as id
cannot be altered using this script. 

Here is an example of what you mappings might look like:
<mappings>
	<mapping>
		<csvHeader>id</csvHeader>
		<oktaAttribute>employeeNumber</oktaAttribute>
	</mapping>
</mappings>

=================
CSV File Location
=================
For the csv location in the config, you can you a cannoical or absolute path as you please. The log file will also print the absolute path if the file could not be found.


===============
Validity Checks
===============
The importer will now ensure that each user create meets the basic standard Okta user by checking that each users has the following attributes:
	*Login
	*Email
	*FirstName
	*LastName
Any rows that do not meet this requirement are ignored. 

=============
Empty Columns
=============
If a column is empty then it is not included in the user that is created. 

=============
Booleans
=============
If you have columns that contain a capitalised boolean such as 'TRUE' or 'FALSE'. The value of the column will be changes to 'true' or 'false' respectively.


		//// Setting up \\\\
		
================
Okta Information
================
You need to replace the information in the config.xml file to run the scripts on a particular OKTA tenant. 

You will need the following
	*Okta Tenant URL (For Example: https://test.oktapreview.com )
	*API Token
	*File Location
	
Ensure you Okta Tenant URL contains 'https://' at the start and does not have a '/' at the end.
Ensure that the API Token supplied does not have the suffix at the start (i.e. SSWS)
Ensure that your file location is accessable and is a .csv file.

[STEP 1]
Place the Okta Tenant URL in the <oktaUrl> tags:
	
	<oktaUrl>https://test.oktapreview.com</oktaUrl>
	
[STEP 2]
Place the API token in the <apiToken> tags:

	<apiToken>000000000000</apiToken>
	
[STEP 3]
Place the file location in the <csvLocation> tags:

	<csvLocation>allOktaUsers.csv</csvLocation>
	
[STEP 4] (optional)
Add mapping tags to change the names of any columns in the csv to the okta equiliant names by placing them within <mapping> tags.
The name of the column in the file should be in <csvHeader> tags.
The Okta variable name should be in <oktaAttribute> tags.

Here is an example:
<mappings>
	<mapping>
		<csvHeader>id</csvHeader>
		<oktaAttribute>employeeNumber</oktaAttribute>
	</mapping>
</mappings>

	
The main config should look something like below once you have place the appropriate information:

<config>
  <oktaUrl>https://test.oktapreview.com</oktaUrl>
  <apiToken>000000000000</apiToken>
  <csvLocation>allOktaUsers.csv</csvLocation>
  <mappings>
	<mapping>
		<csvHeader>id</csvHeader>
		<oktaAttribute>employeeNumber</oktaAttribute>
	</mapping>
  </mappings>
</config>

[STEP 4]
Run the script in the command line

When in current working directory:
python <scriptFileName>.py 
or
python <locationOfScripts>/<scriptFileName>.py 
***************************************************************************************************************


	
	
