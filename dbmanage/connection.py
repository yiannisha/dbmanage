
""" A module for the Connection Classes """

from dbmanage import shellinter

import os
import re
import subprocess

from typing import Union, List, Dict

ColumnDict = Dict[str, List[str]]

class Connection():
    """ TODO: add documentation """

    dbtype = ''

    def __init__(self, host: str, user: str, dbname: str = '', passwd: str = '',
                 port: Union[int, str] = 5432, **kwargs) -> None:
        """ Initialize connection with database server """

        self._connection = shellinter.connect(dbtype=self.dbtype, host=host, user=user, dbname=dbname, passwd=passwd, port=port, **kwargs)
        self.terminated = False

        #self.databases = self.get_databases()

    def kill(self) -> None:
        """ Terminates connection to server """
        self._connection.communicate()
        self.terminated = True

    #def get_databases(self) -> List[Database]:
    #    """ Return a list of Database objects that represent the databases in the server """
    #    pass

    def _readStdout(self, *args, **kwargs) -> ColumnDict:
        """
        Returns a dictionary with the columns of the output as dictionary keys
        and the values of each row as elements in a list as dictionary values
        """

        return self._untabulate(self._readrows(*args, **kwargs))

    def _readrows(self, filepath: str, extra: bool = True) -> Dict:
        """
        Returns a dictionary with the "column", "row", "extra" as keys
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
            while not self._isrow(column_str):
                column_str = f.readline()
                if not column_str:
                    break

            # get values from rows
            f.readline() # skip line right after the line with column names
            line = f.readline() # first row
            while(self._isrow(line)):
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

    def _isrow(self, line: str) -> bool:
        """ Returns True if the line passed is a valid row of output """
        regex = '.*\|'
        return bool(re.search(regex, line))

    def _untabulate(self, row_dict: Dict) -> ColumnDict:
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

class PostgresConnection(Connection):
    """ Class that handles interaction between user and PostgreSQL database server """

    dbtype = 'postgres'

    def _untabulate(self, row_dict: Dict) -> ColumnDict:

        columnDict = super()._untabulate(row_dict)

        try:
            columnDict['extra'] = row_dict['extra']
        except KeyError:
            pass

        return columnDict

class MysqlConnection(Connection):
    """ Class that handles interaction between user and MySQL database server """

    dbtype = 'mysql'
