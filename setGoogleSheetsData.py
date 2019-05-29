import os
from gspread_pandas import Spread, conf


def setGoogleSheetsData(CREDSPATH, DATAFRAME):

    SHEETID = '1I4BoAF7zdB3QHFGMyphvp-QwLhYZ-nWsxaTIa3zuRJ0'
    SHEETTAB = 'alm_hardware'

    # Connect to the Google Sheets file
    spread = Spread('sn_datapusher', SHEETID,
                    0, conf.get_config(conf_dir=CREDSPATH, file_name='google_secret.json'))
    print('Spreadsheet loaded...')

    # Copies dataframe to google sheet
    spread.df_to_sheet(DATAFRAME, index=False, sheet=SHEETTAB,
                       start='A1', replace=True,)
