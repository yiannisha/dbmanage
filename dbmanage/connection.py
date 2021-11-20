
""" A module for the Connection Classes """

from dbmanage import shellinter

import subprocess

from typing import Union, List

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


class MysqlConnection(PostgresConnection):
    """ Class that handles interaction between user and MySQL database server """

    dbtype = 'mysql'
