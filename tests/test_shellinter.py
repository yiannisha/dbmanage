
""" Unittests for shellinter.py """

from dbmanage import shellinter

import os
import getpass
import json
from subprocess import Popen

import unittest
from tests import test_utils



class Test(unittest.TestCase):

    def setUp(self) -> None:
        """ Sets up tests """

        # Setup credentials.json if it doesn't exist
        creds_path = os.path.join(os.path.dirname(__file__), 'credentials.json')
        if not os.path.exists(creds_path):
            psql_pass = getpass.getpass('Enter PostgreSQL password to add to credentials.json: ')
            mysql_pass = getpass.getpass('Enter MySql password to add to credentials.json: ')

            with open(creds_path, 'w', encoding='utf-8') as file:
                file.write(json.dumps({'PSQL_PASS': psql_pass, 'MYSQL_PASS': mysql_pass}))


        # Setup test cases
        self.test_cases = [
            #  postgresql test case
            {
            'host' : 'localhost',
            'port' : '5432', # default postgres port
            'user' : f'{getpass.getuser()}',
            'dbname' : 'postgres',
            'pass' : '',
             },

            #  postgresql failing test case
            {
            'host' : 'fail_test',
            'port' : '5432', # default postgres port
            'user' : f'{getpass.getuser()}',
            'dbname' : 'postgres',
            'pass' : '',
            },

            #  mysql test case
            {
            'host' : 'localhost',
            'port' : '3306', # default mysql port
            'user' : f'{getpass.getuser()}',
            'dbname' : 'mysql',
            'pass' : f'{test_utils.get_pass("MYSQL_PASS")}',
            },

            #  mysql failing test case
            {
            'host' : 'fail_test',
            'port' : '', # default mysql port
            'user' : f'{getpass.getuser()}',
            'dbname' : 'mysql',
            'pass' : '',
            }
        ]

    def test_connect(self) -> None:
        """ Tests shellinter.connect """

        # check return types
