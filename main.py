import os
import json
import pandas
from getServiceNowData import getServiceNowData
from setGoogleSheetsData import setGoogleSheetsData

# clear terminal
os.system("clear")  # Linux - OSX

# You must have a json file in ./creds called google_secret.json
# Download the json file from Google
CREDSPATH = os.getcwd() + '/credentials'

# Finds path of /credentials directory and ServiceNow credentials
with open(CREDSPATH+'/sn_config.json') as json_file:
    CREDENTIALS = json.load(json_file)

# Gets Hardware Assets data from ServiceNow instance
SNDATA = getServiceNowData(CREDENTIALS)

# Pushes the data to a Google Sheet
setGoogleSheetsData(CREDSPATH, SNDATA)
