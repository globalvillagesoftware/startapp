"""
Created on Apr. 30, 2020

@author: Jonathan Gossage

This script provides unit tests that validate the template
`global_village_start.py`. Part of the code in the template runs at module
 level. This code will be checked by importing the module that contains the
 template script.
"""

import importlib
import unittest
import sys

import lib.configuration as _c
from lib.configuration import Configuration as _C

template = 'pydev.gv_start_template'

def verifyModule(self):

    def verifyModule(self):
        cfg = self._tp.cfg # Get the actual configuration
        #TODO: startup_test - This test will run with simulated command line arguments and configuration files
        cfg[_c.noargs] = True
        _C.insert(cfg.cmdargs)
        
        # Now test the results from running the high-level code module-level
        # code. This actually ran in the setup function since the template was
        # imported there.
        self.assertTrue(isinstance(cfg, dict),
                        f'The configuration is not a dictionary - {type(cfg)}')
        l = _C(cfg).len()  # Number of entries in the configuration
        num = 8            # The expected number of entries in the configuration
        self.assertEqual(l, num,
            f'The configuration dictionary should have {num} item(s), has {l} '
             '\n    The entries are: {cfg}')
        #TODO: Cleanup and use the platform module to use this code
        """
        plid = cfg.plid  # The determined operating system
        plsys = 'linux'  # The expected operating system
        self.assertEqual(plid, plsys,
            'The configuration dictionary should say running on {} - is {}'.\
                         format(plid, plsys))
        """
        self.assertIsNone(cfg[_c.uac],
f'We should not have access to the user startup module yet - have {cfg[_c.uac]}')

def verifyFunction(self):
    num = 10         # The expected number of entries in the configuration
    l = _C(self._tp.cfg).len()  # Number of entries in the configuration
    self.assertEqual(l, num,
        f'The configuration dictionary should have {num} item(s), has {l} '
            '\n    The entries are: {cfg}')

def reload(template):
    if template in sys.modules:
        _tp = importlib.import_module(template)
    else:
        # Reloading the module gets rid of the old
        # copy of the template
        _tp = importlib.reload(template)
    return _tp


class TestModule(unittest.TestCase):

    def setup(self):
        """
        This will load the script module and will run the module level code
        without invoking the code in the main() module level function. The
        main() function will be invoked separately thus separating the testing
        of the two levels of code
        """
        self._tp = reload(template)

    def testModule(self):
        verifyModule(self)

@unittest.skip('Not fully implemented yet')
class TestFunction(unittest.TestCase):
    """
    The unittest driver for the `StartupApp` template
    This is a functional test that verifies that the StartupApp template does
    the right thing ad is usable as a template.
    """
    
    def setup(self):
        """
        This will load the script module and will run the module level code
        without invoking the code in the main() module level function. The
        main() function will be invoked separately thus separating the testing
        of the two levels of code.
        """

        self._tp = reload(template)

    def testFunction(self):

        verifyModule(self)
        
        # The next step is to run the main() function
        self._tp.main()

        # Run unit tests on the result of running the main startup function
        verifyFunction(self)

if __name__ == '__main__':
    unittest.main()