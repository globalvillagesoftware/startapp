"""
Unit test driver for the application startup template

Created on Jul. 6, 2020

@author: Jonathan Gossage
"""

import sys
import unittest

# Setup the PYTHONPATH for this run
sys.path.insert(0,
                '/home/jgossage/GlobalVillage/EclipseWorkspaces/Library')
sys.path.insert(1,
                '/home/jgossage/GlobalVillage/EclipseWorkspaces/'
                'StartupApp/templates')
sys.path.insert(2,
                '/home/jgossage/GlobalVillage/EclipseWorkspaces/StartupApp')
from pydev import gv_start_ide as ide


class Test(unittest.TestCase):


    def testName(self):
        ide.main()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    