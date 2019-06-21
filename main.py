import sys
import os
import json
import pandas
from getServiceNowData import getServiceNowData
from setGoogleSheetsData import setGoogleSheetsData

# clear terminal
os.system("clear")  # Linux - OSX

# Set current working directory
CWD = '/data/servicenow/'

# Look for parameters or set defaults
if sys.argv[1]:
    FILEPATH = CWD + sys.argv[1]
else:
    FILEPATH = CWD + 'assets/sn_alm_hardware.csv'

if sys.argv[2]:
    SHEETID = sys.argv[2]
else:
    SHEETID = '1I4BoAF7zdB3QHFGMyphvp-QwLhYZ-nWsxaTIa3zuRJ0'

if sys.argv[3]:
    SHEETTAB = sys.argv[3]
else:
    SHEETTAB = 'alm_hardware'

# Finds path of /credentials directory and ServiceNow credentials
# You must have a json file in ./credentials called google_secret.json
# Download the json file from Google
# CREDSPATH = CWD + 'bin/alm_hardware_to_gsheets/credentials'
CREDSPATH = os.getcwd() + '/credentials'
CREDSEXISTS = os.path.isdir(CREDSPATH)
if not CREDSEXISTS:
    CREDSPATH = CWD + 'bin/alm_hardware_to_gsheets/credentials'
    CREDSEXISTS = os.path.isdir(CREDSPATH)

if not CREDSEXISTS:
    print('>>> No credentials directory found.')


with open(CREDSPATH+'/sn_config.json') as json_file:
    CREDENTIALS = json.load(json_file)

# Gets Hardware Assets data from ServiceNow instance
SNDATA = getServiceNowData(FILEPATH)

if not type(SNDATA) == bool:
    # Pushes the data to a Google Sheet
    setGoogleSheetsData(CREDSPATH, SNDATA, SHEETID, SHEETTAB)
    print('>>> Data push to Google Sheets complete.')
else:
    print('>>> No action was taken.')
