"""
Created on Apr. 18, 2020

@author: Jonathan Gossage
"""

from typing import Dict, Text
import platform


class Platform(object):
    """
    This class obtains the following platform information from the operating
    system in a platform dependent manner:
    
    * platform type
    * platform name
    * platform version

   The Linux platform is the only one currently supported.
    
    """


    # Keys naming the records in the platform_desc dictionary
    MachineType = '0'
    Processor   = '1'
    Release     = '3'
    System      = '4'
    Version     = '5'

    def __init__(self):
        """
        Constructor
        
        Some basic information is captured here including:
        
        * Machine type
        * Processor - Specific processor model, not always available
        * Release - Operating system release
        """

        self._platform_desc                       = {}
        self._platform_desc[Platform.MachineType] = platform.machine()
        self._platform_desc[Platform.Processor]   = platform.processor()
        self._platform_desc[Platform.Release]     = platform.release()
        self._platform_desc[Platform.System]      = platform.system()
        self._platform_desc[Platform.Version]     = platform.version()

    @property
    def platform(self) -> Dict[Text, Text]:
        return self._platform_desc
