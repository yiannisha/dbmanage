
""" A module for query parsing utilities """

from typing import Union

# API

def parse_connection_request(dbtype: str, **kwargs) -> str:
    """ Returns a string command to be run by a subprocess """

    connection = ''

    if dbtype == 'mysql':
        connection = _parse_mysql_connection_request(**kwargs)
    elif dbtype == 'postgres':
        connection = _parse_psql_connection_request(**kwargs)

    return connection

# helper functions

def _parse_mysql_connection_request(host: str, user: str, dbname: str = '', passwd: str = '', **kwargs) -> str:

    base_cmd = ''
    try:
        pass_str = ''
        if passwd:
            pass_str = f'-p{passwd}'

        base_cmd = f'mysql -h {host} -u {user} {pass_str} {dbname}\n'
    except KeyError as e:
        # TODO: properly handle missing args
        raise ValueError('')

    return base_cmd

def _parse_psql_connection_request(host: str, user: str, dbname: str = '', passwd: str = '', port: Union[int, str] = 5432 ) -> str:

    base_cmd = ''
    try:
        pass_str = ''
        if passwd:
            pass_str = f'--password{passwd}'

        base_cmd = f'psql -h {host} -U {user} -p {port} {pass_str} {dbname}\n'
    except KeyError as e:
        # TODO: properly handle missing args
        raise ValueError('')

    return base_cmd
