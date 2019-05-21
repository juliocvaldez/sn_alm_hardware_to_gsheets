import os
import json
import pysnow as snow
import pandas as pd
from gspread_pandas import Spread, conf

# clear terminal
os.system("clear")  # Linux - OSX

# Finds path of current directory
pypath = os.getcwd()

# Finds path of /creds directory and ServiceNow credentials
with open('creds/sn_config.json') as json_file:
    creds = json.load(json_file)

store = {'token': None}

# Takes care of refreshing the token storage if needed


def updater(new_token):
    print("OAuth token refreshed!")
    store['token'] = new_token


# Create the OAuthClient with the ServiceNow provided `client_id` and `client_secret`, and a `token_updater`
# function which takes care of refreshing local token storage.
s = snow.OAuthClient(
    client_id=creds['CLIENT_ID'],
    client_secret=creds['CLIENT_SECRET'],
    token_updater=updater,
    instance=creds['INSTANCE']
)

if not store['token']:
    # No previous token exists. Generate new.
    store['token'] = s.generate_token(creds['USERNAME'], creds['PASSWORD'])

# Set the access / refresh tokens
s.set_token(store['token'])

# Define fields to pull from table
fields = [
    'asset_tag',
    'ci.host_name',
    'ci.mac_address',
    'company',
    'cost',
    'department',
    'display_name',
    # 'end_of_depreciation',
    # 'end_of_life_year',
    'install_date',
    'install_status',
    'invoice_number',
    'location',
    'model',
    'model.depreciation',
    'model.manufacturer',
    'model_category',
    'po_number',
    'purchase_date',
    'residual',
    'retired',
    'retirement_date',
    'serial_number',
    'substatus',
    'u_business_services',
    'u_uc_property_tag'
]

# Build query
qb = (
    snow.QueryBuilder()
        .field('company.name').equals('INFR')
        .OR()
        .field('company.name').equals('NCS')  # NCS
        .OR()
        .field('company.name').equals('EUC')  # NCS
        .AND()
        .field('company').order_ascending()
        .AND()
        .field('display_name').order_ascending()
)

# Define a resource, here we'll use the Hardware Assets table API
assets = s.resource(api_path='/table/alm_hardware')

# Set request paramaters
assets.parameters.display_value = True
assets.parameters.exclude_reference_link = True

# Query for assets
response = assets.get(query=qb, stream=True, fields=fields)
print('Assets received...')

# Iterate over the result and
list = []
for record in response.all():
    list.append(record)

# Creates a dataframe from the query
df = pd.read_json(json.dumps(list), orient='records')
print('Dataframe created...')

# You must have a json file in .\creds called google_secret.json
# Download the json file from Google
credspath = pypath + '/creds'
googleSheetId = '1I4BoAF7zdB3QHFGMyphvp-QwLhYZ-nWsxaTIa3zuRJ0'
sheetTabNm = 'alm_hardware'
spread = Spread('sn_datapusher', googleSheetId,
                0, conf.get_config(conf_dir=credspath, file_name='google_secret.json'))
print('Spreadsheet loaded...')

# Copies dataframe to google sheet
spread.df_to_sheet(df, index=False, sheet=sheetTabNm,
                   start='A1', replace=True,)
print('Spreadsheet updated!')
