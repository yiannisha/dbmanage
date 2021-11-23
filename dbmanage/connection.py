
""" A module for the Connection Classes """

from dbmanage import shellinter

import os
import re
import subprocess

from typing import Union, List, Dict

class PostgresConnection():
    """ Class that handles interaction between user and PostgreSQL database server """

    dbtype = 'postgres'

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

    def _readStdout(self, *args, **kwargs) -> Dict:
        """
        Returns a dictionary with the columns of the output as dictionary keys
        and the values of each row as elements in a list as dictionary values
        """

        initial_dict = self._readrows(*args, **kwargs)

        # TODO: format strings into the appropriate dictionary

        print('columns:', initial_dict['column'])
        print('rows', initial_dict['row'])
        print("Extra:", initial_dict['extra'])

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
            i=0
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
                extra_strs.append(line)
                extra_strs.extend([line.strip() for line in f.readlines()])

        return {
            'column' : column_str,
            'row' : row_strs,
            'extra' : extra_strs,
        }

    def _isrow(self, line: str) -> bool:
        """ Returns True if the line passed is a valid row of output """
        regex = '.*\|'
        return bool(re.search(regex, line))

class MysqlConnection(PostgresConnection):
    """ Class that handles interaction between user and MySQL database server """

    dbtype = 'mysql'
