import config
import pandas as pd
import re
import openfigi_api

pd.set_option('max_rows', 500)
pd.set_option('max_columns', 1000)

mapper_output = './mapper_outputs/fq_20210630.csv'
openfigi_apikey = config.api_key

# read the files
fq = pd.concat([pd.read_csv('./tci_names/US_FQ_2021_06_30.csv'),])
#fq = fq[['SYMBOL', 'Company Name']]

# map exchanges
# https://stockmarketmba.com/globalstockexchanges.php
# go to interactive brokers website: https://www.interactivebrokers.com/en/index.php?f=1562
fq['SYMBOL'] = fq['SYMBOL'].str.replace('\.', '', regex=True)
fq['exchange_ib'] = fq['SYMBOL'].str.extract('\s([A-Z0-9]*)$')
fq['ticker_local'] = fq['SYMBOL'].str.extract('^([A-Z0-9]*)\s?')
exchange_map = {
    'IBIS': 'GY',  # e.g. xetra(ibis) maps to GY bloomberg exchange id
    'SEHK': 'HK',
    'FWB': 'GF',
    'FWB2': 'GF',
    'SBF': 'FP',
    'AEB': 'NA',
    'LSE': 'LN',
    'TSE': 'CN',
    #'TSE': 'JT',
    'SFB': 'SS',
    'SWB2': 'GS'
    #'CN': 'CN'
    }
fq['exchange_bb'] = fq['exchange_ib'].apply(lambda x: exchange_map.get(x)).fillna('US')
fq_w_info = fq.dropna(subset=['ticker_local']).drop_duplicates()

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
           'marketSecDes': 'Equity',
           'includeUnlistedEquities': True}
    jobs.append(job)


job_chunks = [jobs[x:x + 100] for x in range(0, len(jobs), 100)]
id_maps = openfigi_api.map_jobs(job_chunks)

all_data = fq_w_info.merge(id_maps,how='left',left_on='ticker_local',right_on='ticker')

all_data.to_csv(mapper_output,index=False)