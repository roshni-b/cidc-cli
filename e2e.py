#!/usr/bin/env python3
"""
A script that mocks the CLI to run an end-to-end workflow test.
"""
import time
from os import environ as env
import requests
from cidc_utils.requests import SmartFetch
from utilities.cli_utilities import create_payload_objects
from upload.upload import upload_files

DOMAIN = env.get('DOMAIN')
CLIENT_SECRET = env.get('CLIENT_SECRET')
CLIENT_ID = env.get('CLIENT_ID')
AUDIENCE = env.get('AUDIENCE')


def get_token() -> dict:
    """
    Fetches a token from the auth server.

    Returns:
        dict -- Server response.
    """
    payload = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'audience': AUDIENCE
    }
    res = requests.post("https://cidc-test.auth0.com/oauth/token", json=payload)

    if not res.status_code == 200:
        print(res.reason)
    else:
        print('token fetched succesfully')

    return {
        'access_token': res.json()['access_token'],
        'expires_in': res.json()['expires_in'],
        'time_fetched': time.time()
    }

# Get token
EVE_TOKEN = get_token()['access_token']

EVE_URL = 'http://' + env.get(
    'INGESTION_API_SERVICE_HOST') + ':' + env.get('INGESTION_API_SERVICE_PORT')
# Set up connection to API
EVE_FETCHER = SmartFetch(EVE_URL)

# Mock Trial
HELLO_TRIAL = {
    "_id": "5ac674521e478003ad494cd0",
    "trial_name": "test_trial",
    "principal_investigator": "lloyd",
    "start_date": "2018-04-05T19:09:06.062Z",
    "samples": ["FOO"],
    "assays": [
        {
            "assay_name": "hello.wdl",
            "assay_id": "5ac674d81e478003ad494cd1"
        }
    ],
    "collaborators": ["mccarthy@bcb-mail.dfci.harvard.edu"]
}

# Mock Assay
HELLO_ASSAY = {
    "assay_id": "5ac674d81e478003ad494cd1",
    "assay_name": "hello.wdl",
    "non_static_inputs": ["wf_hello.hello.addressee"],
    "static_inputs": [
        {"key_name": "foo", "key_value": "bar"},
        {"key_name": "prefix", "key_value": ""}
    ],
    "wdl_location": "wdl/wes/hello.wdl"
}

UPLOAD_DIR = 'cidc-cli/sample_data/test'
UPLOAD_GUIDE = {
    "FOO123.txt": {
        "sample_id": "FOO",
        "mapping": "wf_hello.hello.addressee"
    }
}

# Create upload payload
UPLOAD_PAYLOAD = {
    'number_of_files': len(UPLOAD_GUIDE),
    'status': {
        'progress': 'In Progress'
    },
    'files': create_payload_objects(UPLOAD_GUIDE, HELLO_TRIAL, HELLO_ASSAY)
}

try:
    RESPONSE_UPLOAD = EVE_FETCHER.post(
        token=EVE_TOKEN, endpoint='ingestion', json=UPLOAD_PAYLOAD, code=201
    )
    print(RESPONSE_UPLOAD.json())
except RuntimeError:
    print("Eve error")


JOB_ID = upload_files(
    UPLOAD_DIR,
    [UPLOAD_GUIDE[key] for key in UPLOAD_GUIDE],
    RESPONSE_UPLOAD.json(),
    EVE_TOKEN,
    RESPONSE_UPLOAD.headers
)

DONE = False
COUNTER = 0
while not DONE and COUNTER < 200:
    STATUS_RESPONSE = EVE_FETCHER.get(
        token=EVE_TOKEN, endpoint='ingestion' + '/' + JOB_ID, code=200
        )
    if not STATUS_RESPONSE.status_code == 200:
        print("Error")
        time.sleep(200)

    PROGRESS = STATUS_RESPONSE.json()['status']['progress']
    if PROGRESS == 'In Progress':
        print('Upload is still in PROGRESS, check back later')
    elif PROGRESS == 'Completed':
        print('Upload is completed.')
        DONE = True
    elif PROGRESS == 'Aborted':
        print('Upload was aborted: ' + STATUS_RESPONSE.json()['status']['message'])
        raise RuntimeError
    time.sleep(30)
    COUNTER += 1

print("Job uploaded")

# Check if job is running.
PIPELINE_STATUS = EVE_FETCHER.get(token=EVE_TOKEN, endpoint="status").json()

PIPELINEDONE = False
P_COUNTER = 0
while not PIPELINEDONE and P_COUNTER < 200:
    if PIPELINE_STATUS['_items']:
        STATUS = PIPELINE_STATUS['_items'][0]['status']['progress']
        if STATUS == 'In Progress':
            print('Job is still in progress, check back later')
        elif STATUS == 'Completed':
            print('Job is completed.')
            PIPELINEDONE = True
        elif STATUS == 'Aborted':
            print('Job was aborted: ')
            print(PIPELINE_STATUS)
            raise RuntimeError
        time.sleep(30)
        P_COUNTER += 1
    else:
        print("No jobs found")
        raise RuntimeError