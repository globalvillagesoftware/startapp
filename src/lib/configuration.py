"""
Created on Apr. 19, 2020

@author: Jonathan Gossage

Manage the application configuration for an application.

This class is only partially implemented, allows the whole startup
infrastructure to be tested. It is intended that constructing the configuration
for an application will provide it with all the information needed to run. This
information can come from a variety of sources. The default implementation will
provide three sources but the software will allow any number of sources to be
defined. The sources are considered to be hierarchical so configuration elements
at a lower level will override the same elements from a higher level.
Configuration data will be persisted in
`JSON <https://www.json.org/json-en.html>`_ files which match exactly in
structure with the dictionary structure used internally to hold configuration
data.

External configuration is stored in JSON files and is loaded into the computer
as a dictionary that contains the configuration data for the application. Third
party configuration modules must be capable of translating their information
into a JSOM compatible dictionary. Each source is responsible for the
maintenance of it's configuration data through a graphical program that has not
yet been developed.

Much of this data is stored in configuration files that are located via a
configuration index file that contains entries for the address of each
application. Configuration element names are grouped into functional groups that
work together. Groups may not be implemented in the initial configuration
module. The following groups are supported by this configuration and should be
supported by the user's interface module to any third party configuration
system:

* user |br| 
  This group contains personal information related to a specific user.
  Ultimately this information is supplied by the user or by the Human Resources
  department of am organization. This group is mandatory as it allows the
  tracking of problems related to the application.
  A user entry may specify one or more roles that a user fulfills in an
  organization.
* user roles |br| 
  These roles define what the user does within an organization. In many cases
  they actually define job titles. Roles are implemented as groups in their own
  right and provide a description of how the role elated to 

  * developer |br|
      This group contains a list of information related to the original
      developer(s) of this application. It may contain a list of links to
      group(s) that define each developer involved in the creation of this
      application.
      the user. It contains information relating to the original developer of
      the application. It is used for problem tracking and is optional. It is
      only used when
    * team_developer|br| 
      This list of entries defines the team that developed
"""
#TODO: Complete documentation of the configuration process - Issue #1

import importlib

#import lib.version
#v = lib.version.Version

# Configuration item keys. These variables are for commonly used configuration
# elements. Others are organization or application specific and their keys will
# not appear here.

userid      = 'userid'
"""
*userid* is the operating system user identification of the user running the
program.
"""
username    = 'username'
""" *username* is the full name of the user running the program."""
debug       = 'debug'
"""
Run the program in `debugging <https://docs.python.org/3/library/debug.html>`_
mode in the Python interactive console or in other consoles such as
`Idle <https://docs.python.org/3/library/idle.html>`_ that support Python
debugging.
"""
testrun     = 'testrun'
"""
Run the program in `doctest <https://docs.python.org/3/library/doctest.html>`_
mode.
"""
profile     = 'profile'
"""
`Profile <https://docs.python.org/3/library/debug.html>`_ the python program.
"""
version     = 'version'
"""
Abbreviated program version. Global Village uses and supports
`semantic versioning <https://semver.org/>`_
"""
release     = 'release'
"""
`Full <https://semver.org/>`_ program version.
"""
datecr      = 'datecr'
"""Date program was created."""
dateup      = 'dateup'
"""Date program was last updated."""
verbose     = 'verbose'
"""
Run program in verbose mode. This item can have values that range from 0-3
which control how verbose the program is, i.e. how much debugging data is
provided. 0 is the most terse.
"""
pname     = 'pname'
"""The name of the program, as seen by the operating system"""

plid      = 'plid'
"""
Name of the operating system platform that is running.
"""
ppath       = 'ppath'
"""
Path to the directory that contains the platform specific modules for this
application.
"""
commandargs = 'commandargs'
"""
A list of the arguments passed from the command line when the application is
invoked. This is used in situations where the command line is emulated.
"""
umname      = 'umname'
"""Name of the application specific high-level module."""
umpkg       = 'umpkg'
"""Name of the package that contains the application module."""
umclass     = 'umclass'
"""Name of the class that contains the high-level application specific code"""
log         = 'log'
"""
The log to use throughout the application. This is a Python type.
"""
uac         = 'uac'
"""The name of the applicaion specific mainline function for this application"""
cmdargs     = 'cmdargs'
"""
A list of arguments to be used in place of the command line. Mainly used for
debugging with tooks like `unittest`."""
cmdfile      = 'cmdfile'
"""
The path to the file that is to be used for the configuration of this
application for aspecific run.
"""
noupdate     = 'noupdate'
"""
Flag that supresses the update of a configuration value
"""
nologging    = 'nologging'
"""
Flag that suppresses the use of the logging facility, leaving only the ability
to write messages to stderr.
"""
noargs       = 'noargs'
"""
Flag that suppresses the use of command line arguments
"""
noconfig     = 'noconfig'
"""
Flag that suppresses the use of configuration files leaving only the
configuration supplied by the Global Village
"""
logsys       = None
"""
The name of the module that invokes or supplies a third party logging system
This module should be callable. We make use of the initialization and call
methods from this module.
"""
argsys       = None
"""
The name of the module that invokes or supplies a third party command line
argument processing system.
"""
class ArgDescriptor(object):
    def __init__(self):
        return

#TODO: Update configuration.py with key names from cfg.data

class CfgEntry(object):
    """
    Encapsulates the key and value components of a dictionary entry.
    """

#TODO: Expand definition to include variable definition for Arguments
#TODO: Make a class entry for CfgEntry be the element of the configuration
    def __init__(self, cfg, key, value, ad=None, admin=None):
        """
        :param dict cfg          The configuration dictionary
        :param str key:          The key for the dictionary entry
        :param Any value:        The value for the dictionary entry
        :param ArgDescriptor ad: The argparse definition
        :param Any admin:        Administrative data for this entry
        """

        self._key   = key
        self._value = value
        self._ad    = ad
        self._admin = admin

        if not cfg[noconfig]:
            self._cj = importlib.import_module('commentjson')
            self._a = importlib.__import__('lib.parse_arguments',
                                           fromlist=('Arguments'))

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key ):
        self._key = key

    @property
    def value(self):
        return self._value   

    @value.setter
    def value(self, v ):
        self._value = v 


class Configuration(object):
    """
    classdocs
    """

    def __init__(self, cfg):
        """
        :param dict cfg: The configuration directory
        :returns: the full configuration data including command line arguments
        :rtype: dict
        """

        self._cfg            = cfg
        self._cfg[debug]     = False
        self._cfg[testrun]   = False
        self._cfg[profile]   = False
        self._cfg[noupdate]  = False
        self._cfg[nologging] = False
        self._cfg[noargs]    = False
        self._cfg[noconfig]  = False
# Assume that arguments will be obtained from the command line via sys.argv
        self._cfg[cmdargs]   = None
# Assume that an empty configuration file will be used. The actual file to be
# used can be specified by the cfgfile argument on the command line or may be
# set by our caller who might be a debgugging system like unittest.
        self._cfg[cmdfile]   = None
        #TODO: Repair the importation of the version module so it can be used
#        self._cfg[version]  = CfgEntry( version, v( 0, 1 ))
        self._cfg[verbose]   = 0
        self._cfg[uac]       = None
        # Load up and merge the configuration file for this run
        # It cannot be done earlier because its' location may be specified on
        # the command line
        #TODO: Invoke the loading of the configuration files
        
        # Setup the argument parsing libraty
        
        if not self._cfg.get(noargs):
            self._a = importlib.__import__('lib.parse_arguments',
                                           fromlist=('Arguments'))
            print(f'Arguments type: {type(self._a.Arguments)}')
            print(f'Arguments: {dir(self._a.Arguments)}')
            self._cfg.update(self._a.Arguments.Parse())
        
        # If the user does not want configuration - go no further
        if self._cfg[noconfig]:
            return

        # Now the configuration file can be loaded and merged into the
        # configuration.
        #TODO: Get user data correctly. Possibly use configuration file
#TODO: Get access to configuration data file.

#TODO: Complete sample configuration data file, cfg.data

    def set_member(self, member):
        self._cfg[member.key] = member.value

    def add(self, entry):
        if self._cfg.get(entry.key()) is not None:
            raise(KeyError, '{} is already in configuration - cannot add'.\
                  format(entry.key()))
        self._cfg[entry.key()] = entry.value()

    def delete(self, entry):
        if isinstance( entry, CfgEntry ):
            if entry.key() in self._cfg:  # Got an entry object
                raise(KeyError,
                      f'{entry.key} is not in configuration - cannot delete')
            else:
                    del self._cfg[entry.key]
        else:  # Got a text key
            if entry.key() in self._cfg:
                raise(KeyError,
                      f'{entry} is not in configuration - cannot delete')
            else:
                del self._cfg[entry]
                
    def insert(self, key, value):
        self._cfg.update(key, value)
        
    def get(self, key):
        return(self._cfg.get(key))
    
    def len(self):
        return len(self._cfg)
    
    def _loadConfig(self, cfg):
        """
        Load the configuration data from disk
        
        :param List[str] cfg: A list containing the paths of the configuration
                              data files to be loaded. 
        :returns:            Nothing. Everything is done as side-effects.
        """

        final_file = {}  # The consolidated comfiguration data
        for file in cfg:
            with open(file, 'r') as f:
                temp_file = self._cj.load(f)
                for ent in temp_file:  # Check for existing keys
                    #TODO: Handle updating of existing keys
#                    if not ent.key() in self._cfg or ent.key() in final_file:
                    final_file.update(ent)
        self._cfg.update(final_file)
        return

    def __call__(self):
        """
        The configuration file resides in a platform specific location and can
        reside in a different place for testing so that test versions of the
        file can be used. When testing, the name of the configuration file
        is passed as an argument to main(). For testing, the name of the testing
        file can be specified on the command line when the test is invoked.
        """
#TODO: Load configuration data from file

        # Return standard configuration augmented by the command line arguments
        return self._cfg
