"""
Platform specific support

This is an operating system dependent package. I will be deployed in an
operating system dependent package that has the same name as is returned
by platform.system(). One such package and module exists for every platform
supported by this framework.

It contains functions that are platform specific. Every platform specific
package contains identically named functions. This allows the module to be
imported like this:
    `from linux import *`
When this function succeeds, all the platform specific functions will have been
imported and can be used directly without needing to consider that they are
platform specific in their implementation.

Created on Apr. 18, 2020

@author: Jonathan Gossage
"""
from getpass import getuser

import configuration as _c


def platformConfiguration():
    """
This function will generate a dictionary containing entries whose values are
determined in a platform specific manner. The key will be the name of the
configuration entry and the value will be its value as discovered on the
specific platform.
    """

    cfg = {}
    cfg[_c.userid] = getuser()
    return cfg
