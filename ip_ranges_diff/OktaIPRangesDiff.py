# Import Required Modules
import requests
import pprint
import json
from deepdiff import DeepDiff
from deepdiff import grep, DeepSearch
from deepdiff import DeepHash

print ('--- Starting IP Ranges Diff Script ---')

# Read in Old IP Data
try:
    with open('ip_ranges_diff/old_ip_ranges.json') as json_file:
        oldIpData = json.load(json_file)
    #Read in Latest IP Data
    newIpData = requests.get('https://s3.amazonaws.com/okta-ip-ranges/ip_ranges.json').json()

    with open('ip_ranges_diff/old_ip_ranges.json', 'w') as outfile:
        json.dump(newIpData, outfile)

    dataDiff = DeepDiff(newIpData, oldIpData, ignore_order=True)

    if not dataDiff:
        print ('- No differences detected -')
    else:
        print ("- Differences were detected -")
        with open('ip_ranges_diff/ip_ranges_diff.diff', 'w') as outfile:
            json.dump(dataDiff, outfile)
except IOError:
    print("Error: Cannot find old_ip_ranges.json file. Creating file for next run time.")
    #Read in Latest IP Data
    newIpData = requests.get('https://s3.amazonaws.com/okta-ip-ranges/ip_ranges.json').json()

    with open('ip_ranges_diff/old_ip_ranges.json', 'w') as outfile:
        json.dump(newIpData, outfile)

print ('--- Completing IP Ranges Diff Script ---')







