
""" A module to test the shellinter module """

from dbmanage import shellinter

import os
import subprocess
from subprocess import PIPE

import unittest
import tracemalloc

tracemalloc.start()

class TestProcessesNotProperlyCreated(Exception):
    """ An exception to be raised when test processes don't behave as they should """

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
                'login' : 'psql -h localhost\n',
                'logging_cmd' : (r'\out {}\n', r'\out\n'),
            },
            {
                'process' : self.mysql_process,
                'test_quaries' : ['select DATABASE();\n'],
                'login' : 'mysql --login-path=local\n',
                'logging_cmd' : ('pager cat | tee {}', 'notee\n'),
            },
        ]

    # DO NOT SKIP IT IS ESSENTIAL FOR SETUP
    def test_setUp(self):
        """ Tests for local Test.setUp """

        # test processes created
        for process in self.process_tests:
            # make test call
            process['process'].stdin.write(b'echo "test" > test_temp\n')

            while(not os.path.isfile('test_temp')):
                pass

            with open('test_temp', 'r', encoding='utf-8') as f:
                line = f.readline().strip()
                if line != 'test':
                    raise TestProcessesNotProperlyCreated(f'Wrote: {line} -> temp')
            # delete temp file
            if os.path.isfile('test_temp'):
                os.remove('test_temp')

        for process in self.process_tests:
                # print(bytes(process['login'], 'utf-8'))
                process['process'].stdin.write(bytes(process['login'], 'utf-8'))

    def tearDown(self):
        """ Closes all dependencies opened during the test """

        # kill remaining subprocesses
        for process in self.process_tests:

            pid = process['process'].pid
            subprocess.run(['kill', '-9', f'{pid}'])
            print('killed subprocesses')

        # tracemalloc debugging
        #snapshot = tracemalloc.take_snapshot()
        #top_stats = snapshot.statistics('lineno')
        #print('[Top 10]')
        #for stat in top_stats[:10]:
        #    print(stat)

    @unittest.skip
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
            process, quaries, _, logging_cmd = test_process.values()
            # this test simulates passing args from a higher level object to get_stdout
            output = shellinter.get_stdout(process, quaries, logging_cmd)
            self.assertEqual(output, known)
