
""" Unittests for shellinter.py """

from dbmanage import shellinter

import os
import getpass
import json
from subprocess import Popen

import unittest
from tests.test_utils import get_pass, read_temp_file



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
            'pass' : f'{get_pass("MYSQL_PASS")}',
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

                # read temp file
                out_str = read_temp_file(filename=temp_filename, stdout=stdout, stderr=stderr)

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

    @unittest.skip
    def test_write_queries(self) -> None:
        """ Tests shellinter.write_queries """

        temp_filename = 'test'
        test_db = 'dbmanage_testdb'
        QUERIES = { # type: ignore
            'postgre' : [
                f'DROP DATABASE IF EXISTS {test_db};\n',  # drop databases from previous tests
                f'CREATE DATABASE {test_db};\n',  # create a database
                f'\c {test_db}\n',  # connect to database

                # create a table
                """CREATE TABLE test(
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    age INTEGER,
                    gender TEXT
                );\n""",

                # add data to table
                """
                INSERT INTO test (name, age, gender)
                VALUES ('Yiannis', 19, 'male'),
                       ('Friedrich Nietzsche', 39, 'male'),
                       ('Nataly', 20, 'female');\n
                """,
                f'\o {temp_filename}\n',  # set up a file for stdout
                'SELECT * FROM test;\n',  # select data from table and output to file
                '\c postgres',  # connect to default database
                f'DROP DATABASE {test_db};\n',  # drop database from this test
            ],
            'mysql' : [
                f'DROP DATABASE IF EXISTS {test_db};\n',  # drop databases from previous tests
                f'CREATE DATABASE {test_db};\n',  # create a database
                fr'\r {test_db}\n',  # connect to database

                # create a table
                """CREATE TABLE test (
                    id INT AUTO_INCREMENT,
                    name TEXT NOT NULL,
                    age INT,
                    gender TEXT,
                    PRIMARY KEY (id))
                    ENGINE = InnoDB;\n
                    """,

                # add data to the table
                """
                INSERT INTO
                test (name, age, gender)
                VALUES
                ("Yiannis", 19, "male"),
                ("Friedrich Nietzsche", 39, "male"),
                ("Nataly", 20, "female");\n
                """,

                fr'\T {temp_filename}\n',  # set up a file for stdout
                'SELECT * FROM test;\n',  # select data from table and output to file
                'notee',  # disable outfile
                '\r mysql',  # connect to default database
                f'DROP DATABASE {test_db}\n',  # drop database from this test
            ],
        }

        EXPECTED_OUTPUT = { # type: ignore

            'postgre' : """ id |        name         | age | gender \n
            ----+---------------------+-----+--------\n
            1 | Yiannis             |  19 | male\n  2 | Friedrich Nietzsche |  39 | male\n
            3 | Nataly              |  20 | female\n(3 rows)\n\n""", # data that was added to table

            'mysql' : """mysql> SELECT * FROM test;\n+----+---------------------+------+--------+\n
            | id | name                | age  | gender |\n+----+---------------------+------+--------+\n
            |  1 | Yiannis             |   19 | male   |\n|  2 | Friedrich Nietzsche |   39 | male   |\n
            |  3 | Nataly              |   20 | female |\n+----+---------------------+------+--------+\n
            3 rows in set (0.00 sec)\n\nmysql> notee\n""", # data that was added to table
        }

        # create processes
        # if the tests have come this far it means that shellinter.connect works
        # properly so I can use it
        localTest_cases = [test for test in self.test_cases if test['host'] != 'fail_test']

        for test_case in localTest_cases:
            dbname = test_case['dbname']
            connection = shellinter.connect(dbname, **test_case)

        # test input to processes
            shellinter.write_queries(connection, QUERIES[dbname])

        # check process output from temp file
            stdout, stderr = connection.communicate()
            out_str = read_temp_file(temp_filename, stdout=stdout, stderr=stderr)

            self.assertEqual(EXPECTED_OUTPUT[dbname], out_str)
