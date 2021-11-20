
""" Unittests for connection.py """

from dbmanage.connection import PostgresConnection, MysqlConnection

import getpass
from subprocess import Popen

import unittest
from tests.test_utils import get_pass

class Test(unittest.TestCase):

    def setUp(self) -> None:
        """ Initialize test connections """
        self.test_cases = {

            'postgres':  {
            'host' : 'localhost',
            'port' : '5432', # default postgres port
            'user' : f'{getpass.getuser()}', # default postgres username is user
            'dbname' : 'postgres',
            'passwd' : '',
            },

            'mysql':    {
            'host' : 'localhost',
            'port' : '3306', # default mysql port
            'user' : 'root', # default mysql username is root
            'dbname' : 'mysql',
            'passwd' : f'{get_pass("MYSQL_PASS")}',
            },
        }

        self.postgresConnection = PostgresConnection(**self.test_cases['postgres'])
        self.mysqlConnection = MysqlConnection(**self.test_cases['mysql'])

    def tearDown(self) -> None:
        """ Terminate remaining processes """

        self.test_kill()

    def test_kill(self) -> None:
        """ Tests Connection.kill """

        self.postgresConnection.kill()
        self.assertEqual(self.postgresConnection.terminated, True)
        self.assertEqual(self.postgresConnection._connection.returncode, 0)

        self.mysqlConnection.kill()
        self.assertEqual(self.mysqlConnection.terminated, True)
        self.assertEqual(self.mysqlConnection._connection.returncode, 0)
