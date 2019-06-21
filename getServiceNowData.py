import os
import json
import pysnow as snow
import pandas


def _readFile(FILE):
    try:
        # Read data from file 'filename.csv'
        data = pandas.read_csv(FILE, encoding='utf-8')
        print('Data file read...')
        return data
    except:
        print('An error occurred while attempting to read the file.')
        return


def getServiceNowData(FILEPATH):
    print('Finding data file: ' + FILEPATH)
    exists = os.path.isfile(FILEPATH)
    if exists:
        print('Data file found...')
        data = _readFile(FILEPATH)
        return data
    else:
        print('Data file was not found...')
        return exists
