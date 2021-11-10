
""" A module to handle the interactions between dbmanage and shell """

import os
import subprocess

# main module functions

def connect(dbtype: str, **kwargs) -> subprocess.Popen:
    """ Creates a connection to the database server """

    # create subprocess
    process = subprocess.Popen('/bin/bash', shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=10)

    # connect process to database server
    cmd = _parse_connection_request(dbtype, **kwargs)

    # debug
    #print(cmd)

    process.stdin.write(bytes(cmd, 'utf-8')) # type: ignore

    return process

# helper functions

def _parse_connection_request(dbtype: str, **kwargs) -> str:
    """ Returns a string command to be run by a subprocess """

    connection = ''

    if dbtype == 'mysql':
        connection = _parse_mysql_connection_request(**kwargs)
    elif dbtype == 'postgres':
        connection = _parse_psql_connection_request(**kwargs)

    return connection

def _parse_mysql_connection_request(**kwargs) -> str:

    base_cmd = ''
    try:
        pass_str = ''
        if kwargs['pass']:
            pass_str = f'-p{kwargs["pass"]}'

        base_cmd = f'mysql -h {kwargs["host"]} -u {kwargs["user"]} {pass_str} {kwargs["dbname"]}\n'
    except KeyError as e:
        # TODO: properly handle missing args
        raise ValueError('')

    return base_cmd

def _parse_psql_connection_request(**kwargs) -> str:

    base_cmd = ''
    try:
        pass_str = ''
        if kwargs['pass']:
            pass_str = f'--password{kwargs["pass"]}'

        base_cmd = f'psql -h {kwargs["host"]} -U {kwargs["user"]} -p {kwargs["port"]} {pass_str} {kwargs["dbname"]}\n'
    except KeyError as e:
        # TODO: properly handle missing args
        raise ValueError('')

    return base_cmd
