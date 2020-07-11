"""
*Linux* platform specific support for capturing environmental information

This is an operating system dependent module. It will be deployed in an
operating system dependent package that has the same name as is returned
by platform.system(). One such module exists for every platform supported by
this framework.

It contains functions that are platform specific. Every platform specific
package contains identically named functions. This allows the module to be
imported like this:
    `from linux import *`
When this function succeeds, all the platform specific functions will have been
imported and can be used directly without needing to consider that they are
platform specific in their implementation.

.. only:: development_administrator

    Module management
    
    Created on Apr. 18, 2020
    
    @author: Jonathan Gossage
"""
import os
from pathlib import Path
from getpass import getuser
import re
from typing import MutableMapping, Any

__ALL__ = []


class configCode():
    """
    The class name will be identical in all configuration data files. This
    supports a generic configuration environment that can easily be implemented
    at any specific location, as required.

    There is a set of methods, each of which retrieves a piece of information
    in a platform specific manner and adds it to the list of platform sensitive
    configuration data. The methods will have a common format to their names.
    They will all take the form platformXyz. This means that adding a new
    platform sensitive entry is as simple as adding the appropriate method to
    the source for this module. This will be done manually since the methods of
    acquiring platform specific data are variable and are not automatable
    across platforms.
    """

    import lib.configuration as _c
    _C = _c.Configuration
    import lib.gvLogging as _l
    _L = _l.Logging
    admin_data: configCode._c.CfgAdmin

    def __init__(self) -> None:
        self._cfgSource: MutableMapping[str, configCode._c.CfgEntry] = {}
        self.errors = 0
        pass

    def __call__(self) -> None:
        for m in __dict__:
            if m.__name__.contains('platform'):
                m()     # Run the method to add a platform sensitive
                        # configuration variable.

    def shutdown(self) -> int:
        configCode._C.add(self._cfgSource)      # add the platform specific
                                                # variables to the
                                                # configuration.
        return self.errors

    def platformA(self):
        """
        Even though Python provides a platform neutral way of retrieving this
        information, it is handled here because the source of the information
        is the underlying platform. The method has a funny name to ensure that
        it is recognized first if the method list is sorted. 
        """
        uname = getuser()
        admin_data = configCode._c.CfgAdmin(uname,
                                 override=False)
        self.cfgSource[configCode._c.userid] =\
            configCode._c.CfgEntry(configCode._c.userid,
                                   uname,
                                   admin=admin_data)

    def platformUserData(self):
        """
        This method can extract three data items from an entry in the password
        data file. These are the userid, the primary group id and the full user
        name of the current user.
        """

        reflags = re.VERBOSE | re.MULTILINE
        # The pattern will be used to search the contents of the Linux password
        # file for a record matching the current system user. Each line of the
        # file is also a logical record that contains 7 fields, each delimited
        # by a : character. The record contains the data for a single user,
        # Scanning of each logical record starts at the beginning of the line.
        pattern = r"""
^%s:                      # The userid - %s in the pattern becomes the
                          # discovered userid of the user running this program.
                          # The field is delimited  by a colon.
[^:](?!:)*:               # The password - accepts any character until a
                          # colon is encountered.
(\d{1,5}):                # The UID should have from 1-5 digits followed by
                          # a colon.
(\d{1,5}):                # The GID should have from 1-5 digits followed by
                          # a colon.
([\w (?! )]+):|\,{1,3}:   # The user name - must be alphanumeric with several
                          # instances of a single embedded space, followed by
                          # a colon or 1-3 commas followed by a colon.
""" % self.cfgSource[configCode._c.userid]
        # Read the password file
        text = ''
        with Path('/etc/passwd') as f:
            text = f.read_text()
        match = re.search(pattern,
                          text,
                          reflags)
        grp = ()
        if match:
            cfg_keys = ('', '', '', '_c_uid', '_c_gid', '_c_username')
            grp = match.groups()
            """
            This loop contains a little bit of black magic.
            The `grp` variable contains the matched groups found by the regular
            expression. They will have the following order as defined in the
            regular expression:
            * full string text
            * userid
            * password
            * uid
            * gid
            * full user name
            
            The variable `cfg_keys` contains the the keys that should be used
            in the configuration dictionary. The first three names are empty
            because we are ignoring the first 3 groups found.
            We loop through the groups, skipping the first three, to get the
            values that we need for the corresponding configuration dictionary
            entries
            """
            for i, g in enumerate(grp,
                                  start=3):
                if g is None:
                    configCode._L.warning(f'{cfg_keys[i]} is None,'
                                          ' unexpected value')
                    self.errors += 1
                else:
                    self.cfgSource[cfg_keys[i]] =\
                        configCode._c.CfgEntry(cfg_keys[i],
                                               g,
                                               configCode.admin_data)
        else:
            configCode._L.warning(f'unable to recognize an entry for'
                                  f' {self.cfgSource[cfg_keys[i]]}'
                                  ' in the Linux password file')
            self.errors += 1
    
        # These variables will not be needed anymore and they take space
        del(reflags)
        del(pattern)
        del(text)
        del(match)
        del(grp)

        """
Note on conversion of this function to asynchronous mode

Although this function is logically a small part of the total picture of
creating the environment for an application invocation, it is highly CPU
intensive because it loads the entire password file and uses regular
expressions to examine the content of the file. It will also serve as a useful
tool for me in learning how to properly use asynchronous processing.

The file is made up of records, one for each user recorded in the file and a
record is contained in a physical line.

Record processing has two stages. In the first stage, we determine if this is a
record of interest. In the second stage, we process the record. This second
level processing takes place only when we have identified that a record is of
interest.

This suggests that we should get overlap in our processing in the following
way:

* Read records asynchronously, line by line.
* As a line becomes available, pass it to a pool of processors running in a
  pool as multiprocessing tasks.
* Since each pool member runs asynchronously on a  separate processor core, we
  can get strong overlap because the first stage of record processing, for each
  record, can run overlapping the time for reading records and the time for
  processing each record. For example, on a 8 thread processor we can run 7
  record identification processes simultaneously in parallel while reading the
  records for the file.at the same time. When a record is found that is
  interesting it can be sent to another processor for analyzing.
* The net effect is that almost all processing of the password file can be
  overlapped with the reading of the file, considerably reducing the elapsed
  time to handle the file.
* This method can be generalized and applied to any situation where data comes
  in definable chunks from asynchronous sources and must be processed, a very
  common situation.
        """

    def platformComputerName(self):
        self.cfgSource[configCode._c.computer_name] = os.uname().nodename
