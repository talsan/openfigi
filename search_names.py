import requests
import config
import json
import pandas as pd
import time
import re

pd.set_option('max_rows', 500)
pd.set_option('max_columns', 1000)
'''
See https://www.openfigi.com/api for more information.
'''

openfigi_apikey = config.api_key
xls = pd.ExcelFile(config.holdings_xls)
fq = pd.read_excel(xls, config.holdings_xls_sheet)

acwi = pd.read_csv(config.id_meta_file, keep_default_na=False)

# map exchanges
# https://stockmarketmba.com/globalstockexchanges.php
acwi['exchange_ib'] = acwi['Financial Instrument.1'].str.extract('\s([A-Z].*)$')
exchange_map = {
    'IBIS': 'GY',  # e.g. xetra(ibis) maps to GY bloomberg exchange id
    'SEHK': 'HK',
    'FWB': 'GF',
    'FWB2': 'GF',
    'SBF': 'FP',
    'AEB': 'NA',
    'LSE': 'LN',
    'TSE': 'JT',
    'SFB': 'SS',
    'SWB2': 'GS'}
acwi['exchange_bb'] = acwi['exchange_ib'].apply(lambda x: exchange_map.get(x)).fillna('US')

fq_w_info = fq.merge(acwi, how='left', left_on='Description', right_on='Company Name')
fq_w_info = fq_w_info.dropna(subset=['Company Name'])

jobs = []
for i, row in fq_w_info.iterrows():
    if re.search('(\s|-)(ADR|GDR)',row['Company Name']):
        sec_type = 'Depositary Receipt'
    else:
        sec_type = 'Common Stock'

    job = {'job_id': i,
           'payload': {
               'query': row['Company Name'],
              #'currency': row['Trading Currency'],
               'exchCode': row['exchange_bb'],
               'securityType2': sec_type,
               'marketSecDes': 'Equity'}}
    jobs.append(job)

def request_figi(job_payload, sleep_time=65):
    response = requests.post(url='https://api.openfigi.com/v2/search',
                             headers={'Content-Type': 'application/json',
                                      'X-OPENFIGI-APIKEY': openfigi_apikey},
                             data=json.dumps(job_payload))
    retry_count = 0
    while response.status_code == 429:
        retry_count += 1
        print(f'retry number {retry_count}; waiting {sleep_time} seconds before next request...')
        time.sleep(sleep_time)
        response = request_figi(job_payload)

    return response

jobs_df = pd.DataFrame()
id_maps = pd.DataFrame()
for i, job in enumerate(jobs):
    print(job)

    job_df = pd.DataFrame(job['payload'],index=[i])
    job_df.insert(0, 'job_id', job['job_id'])
    jobs_df = jobs_df.append(job_df)

    response = request_figi(job['payload'])
    id_map = pd.json_normalize(response.json()['data'])
    id_map.insert(0, 'job_id', job['job_id'])
    id_maps = id_maps.append(id_map, ignore_index=True)

# merge back to input
id_map_all = jobs_df.merge(id_maps,how='left',on='job_id')

#



# deal with duplicates

id_maps.groupby('job_id').size().max()

print(json.dumps(response.json(), indent=4))
