import pandas
import json
from gspread_pandas import Spread, conf


def setGoogleSheetsData(CREDSPATH, SNDATA, SHEETID, SHEETTAB):
    # Connect to the Google Sheets file
    spread = Spread('sn_datapusher', SHEETID,
                    0, conf.get_config(conf_dir=CREDSPATH, file_name='google_secret.json'))
    print('Spreadsheet loaded...')

    # Copies dataframe to google sheet
    spread.df_to_sheet(SNDATA, index=False, sheet=SHEETTAB,
                       start='A1', replace=True,)
    print('Spreadsheet updated!')
