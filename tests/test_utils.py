
""" Utilities for testing """

import os
import json

def get_pass(pass_name : str):
    """ Returns pass from test_credentials.json """

    creds_path = os.path.join(os.path.dirname(__file__), 'test_credentials.json')
    with open(creds_path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            creds = json.loads(line)

    return creds[pass_name]
