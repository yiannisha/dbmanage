
""" Utilities for testing """

import os
import json

TESTDATADIR = os.path.join(os.path.dirname(__file__), 'testdata')

def get_pass(pass_name : str) -> str:
    """ Returns pass from test_credentials.json """

    creds_path = os.path.join(os.path.dirname(__file__), 'test_credentials.json')
    with open(creds_path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            creds = json.loads(line)

    return creds[pass_name]

def read_temp_file(filename: str, delete = True, stdout: str = '',  stderr: str = '') -> str:
    """ Reads temp file and returns contents """

    # wait for file to be generated
    print(f'Waiting for {filename} file...')
    try:
        while(not os.path.exists(filename)):
            pass
    except KeyboardInterrupt as e:
        error_msg = f'Stdout: {stdout}\nStderr: {stderr}\n'
        raise Exception(error_msg)

    # read file
    with open(filename, 'r', encoding='utf-8') as f:
        out_str = ''.join([line for line in f.readlines()])

    # delete file
    if delete and os.path.exists(filename):
        try:
            os.remove(filename)
        except:
            print(f'{filename} file already removed')

    return out_str
