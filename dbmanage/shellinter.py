
""" A module to handle the interactions between dbmanage and shell """

import os
import re
import subprocess
import time

from .query_utils import parse_connection_request

# API

def connect(dbtype: str, **kwargs) -> subprocess.Popen:
    """ Creates a connection to the database server """

    # create subprocess
    process = subprocess.Popen('/bin/bash', shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=10)

    # connect process to database server
    stderr_out = 'errtemp'
    cmd = parse_connection_request(dbtype, stderr=stderr_out, **kwargs)

    # debug
    print(cmd)

    process.stdin.write(bytes(cmd, 'utf-8')) # type: ignore

    # get stderr from errtemp file
    error_msg = _get_stderr(stderr_out)
    print(error_msg)
    if error_msg:
        process.communicate()
        raise ConnectionRefusedError(error_msg)


    return process

def write_queries(process: subprocess.Popen, queries: list[str]) -> None:
    """ Writes queries in process.stdin """

    for query in queries:
        process.stdin.write(bytes(query, 'utf-8')) # type: ignore

# helper functions

def _get_stderr(filepath: str) -> str:
    """ Checks file for error messages """

    # wait until error file is generated
    #while(not os.path.exists(filepath)):
    #    pass

    # TEMPORARY SOLUTION
    time.sleep(.018)

    error_msg = ''
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            errlines = f.readlines()
        error_msg = '\n'.join([
            line for line in errlines
            if re.search('error', line.lower())
        ])
        print(error_msg)
        print(errlines)

    # remove file
    if os.path.exists(filepath):
        os.remove(filepath)

    return error_msg
