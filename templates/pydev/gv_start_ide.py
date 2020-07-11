#!/usr/bin/env python
# encoding: utf-8
"""
>>> The module short description. Change it appropriately. <<<

>>> The module description follows here. <<<

This is based on code written by Fabio Zadrozny as a template in the `Pydev`
plugin for Eclipse. It provides the basic code that you need to start and run
an application.

There are four main stages in the startup process:

* Get the configuration that the application will use.
* Initialize gvLogging.
* Run the application.
* Dispose of exceptions that happen during the running of the application.

This code can be used in two ways:

* It may be used as a module template by the `pydev` plugin for the Eclipse
  IDE. It will be automatically installed in `pydev` if `pydev` is detected by
  the `startupapp` installation procedure.
* It may be used manually as a template for the application agnostic portion of
  a user application high level module.

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
>>> Insert application specific documentation here. <<<
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

.. only:: development_administrator

    Module management
    
    ${module} -- ${shortdesc}
    
    ${module} is a ${description}
    
    
    @author:     ${user_name}
    
    @copyright:  © 2020 Global Village. All rights reserved.
    
    @license:    ${license}
    
    @contact:    ${user_email}
    @deffield    updated: Updated
"""

import sys
import os
import importlib
from typing import Callable, Optional

print(f'In start of template - {sys.path}')

import lib.configuration as _c
_C = _c.Configuration
import lib.gvLogging as _l
_L = _l.Logging
_l.setLogging()  # Setup the Global Village logger, if not already done



# The module level code in the configuration module was run during import
# Initialize the Configuration class. This will acquire disk files or remote
# site based configuration files, as well as the command line arguments if
# desired.
_C = _C()  # Initialize the local configuration
# Initializes the site logger if not already done and fully configures the
# Global Village logger if necessary.
# Record the logging state in the configuration
_L = _l.initializeLogging()
_C.setMember(_c.log,
             _L)


__ret = 0        # Default return code

"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Normally, the program name will be the value passed on the command line in
sys.argv[0], but in some circumstances, such as running in a debugger or
testing framework, this name may not be available. The default name is set here
in the configuration using the configuration key pname. Change this name to
suit the application.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""
_C.setMember(_c.pname,
             'startupapp')

__all__ = []


class gvError(Exception):
    """"Generic exception to raise and log different fatal errors."""
    def __init__(self, msg) -> None:
        super()
        self.msg = f'E: {msg}'

    def __str__(self) -> str:
        return self.msg

    def __unicode__(self) -> str:
        return self.msg


def main() -> int:
    """The application agnostic startup controller"""

    try:
        # Stage 1
        # Validate the configuration data
        # Validate that we are running on a supported platform
        plsys: Optional[str] = None
        sa: str = _C.get(_c.pname)
        if sa is None:
            sa = 'StartupApp template'
        p: str = sys.platform
        if p.startswith('win32'):
            raise(ValueError, f'{sa} - Windows is not supported yet')
        elif p.startswith('linux'):
            plsys = 'linux'
        else:
            # Platform is unsupported
            raise(ValueError, f'{sa} - {plsys} is an unsupported platform')

        # Load the user's application specific high level class
        um = _C.get(_c.umname)
        upk = _C.get(_c.umpkg)
        upc = _C.get(_c.umclass)
        _uac: Optional[Callable] = None
        if um and upk and upc:
            # from upk import um.uc as _uac
            _uac = importlib.import_module(um,
                                           upk).upc

        # Gives the program name
        _C.setMember(_c.pname,
                     os.path.basename(sys.argv[0]))

        # If we got a command line argument specifying the name of the config
        # file to use for the test run use it if dynamic configuration is not
        # suppressed.
        #TODO: Handle configuration file processing including the index

#       _tf = sys.argv[1] if len(sys.argv) > 1 else None

        # Stage 3 - Run the application
        # The first step imports the user's module
        # The second step creates an instance of the user's module
        # The third step invokes the user's module as a callable
        """
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
We invoke the application's startup method here that handles application
specific startup processing. Global Village programming conventions expect it
to be called `startup`. Change the method name if needed. `startupApp`
tolerates the lack of a startup method.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        """
        if _uac:
            if not isinstance(_uac,
                               Callable):
                raise(ValueError('The user application specific'
                                 ' class must be callable'))
            
            if 'startup' in _uac:
                _ret = _uac.startup()
                if _ret > 0:
                    raise(AssertionError('Application startup failed with'
                                         f' return code {_ret}'))
            else:
                """
Run the user's application. This loads the application specific code that
contains a callable class and invokes it. The Global Village environment
expects that the application specific class takes the configuration as
a parameter and that it contains a callable method that runs the application.
            """
            # The first step imports the user's module
            # The second step creates an instance of the user's module
            # The third step invokes the user's module as a callable
            _ret = max(_uac(),
                   _ret)
                
            if _ret > 0:
                raise(AssertionError('The application failed with return'
                                     f' code {_ret}'))
        else:
            raise ValueError(f'The application module {_uac} was not'
                             ' supplied in the configuration')


        # Stage 4 Application completed - Do application cleanup

        """"
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
We invoke the application's shutdown method here that handles application
specific shutdown. Global Village programming conventions expect it to be
called `shutdown`. Change the method name if needed. `startupApp` tolerates the
lack of a shutdown method.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        """
        if _uac and 'shutdown' in _uac:
            _ret = max(_uac.shutdown(),
                       _ret)
            if _ret > 0:
                raise(AssertionError('Application failed during shutdown with'
                                     f' return code {_ret}'))
        return _ret  # The application finished normally

    except KeyboardInterrupt:
        # handle keyboard interrupt
        return 0

    # This is the normal exception handler. It simply logs the exception
    except Exception as e:
        _L.exception('Got an exception: - ')
        if _C.get(_c.debug) or _C.get(_c.testrun):
            raise(e)
        else:
            sys.exit(2)


# Note that this code runs before the start of the main-line.
if __name__ == '__main__':
    if _C.get(_c.debug):
        sys.argv.append('-vvv')

    if _C.get(_c.testrun):
        import doctest
        doctest.testmod()

    if _C.get(_c.profile):
        import cProfile
        import pstats
        profile_filename = '${module}_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open('profile_stats.txt', 'wb')
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)

    # Run the application startup controller
    sys.exit(main())
