"""
Unit test driver for the application startup template

Created on Jul. 6, 2020

@author: Jonathan Gossage
"""

import os
import sys
import unittest

print(f'Current CWD is: {os.getcwd()}')
sys.path.insert(0, '/home/jgossage/GlobalVillage/EclipseWorkspaces/Library')
sys.path.insert(1, '/home/jgossage/GlobalVillage/EclipseWorkspaces/StartupApp/templates')
print(f'PYTHONPATH is {sys.path}')
from pydev import gv_start_ide as ide


class Test(unittest.TestCase):


    def testName(self):
        ide.main()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    