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
import platform

from pathlib import Path
from typing import Callable, Dict, Optional

# This assumes we want the configuration process. We default to wanting it
# since the use of mock objects for configuration during testing can give us
# control over the environment
import lib.configuration as _c  # Defines c as an abbreviation for
                                # lib.configuration
import lib.gvLogging as _l


cfg: Dict[str, _c.CfgEntry] = {}        # The application configuration data

# Initialize gvLogging
_L = _l.Logging(cfg)

# The module level code in the configuration module was run during import
# Initialize the Configuration class. This will acquire disk file or remote
# site based configuration files, as well as the command line arguments if
# desired.
_C = _c.Configuration(cfg)
# Record the logging state in the configuration
_C.set_member(_c.log,
              _L)

# Load the platform specific module
_platform: Optional[str] = platform.system()
_platform_module_name = 'platform.py'
_platform_module_path = Path(sys.argv[0]).resolve()
_platform_module_path = Path(_platform_module_path.parent / _platform)
err = 0
if _platform is None:

    _L.error('We are running on a strange system.'
             f' {sys.argv[0]} does not understand the name'
             ' of the operating system')
    sys.exit(1)

if not _platform_module_path.exists():
    _L.error('Global Village does not support the'
             f' operating system platform {_platform_module_path}')
    exit(1)
try:
    importlib.import_module(f'lib.{_platform}.platform')
except ImportError as e:
    _L.exception(f'Python cannot import {e}')
    sys.exit(1)


_tf  = None     # Name of the configuration file to use for testing
_ret = 0        # Default return code

"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Normally, the program name will be the value passed on the command line in
sys.argv[0], but in some circumstances, such as running in a debugger or
testing framework, this name may not be available. The default name is set here
in the configuration using the configuration key pname. Change this name to
suit the application.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""
_C.set_member(_c.pname,
              'startupapp')

__all__ = ['lib.configuration.Configuration']


__sources__ = {}
"""
>>> The sources where configuration information can be obtained. <<<

Each dictionary element can be an instance of the class configLoader that can
load configuration data for a specific group within an organization. It can
also be a dictionary of sources that are considered to be lower in the
organization hierarchy.

The key of each element should be the name of the organization group. The top
level entry in a hierarchy can use the organization name as a key.

The value for each configuration item is a tuple. The first member of the
tuple is the actual value of the configuration item. The second is a set of
flags that are mostly organization specific and are intended to define how the
configuration item can be used. These include a global flag that controls
whether lower level groups within an organization hierarchy can override the
value of the specific configuration item. If the value is a dictionary then it
contains a set of lower level organization definitions.

This dictionary is originally empty so no sources for configuration data are
supported.
"""


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
        sa: str = cfg.get(_c.pname)
        if sa is None:
            sa = 'StartupApp template'
        p: str = sys.platform()
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
        if um and upk and upc:
            # from upk import um.uc as _uac
            _uac = importlib.import_module(um,
                                           upk).upc

        # Stage 2 - Initialize gvLogging. Happens even if gvLogging not desired

        _C.set_member(cfg.log,
                       __import__('lib.gvLogging',
                                  fromlist=('Logging')))
        _C.get(_c.log)()  # Initialize the gvLogging

        # Gives the program name
        _C.set_member(_c.pname,
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
        if cfg.get(_c.debug) or cfg.get(_c.testrun):
            raise(e)
        else:
            sys.exit(2)


# Note that this code runs before the start of the main-line.
if __name__ == '__main__':
    if cfg.get(cfg.debug):
        sys.argv.append('-vvv')

    if cfg.get(cfg.testrun):
        import doctest
        doctest.testmod()

    if cfg.get(cfg.profile):
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
