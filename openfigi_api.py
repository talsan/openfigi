import pandas as pd
import requests
import config
import time
import json


def map_jobs(job_chunks):
    id_maps = pd.DataFrame()
    job_id = 0
    for j, jc in enumerate(job_chunks):
        print(f'chunk {j}')

        if (j > 0) & (j % 24 == 0):
            print('sleeping 6 seconds... ')
            time.sleep(6)

        response = requests.post(url='https://api.openfigi.com/v2/mapping',
                                 headers={'Content-Type': 'application/json',
                                          'X-OPENFIGI-APIKEY': config.openfigi_key},
                                 data=json.dumps(jc))

        for i, r in enumerate(response.json()):
            if r.get('error') is None:
                id_map = pd.json_normalize(r, 'data')
                id_map.insert(0, 'job_id', job_id)
                id_maps = id_maps.append(id_map)
            else:
                print(i)
                print(jc[i])
            job_id += 1

    return id_maps

def search_job(job,sleep_time=65):

    response = requests.post(url='https://api.openfigi.com/v2/search',
                             headers={'Content-Type': 'application/json',
                                      'X-OPENFIGI-APIKEY': config.openfigi_key},
                             data=json.dumps(job))
    retry_count = 0
    while response.status_code == 429:
        retry_count += 1
        print(f'retry number {retry_count}; waiting {sleep_time} seconds before next request...')
        time.sleep(sleep_time)
        response = search_job(job,sleep_time)

    return response

def search_jobs(jobs, sleep_time=65):
    id_maps = pd.DataFrame()
    for j in jobs:
        response = search_job(j['payload'],sleep_time)
        r_json = response.json()
        if r_json.get('error') is None:
            id_map = pd.json_normalize(response.json(), 'data')
            id_map.insert(0, 'job_id', j['job_id'])
            id_maps = id_maps.append(id_map)
        else:
            print(j)

    return id_maps
