
""" A module for query parsing and output reading utilities """

import os
import re

from typing import Union, Dict, List

ColumnDict = Dict[str, List[str]]

# API

#  Helper functions for reading output
def _readrows(filepath: str, extra: bool = True) -> Dict:
    """
    Returns a dictionary with "column", "row", "extra" as keys
    and the lines of the file that contain each one as dictionary values.

    This function is to be called in self._readStdout and this code was
    refactored so that _readStdout could be overwritten without the need of
    rewriting the whole function.
    """

    if not os.path.exists(filepath):
        raise FileNotFoundError(f'File with query output not found.\npath: {filepath}')

    with open(filepath, 'r', encoding='utf-8') as f:

        column_str = ''
        row_strs = []
        extra_strs = []

        # read column line
        column_str = f.readline()
        while not _isrow(column_str):
            column_str = f.readline()
            if not column_str:
                break

        # get values from rows
        f.readline() # skip line right after the line with column names
        line = f.readline() # first row
        while(_isrow(line)):
            row_strs.append(line)
            line = f.readline()

        # get extra stuff
        if extra:
            extra_strs.append(line.strip())
            extra_strs.extend([line.strip() for line in f.readlines() if line.strip()])

    return {
        'column' : column_str,
        'row' : row_strs,
        'extra' : extra_strs,
    }

def _isrow(line: str) -> bool:
    """ Returns True if the line passed is a valid row of output """
    regex = '.*\|'
    return bool(re.search(regex, line))

def _untabulate(row_dict: Dict) -> ColumnDict:
    """
    Returns a dictionary with columns as keys and row data as values
    by formatting row strings.

    :param row_dict: a dictionary with row strings
    """

    columns = [
        column[1:].strip().lower() for column in row_dict['column'].split('|')
        if len(column.strip()) > 0 # no null names as columns
        ]
    columnDict = {key: [] for key in columns} # type: ignore

    for row in row_dict['row']:
        rowdata = [data.strip().lower() for data in row.split('|') if len(data) > 0]
        for data, column in zip(rowdata, columns):
            if data:
                columnDict[column].append(data)
            else:
                columnDict[column].append(None)

    return columnDict

#  Helper functions for connection requests
def parse_connection_request(dbtype: str, **kwargs) -> str:
    """ Returns a string command to be run by a subprocess """

    connection = ''

    if dbtype == 'mysql':
        connection = _parse_mysql_connection_request(**kwargs)
    elif dbtype == 'postgres':
        connection = _parse_psql_connection_request(**kwargs)

    return connection

def _parse_mysql_connection_request(host: str, user: str, dbname: str = '', passwd: str = '', **kwargs) -> str:

    base_cmd = ''
    pass_str = ''
    if passwd:
        pass_str = f'-p{passwd}'

    ERRFILE = ''
    if kwargs['stderr']:
        ERRFILE = f'2>{kwargs["stderr"]}'

    base_cmd = f'mysql -h {host} -u {user} {pass_str} {dbname} {ERRFILE}\n'

    return base_cmd

def _parse_psql_connection_request(host: str, user: str, dbname: str = '', passwd: str = '', port: Union[int, str] = 5432, **kwargs ) -> str:

    base_cmd = ''
    pass_str = ''
    if passwd:
        pass_str = f'PGPASSWORD={passwd}'

    ERRFILE = ''
    if kwargs['stderr']:
        ERRFILE = f'2>{kwargs["stderr"]}'

    base_cmd = f'{pass_str} psql -h {host} -U {user} -p {port} {dbname} {ERRFILE}\n'

    return base_cmd
