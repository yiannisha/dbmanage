
""" Unittests for connection.py """

from dbmanage.connection import PostgresConnection, MysqlConnection

import os
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

    def test_readStdout(self) -> None:
        """ Tests Connection._readStdout """

        expected_output = {
            'postgres' : {
                'column' : ['id', 'name', 'age'],
                'type' : ['integer', 'text', 'integer'],
                'collation' : [None, None, None],
                'nullable' : ['not null', 'not null', None],
                'default' : ["nextval('test_id_seq'::regclass)", None, None],
                'extra' : ['Indexes:', '"test_pkey" PRIMARY KEY, btree (id)'],
            },

            'mysql' : {},
        }

        # postgres test
        with self.assertRaises(FileNotFoundError):
            self.postgresConnection._readStdout('fail/file')

        testfile = os.path.join('tests', 'testdata', 'read_table_info_psql.txt')
        result = self.postgresConnection._readStdout(testfile)
        self.assertEqual(expected_output['postgres'], result)

        # mysql test

    def test_kill(self) -> None:
        """ Tests Connection.kill """

        self.postgresConnection.kill()
        self.assertEqual(self.postgresConnection.terminated, True)
        self.assertEqual(self.postgresConnection._connection.returncode, 0)

        self.mysqlConnection.kill()
        self.assertEqual(self.mysqlConnection.terminated, True)
        self.assertEqual(self.mysqlConnection._connection.returncode, 0)
