"""
Tests the functionality of the Linux Platform support.

.. only:: development_administrator

    Module management
    
    Created on Jun. 22, 2020
    
    @author: Jonathan Gossage
"""

import os
import unittest

from linux.platform import *

import lib.configuration as _c


class Test(unittest.TestCase):

    def testName(self):
        """
This test is inherently dependent on the environment that it is run in. It gets
data from the Linux system file `/etc/passwd`. The data in the environment is
also sensitive to the identity of the user running the program. Some of the
data has no alternative source and must be hard coded. An example of this is
the user name variable.
        """

        #TODO: Develop support for accessing command line arguments to a test
        # so that hard coded data can be specified on the command line
        cfg = platformConfiguration()
        self.assertTrue(_c.userid in cfg) and\
            self.assertEqual(cfg[_c.userid],
                             os.environ['USER'])
        self.assertTrue(_c.uid in cfg) and self.assertEqual(cfg[_c.uid],
                                                            os.getuid())
        self.assertTrue(_c.gid in cfg) and self.assertEqual(cfg[_c.gid],
                                                            os.getgid())
        uname = 'Jonathan Gossage'
        tname = ''
        if _c.username in cfg:
            tname = cfg[_c.username]
            self.assertEqual(tname,
                             uname,
                             'The value of the user name has been hardcoded'
                             ' and probably needs to be changed')
        else:
            self.fail('No user name found in the configuration')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
