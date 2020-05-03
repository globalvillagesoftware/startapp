"""
Created on Apr. 30, 2020

@author: Jonathan Gossage

This is the interface to the Python logging system. If a user wants, the logging
system will not be used and all output will be written to stderr. The
configuration of the logging system will be read from the configuration data and
setup in the Logging initializer. We make use of the Python logging system by
default but this can be overridden by the user if a different logging system is
desired.
"""

import importlib
import sys

#import lib.configuration as _c  # Defines c as an abbreviation for
                                # lib.configuration

class Logging(object):
    """
    This class is only minimally implemented at this stage. It simply
    provides the  writing of text to stderr.
    """
    
    def __init__(self, cfg):
        self._cfg = cfg
        self._c = importlib.import_module('lib.configuration')

        if self._c.cfg.get(self._c.nologging):
            #TODO: Provide the rest of the logging system initialization
                # The rest of the logging initialization. The big item is
                    # the definition of the loggers usd by a specific
                    # application
            pass

    def __call__(self, text=None, exc=None):
        """
        Does all the logging work
        
        :param str text:          Message text to be logged
        :param BaseException exc: Exception to be logged
        """

        # Identify program issuing message
        txt = None if text is None else f'{self._c.pname} - {text}'
        indent = len(self.cfg.pname) * ' '
        if self._cfg.get(self._c.nologging):
            # No logging system provided - use default
            if txt is not None:
                sys.stderr.write(f'{txt}\n')
            sys.stderr.flush()
            if exc is not None:
                if repr is None:
                    sys.stderr.write(f'{txt}')
                else:
                    sys.stderr.write(f'{txt}: {repr(exc)}\n')
                sys.stderr.write(
        f'{indent}  for help use the --help application command line flag\n')
            sys.stderr.flush()
            return 
        
        ls = self._c.cfg.get(self._c.logsys)
        if ls:  # We are using a third party logging system
            ls()  # Use it
            return
#TODO: Implement interface to the Python logging system
        return
            
