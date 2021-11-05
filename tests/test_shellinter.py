
""" A module to test the shellinter module """

from shellinter import readFromBufferedReader

import subprocess
from subprocess import PIPE
import unittest

class Test(unittest.TestCase):

    def setUp(self):
        """ Set up a process for testing """

        self.process = subprocess.Popen('/bin/bash',
                                        shell=True,
                                        stdin=PIPE,
                                        stdout=PIPE,
                                        stderr=PIPE,
                                        bufsize=10)

    def _process_write(self, num: int) -> None:
        """ Helper function for filling stdout """

        for i in range(int):
            self.process.sdout.write('echo "test"\n')

    def test_readFromBufferedReader(self):
        """ Tests shellinter.readFromBufferedReader """

        # tests raised exceptions
        self.assertRaises(readFromBufferedReader, '')

        # test output type
