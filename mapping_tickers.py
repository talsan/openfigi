import requests
import config
import json
import pandas as pd
import re

pd.set_option('max_rows', 500)
pd.set_option('max_columns', 1000)

openfigi_apikey = config.api_key
xls = pd.ExcelFile(config.holdings_xls)
fq = pd.read_excel(xls, config.holdings_xls_sheet)

acwi = pd.read_csv(config.id_meta_file, keep_default_na=False)
# edits = NA TSE --> NA

# map exchanges
# https://stockmarketmba.com/globalstockexchanges.php
acwi['Financial Instrument.1'] = acwi['Financial Instrument.1'].str.replace('\.', '',regex=True)
acwi['exchange_ib'] = acwi['Financial Instrument.1'].str.extract('\s([A-Z0-9]*)$')
acwi['ticker_local'] = acwi['Financial Instrument.1'].str.extract('^([A-Z0-9]*)\s?')
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
    'SWB2': 'GS',
    'CN': 'CN'}
acwi['exchange_bb'] = acwi['exchange_ib'].apply(lambda x: exchange_map.get(x)).fillna('US')

fq_w_info = fq.merge(acwi, how='left', left_on='Description', right_on='Company Name')
fq_w_info = fq_w_info.dropna(subset=['ticker_local'])

jobs = []
for i, row in fq_w_info.iterrows():
    if re.search('(\s|-)(ADR|GDR)', row['Company Name']):
        sec_type = 'Depositary Receipt'
    else:
        sec_type = 'Common Stock'

    job = {'idType': 'TICKER',
           'idValue': row['ticker_local'],
           'exchCode': row['exchange_bb'],
           'securityType2': sec_type,
           'marketSecDes': 'Equity'}
    jobs.append(job)

response = requests.post(url='https://api.openfigi.com/v2/mapping',
                         headers={'Content-Type': 'application/json',
                                  'X-OPENFIGI-APIKEY': openfigi_apikey},
                         data=json.dumps(jobs))

id_maps = pd.DataFrame()
for i,r in enumerate(response.json()):
    if r.get('error') is None:
        id_map = pd.json_normalize(r, 'data')
        id_map.insert(0,'job_id',i)
        id_maps = id_maps.append(id_map)
    else:
        print(i)
        print(jobs[i])

jobs_df = pd.DataFrame(jobs).reset_index().rename(columns={'index':'job_id'})

# merge back to input
id_map_all = jobs_df.merge(id_maps, how='left', on='job_id')

# assert no misses
assert(id_map_all['compositeFIGI'].isna().sum()==0)

# assert no duplicates
assert(id_map_all.groupby('job_id').size().max()==1)
