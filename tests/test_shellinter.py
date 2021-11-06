
""" A module to test the shellinter module """

import shellinter

import subprocess
from subprocess import PIPE
import unittest

class Test(unittest.TestCase):

    def setUp(self) -> None:
        """ Set up a processes for testing """

        self.psql_process = subprocess.Popen('/bin/bash',
                                             shell=True,
                                             stdin=PIPE,
                                             stdout=PIPE,
                                             stderr=PIPE,
                                             bufsize=10)

        self.mysql_process = subprocess.Popen('/bin/bash',
                                              shell=True,
                                              stdin=PIPE,
                                              stdout=PIPE,
                                              stderr=PIPE,
                                              bufsize=10)
        self.process_tests = [
            {
                'process' : self.psql_process,
                'test_quaries' : ['select datname from pg_database;\n'],
                'login' : 'psql -h localhost',
                'type' : 'psql',
            },
            {
                'process' : self.mysql_process,
                'test_quaries' : ['select DATABASE();\n'],
                'login' : 'mysql --login-path=local\n',
                'type' : 'mysql',
            },
        ]

        for process in self.process_tests:
                process['process'].stdin.write(process['login'])

    def test_get_stdout(self):
        """ Tests shellinter.get_stdout """

        # tests raised exceptions

        # local databases
        known_values = [
             # default mysql local databases
            '+------------+\n| DATABASE() |\n+------------+\n| NULL       |\n+------------+',
             # default postgresql local databases
            '  datname  \n-----------\n postgres\n template1\n template0\n(3 rows)\n',
        ]

        # test output
        for test_process, known in zip(self.process_tests, known_values):
            for process, quaries, _, type in test_process:
                state_output = shellinter.get_stdout(process, quaries, type, capture_output=True)
                self.assertEqual(state_output, known)
        
