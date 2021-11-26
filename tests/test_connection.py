
""" Unittests for connection.py """

from dbmanage.connection import PostgresConnection, MysqlConnection

import os
import getpass
from subprocess import Popen

import unittest
from tests.test_utils import TESTDATADIR, get_pass

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

        testcases = {

            # postgresql testcases
            'postgres' : [
            {
                # expected output
                'output' : {
                    'column' : ['id', 'name', 'age'],
                    'type' : ['integer', 'text', 'integer'],
                    'collation' : [None, None, None],
                    'nullable' : ['not null', 'not null', None],
                    'default' : ["nextval('test_id_seq'::regclass)", None, None],
                    'extra' : ['Indexes:', '"test_pkey" PRIMARY KEY, btree (id)'],
                },
                # get extra lines
                'extra' : True,
                # file to read
                'filepath' : os.path.join(TESTDATADIR, 'read_table_info_psql.txt')
            },
            {
                # expected output
                'output' : {
                    'id' : ['0', '1', '2'],
                    'name' : ['yiannis', 'natalia', 'friedrich neitzche'],
                    'age' : ['19', '20', '33'],
                },
                # get extra lines
                'extra' : False,
                # file to read
                'filepath' : os.path.join(TESTDATADIR, 'tabledata_psql.txt'),
            },
            ],

            # mysql testcases
            'mysql' : [
            {
                # expected output
                'output' : {
                    'field' : ['id', 'name', 'age'],
                    'type' : ['int', 'text', 'int'],
                    'null' : ['no', 'no', 'yes'],
                    'key' : ['pri', None, None],
                    'default' : ['null', 'null', 'null'],
                    'extra' : ['auto_increment', None, None],
                },
                # get extra lines
                'extra' : True,
                # file to read
                'filepath' : os.path.join(TESTDATADIR, 'read_table_info_mysql.txt')
            },
            {
                # expected output
                'output' : {
                    'id' : ['1', '2', '3'],
                    'name' : ['yiannis', 'natali', 'friedrich neitzche'],
                    'age' : ['19', '20', '33'],
                },
                # get extra lines
                'extra' : False,
                # file to read
                'filepath' : os.path.join(TESTDATADIR, 'tabledata_mysql.txt')
            },
            ],
        }

        # run tests
        failingpath = 'fail/file'

        # postgresql tests
        for test in testcases['postgres']:

            with self.assertRaises(FileNotFoundError):
                self.postgresConnection._readStdout(failingpath)

            result = self.postgresConnection._readStdout(test['filepath'], extra=test['extra'])
            self.assertEqual(test['output'], result)

        # mysql test
        for test in testcases['mysql']:

            with self.assertRaises(FileNotFoundError):
                self.mysqlConnection._readStdout(failingpath)

            result = self.mysqlConnection._readStdout(test['filepath'], extra=test['extra'])
            self.assertEqual(test['output'], result)

    def test_kill(self) -> None:
        """ Tests Connection.kill """

        self.postgresConnection.kill()
        self.assertEqual(self.postgresConnection.terminated, True)
        self.assertEqual(self.postgresConnection._connection.returncode, 0)

        self.mysqlConnection.kill()
        self.assertEqual(self.mysqlConnection.terminated, True)
        self.assertEqual(self.mysqlConnection._connection.returncode, 0)
