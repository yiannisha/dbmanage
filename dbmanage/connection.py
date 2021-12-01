
""" A module for the Connection Classes """

from dbmanage import shellinter
from dbmanage import query_utils
from dbmanage.database import Database

import os
import re
import subprocess

from typing import Union, List, Dict

ColumnDict = Dict[str, List[str]]

class Connection():
    """
    Abstract Object to handle interaction between user and a database server.
    This class is to be used only for inheritance.
    """

    dbtype = ''

    def __init__(self, host: str, user: str, dbname: str = '', passwd: str = '',
                 port: Union[int, str] = 5432, **kwargs) -> None:
        """ Initialize connection with database server """

        self._connection = shellinter.connect(dbtype=self.dbtype, host=host, user=user, dbname=dbname, passwd=passwd, port=port, **kwargs)
        self.terminated = False

        self.databases = self.get_databases()

    def kill(self) -> None:
        """ Terminates connection to server """
        self._connection.communicate()
        self.terminated = True

    def get_databases(self) -> List[Database]:
        """ Return a list of Database objects that represent the databases in the server """

        databases: List[Database]
        databases = []
        return databases

    def _readStdout(self, *args, **kwargs) -> ColumnDict:
        """
        Returns a dictionary with the columns of the output as dictionary keys
        and the values of each row as elements in a list as dictionary values
        """

        return query_utils._untabulate(query_utils._readrows(*args, **kwargs))

class PostgresConnection(Connection):
    """ Class that handles interaction between user and PostgreSQL database server """

    dbtype = 'postgres'

    def _untabulate(self, row_dict: Dict) -> ColumnDict:
        """
        Makes a postgresql specific correction to the dictionary returned from
        query_utils._untabulate. This function is to be used in Connection._readStdout
        instead of query_utils._untabulate
        """

        columnDict = query_utils._untabulate(row_dict)

        try:
            columnDict['extra'] = row_dict['extra']
        except KeyError:
            pass

        return columnDict

    def _readStdout(self, *args, **kwargs) -> ColumnDict:
        """
        Uses Connection._untabulate instead of query_utils._untabulate.
        Read Connection._untabulate documentation for more info.
        """

        return self._untabulate(query_utils._readrows(*args, **kwargs))

class MysqlConnection(Connection):
    """ Class that handles interaction between user and MySQL database server """

    dbtype = 'mysql'
