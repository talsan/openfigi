import requests
import config
import json
import pandas as pd

'''
See https://www.openfigi.com/api for more information.
'''

openfigi_apikey = config.api_key
xls = pd.ExcelFile('./tci_names/Focused Quality Holdings as of 3_23_2021.xlsx')
fq = pd.read_excel(xls,'ACWI-ex_US')
acwi = pd.read_csv('./tci_names/Acwi_today.csv')

fq_w_info = fq.merge(acwi,how='left',left_on='Description',right_on='Company Name')
fq_w_info = fq_w_info.dropna(subset=['Company Name'])
jobs = []
for i, row in fq_w_info.iterrows():
    if (' ADR' in row['Company Name']) or (' GDR' in row['Company Name']):
        sec_type = 'Depositary Receipt'
    else:
        sec_type = 'Common Stock'

    job = {'query': row['Company Name'],
           'currency': row['Trading Currency'],
           'securityType2': sec_type,
           'marketSecDes': 'Equity'}

maps = []
for job in jobs:
    response = requests.post(url='https://api.openfigi.com/v2/search',
                             headers={'Content-Type': 'application/json',
                                      'X-OPENFIGI-APIKEY':openfigi_apikey},
                             data=json.dumps(jobs))

    map = pd.json_normalize(response.json()['data'])
    map
print(json.dumps(response.json(),indent=4))