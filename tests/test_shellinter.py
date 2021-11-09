
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

        # Setup test_credentials.json if it doesn't exist
        creds_path = os.path.join(os.path.dirname(__file__), 'test_credentials.json')
        if not os.path.exists(creds_path):
            psql_pass = getpass.getpass('Enter PostgreSQL password to add to test_credentials.json: ')
            mysql_pass = getpass.getpass('Enter MySql password to add to test_credentials.json: ')

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

        for test_case in self.test_cases:

            fail = False
            if test_case['host'] == 'fail_test':
                fail = True

            # checks to do for with non failing connections
            if not fail:
                connection = shellinter.connect(**test_case)

                # check return type
                self.assertEqual(Popen, type(connection))

                # test that returned process has properly logged in
                out_commands = {
                    # commands to print some output on a temp file that is going to be checked
                    'mysql' : r'\T temp\nshow databases;\n\q\n',
                    'psql' : r'\o temp\nselect datname from pg_database;\n\q\n',
                }

                with open('temp', 'r', encoding='utf-8') as f:
                    out_str = ''.join(line for line in f.readlines())

                # TODO: add equal assertion and file removal
                expected_out_str = {
                    'psql' : rf'  datname  \n-----------\n postgres\n template1\n template0\n {getpass.getuser()}\n(4 rows)\n\n',
                    'mysql': rf"""mmysql> show databases;\n+--------------------+\n| Database           |\n+--------------------+\n| information_schema |\n| mysql
                                  |\n| performance_schema |\n| sys                |\n+--------------------+\n4 rows in set (0.01 sec)\n\nmysql> \\q\n""",
                }

            else:
            # check raised expections
            #TODO: add warnings for missing kwargs
            #TODO: add stderr based expection raising
                pass
