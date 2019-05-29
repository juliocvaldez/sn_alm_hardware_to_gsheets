import os
import json
import pandas
from gspread_pandas import Spread, conf
from getServiceNowData import getServiceNowData
from setGoogleSheetsData import setGoogleSheetsData

# clear terminal
os.system("clear")  # Linux - OSX

# Finds path of /credentials directory and ServiceNow credentials
with open('credentials/sn_config.json') as json_file:
    CREDENTIALS = json.load(json_file)

SNDATA = getServiceNowData(CREDENTIALS)
print('Assets received...')

# Creates a dataframe from the query
DATAFRAME = pandas.read_json(json.dumps(SNDATA), orient='records')
print('Dataframe created...')

# You must have a json file in ./creds called google_secret.json
# Download the json file from Google
CREDSPATH = os.getcwd() + '/credentials'

setGoogleSheetsData(CREDSPATH, DATAFRAME)
print('Spreadsheet updated!')
