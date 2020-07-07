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
from pathlib import Path
from getpass import getuser
import re
# from typing import MutableMapping, Any
from typing import MutableMapping, Any
import lib.configuration as _c
# from _c import Configuration as _C
import lib.configuration.Configuration as _C
import lib.gvLogging.Logging as _L

__ALL__ = ['platformConfiguration']


def platformConfiguration() -> MutableMapping:
    """
This function will generate a configuration dictionary containing entries whose
values are determined in a platform specific manner. The key will be the name
of the configuration entry and the value will be its value as discovered on the
specific platform.
    """

    # Set the current user
    cfg: dict[str: typing.Any] = {}
    cfg[_c.userid] = getuser()

    # Set the full name of the current user plus the UID and GID for the user
    reflags = re.VERBOSE | re.MULTILINE
    # The pattern will be used to search the contents of the Linux password
    # file for a record matching the current system user. Each line of the file
    # is also a logical record that contains 7 fields, each delimited by
    # a : character. The record contains the data for a single user, Scanning
    # of each logical record starts at the beginning of a line. Groups are
    # defined for the UID, GID, and the user name.
    pattern = r"""^%s:    # The userid - %s in the pattern becomes the
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
""" % (cfg[_c.userid], '%s')

    # Read the password file
    text = ''
    with Path('/etc/passwd') as f:
        text = f.read_text()
    match = re.search(pattern,
                      text,
                      reflags)
    grp = ()

    if match:
        cfg_keys = ('', '_c_uid', '_c_gid', '_c_username')
#        cfg_cvt = (None, int. int, str)
        grp = match.groups()
        for i, g in enumerate(grp,
                              start=1):
            if g is None:
                _L.warning(f'{cfg_keys[i]} is None, unexpected value')
            else:
                _C.set_member(cfg_keys[i],
                              g)
    else:
        _L.warning(f'unable to recognize an entry for {cfg[cfg_keys[i]]}'
                   f' for user {cfg[_c.userid]} in the Linux password file')

    # These variables will not be needed anymore and they take space
    del(reflags)
    del(pattern)
    del(text)
    del(match)
    del(grp)

    return cfg  # Return the data that we have captured


def get_user_name(cfg) -> str:
    """
Although this function is logically a small part of the total picture of
creating the environment for an application invocation, it is highly CPU
intensive because it loads the entire password file and uses regular
expressions to examine the content of the file.

The file is made up of records, one for each user recorded in the file and
a record is contained in a physical line.

Record processing has two stages. In the first stage, we determine if this
is a record of interest. In the second stage, we process the record. This
second level processing takes place only when we have identified that a record
is of interest.

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
    pass
