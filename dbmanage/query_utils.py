
""" A module for query parsing utilities """

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
