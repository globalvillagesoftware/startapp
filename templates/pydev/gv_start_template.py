#!/usr/local/bin/python3
# encoding: utf-8
"""
${module} -- ${shortdesc}

${module} is a ${description}


@author:     ${user_name}

@copyright:  © ${year} ${organization_name}. All rights reserved.

@license:    ${license}

@contact:    ${user_email}
@deffield    updated: Updated

This is based on code written by Fabio Zadrozny as a template in the `Pydev`
plugin for Eclipse. It provides the basic code that you need to start and run an
application.
 
There are four main stages in the startup process:
 
* Get the configuration that the application will use.
* Initilize logging.
* Run the application.
* Dispose of exceptions that happen during the running of the application.
 
This code can be used in two ways:
 
* It may be used as a module template by the `pydev` plugin for the Eclipse
  IDE. It will be automatically installed in `pydev` if `pydev` is detected by
  the `startupapp` installation procedure.
* It may be used manually as a template for the application agnostic portion of
  a user application high level module.

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Insert application specific documentation here.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

import sys
import os
import importlib

# This assumes we want the configuratio process. We default to wanting it
# since the use of mock objects for configuration during testing can give us
# control over the environment
import lib.configuration as _c  # Defines c as an abbreviation for
                                # lib.configuration
from lib.configuration import Configuration as _C
                                # Defines _C as an abbreviation for
                                # lib.configuration.Configuration
from lib.logging import Logging as _L

cfg = {}        # The application configuration data
_C(cfg)         # Initialize the Configuration class. This will acquire disk
                # based configuration files, as well as the command line
                # arguments if desired
_uac = None     # The module for the user's startup code
_tf  = None     # Name of the configuration file to use for testing
_ret = 0        # Default return code

"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Normally, the program name will be the value passed on the command line in
sys.argv[0], but in some circumstances, such as running in a debugger or testing
framework, this name may not be available. The default name is set here in the
configuration using the configuration key pname. Change this name to suit the
application.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""
_C.insert(_c.pname, 'startupapp')

__all__ = [cfg]

def main():
    """The application agnostic startup controller"""

    try:
        # Stage 1 - Get the application configuration

        # Validate that we are running on a supported platform
        plsys = None
        sa = cfg.get(_c.pname)
        if sa is None:
            sa = 'StartupApp template'
        p = sys.platform()
        if p.startswith('win32'):
            raise(ValueError, f'{sa} - Windows is not supported yet')
        elif p.startswith('linux'):
            plsys = 'linux'
        else:
            # Platform is unsupported
            raise(ValueError, f'{sa} - {plsys} is an unsupported platform')

        # Collect all the configuration data including the command line
        # arguments. This information is needed very early during program
        # execution so do it now.
        # Remember name of the operating system platform in the configuration
        _C.insert(_C.get(cfg.plid), plsys)
        # Load the user's application specific high level class
        um = _C.get(_c.umname)
        upk = _C.get( _c.umpkg)
        upc = _C.get(_c.umclass)
        if um and upk and upc:
            # from upk import um.uc as _uac
            _uac = importlib.import_module(um, upk).upc

        # Stage 2 - Initialize logging. Happens even if logging not desired

        _C.insert(cfg.log, __import__( 'lib.logging', fromlist=('Logging')))
        _C.get(_c.log)()  # Initialize the logging

        # Gives the program name
        _C.insert(_c.pname, os.path.basename(sys.argv[0]))
        
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
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
We invoke the application's startup method here that handles application
specific startup processing. Global Village programming conventions expect it to
be called `startup`. Change the method name if needed. `startupApp` tolerates
the lack of a startup method.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        """
        try:
            _ret = _uac.startup()
            if _ret > 0:
                return _ret
        except ImportError:     # It's OK if the application startup method is
                                # not there
            pass
        # all other exceptions are handled by the normal shutdown code

        """
Run the user's application. This loads the application specific code that
contains a callable class and invokes it. The Global Village environment
expects that the application specific class takes the configuration as
a parameter and that it contains a callable method that runs the application.
        """
        # The first step imports the user's module
        # The second step creates an instance of the user's module
        # The third step invokes the user's module as a callable
        _ret = _uac()
        if _ret > 0:
            return _ret

        # Stage 4 Application completed - Do application cleanup
        
        """"
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
We invoke the application's shutdown method here that handles application
specific shutdown. Global Village programming conventions expect it to be called
`shutdown`. Change the method name if needed. `startupApp` tolerates the lack
of a shutdown method.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        """
        try:
            _ret = _uac.shutdown()
        except ImportError: # It is OK if the application is not working
            pass
        # all other exceptions are handled by the normal shutdown code
        return _ret  # The application finished normally


    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0

    # This is the normal exception handler. It simply logs the exception
    except Exception as e:
        if _C.get(cfg.debug) or _C.get(cfg.testrun):
            raise(e)
        _C.log = e  # Log the error
        return 2

# Note that this code runs before the start of the mainline.
if __name__ == '__main__':
    c = cfg.get(cfg.debug)
    if c is not None and not c:
        sys.argv.append('-vvv')

    c = cfg.get(cfg.testrun)
    if c is not None and not c:
        import doctest
        doctest.testmod()

    c = cfg.get(cfg.profile)
    if c is not None and not c:
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
