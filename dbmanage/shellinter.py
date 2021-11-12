
""" A module to handle the interactions between dbmanage and shell """

import os
import subprocess

from .query_utils import parse_connection_request

# API

def connect(dbtype: str, **kwargs) -> subprocess.Popen:
    """ Creates a connection to the database server """

    # create subprocess
    process = subprocess.Popen('/bin/bash', shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=10)

    # connect process to database server
    cmd = parse_connection_request(dbtype, **kwargs)

    # debug
    #print(cmd)

    process.stdin.write(bytes(cmd, 'utf-8')) # type: ignore

    return process

def write_queries(process: subprocess.Popen, queries: list[str]) -> None:
    """ Writes queries in process.stdin """

    for query in queries:
        process.stdin.write(bytes(query, 'utf-8')) # type: ignore

# helper functions
