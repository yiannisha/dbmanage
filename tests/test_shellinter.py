
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
            'user' : f'{getpass.getuser()}', # default postgres username is user
            'dbname' : 'postgres',
            'pass' : '',
             },

            #  postgresql failing test case
            {
            'host' : 'fail_test',
            'port' : '5432', # default postgres port
            'user' : f'{getpass.getuser()}', # default postgres username is user
            'dbname' : 'postgres',
            'pass' : '',
            },

            #  mysql test case
            {
            'host' : 'localhost',
            'port' : '3306', # default mysql port
            'user' : 'root', # default mysql username is root
            'dbname' : 'mysql',
            'pass' : f'{test_utils.get_pass("MYSQL_PASS")}',
            },

            #  mysql failing test case
            {
            'host' : 'fail_test',
            'port' : '', # default mysql port
            'user' : 'root', # default mysql username is root
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
                dbname = test_case['dbname']
                connection = shellinter.connect(dbname, **test_case)

                # check return type
                self.assertEqual(Popen, type(connection))

                # test that returned process has properly logged in
                temp_filename = 'temp'
                out_commands = {
                    # commands to print some output on a temp file that is going to be checked
                    'mysql' : bytes(f'\T {temp_filename}\nshow databases;\n\q\n', 'utf-8'),
                    'postgres' : bytes(f'\o {temp_filename}\nselect datname from pg_database;\n\q\n', 'utf-8'),
                }

                # execute out_command with connection and then kill process
                connection.stdin.write(out_commands[dbname]) # type: ignore
                stdout, stderr = connection.communicate()

                # wait for file to be generated
                print(f'Waiting for {temp_filename} file...')
                try:
                    while(not os.path.exists(temp_filename)):
                        pass
                except KeyboardInterrupt:
                    # print process stdout and stderr if no temp file is generated
                    print('Process stdout: ', stdout)
                    print('Process stderr: ', stderr)

                with open(temp_filename, 'r', encoding='utf-8') as f:
                    out_str = ''.join(line for line in f.readlines())

                #print('Output string from file:\n', out_str)

                # delete file
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)

                expected_out_str = {
                    'postgres' : f'  datname  \n-----------\n postgres\n template1\n template0\n {getpass.getuser()}\n(4 rows)\n\n',
                    #'mysql': f"""mysql> show databases;\n+--------------------+\n| Database           |\n+--------------------+\n| information_schema |\n| mysql
                    #              |\n| performance_schema |\n| sys                |\n+--------------------+\n4 rows in set (0.01 sec)\n\nmysql> \\q\n""",
                    'mysql' : 'Database\ninformation_schema\nmysql\nperformance_schema\nsys\n',
                }

                # check output saved to temp file
                self.assertEqual(expected_out_str[dbname], out_str)

            else:
            # check raised expections
            #TODO: add warnings for missing kwargs
            #TODO: add stderr based expection raising
                pass
