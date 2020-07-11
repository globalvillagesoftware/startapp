"""
Handler to interpret and act on pre-configuration values

This control file is a mixture of data and Python code. It is intended to
bootstrap the runtime environment. It contains two major types of data:

* The location of all the necessary runtime components
* The list of the master configuration files to be used.

This file is always found in the same directory as the Python module that
starts the execution of an application. This directory is called the
configuration directory and can be determined by examining sys.argv[0].
The parent directory of this directory will be a standard Python package.
This will be true for both development and for production systems. The
deployment procedures for this application will ensure that this state of
affairs holds.

The code for this module is contained in the class Master. This is a callable
class so it is easy to invoke. Running the module can be embedded in this file
by creating a Class instance for the Master class ans then calling it. Thus
everything in the module will run when the module is imported into a calling
module.

The master files are also always Python modules and are located relative to the
configuration directory. They can therefore be accessed using relative module
locations. This helps deployment and maintenance since the location of files
relative to the configuration directory can be hard coded. only the location
of the configuration directory changes and this can be determined when the
application runs.

.. only:: development_administrator
    
    Created on Jul. 6, 2020
    
    @author: Jonathan Gossage
"""
from importlib import import_module as im
from pathlib import Path
import sys
from typing import Dict, Tuple

class Master():
    """
    """
    _L = None
    configDir: Path = Path(Path(sys.argv[0]).resolve().parent)
    gvPackage  = 'gvconfig'
    
    @classmethod
    def lateInitialization(cls):
        import lib.gvLogging as _l
        Master._L = _l.Logging

    platformKey = 'platform'
    siteKey = 'siteMaster'
    organizationMasterKey = 'organizationMaster'
    gvKey = 'GlobalVillage'
    
    masterFiles: Dict[str, Tuple[str, str]] =\
    {platformKey : ('platform', 'Master'),
     siteKey : ('siteMaster', 'Site'),
     organizationMasterKey : ('organizationMaster', 'Organization'),
     gvKey : ('gvMaster', 'Supplier')}

    def __init__(self):
        """
        Makes sure that we can import the logging by delaying it until the
        first and only instance is in instance initialization. That way, we
        avoid recursive import attempts for the logging service.
        """
        if Master._L is None:
            Master.lateInitialization()

    def __call__(self) -> int:
        errors = 0
        sys.path.insert(0, Master.configDir)
        for _, targetModule in Master.masterFiles.values():
            if Path(Master.configDir / self.gvPackage /\
                    targetModule).joinpath('.py').is_file():
                try:
                    pm = im(targetModule, Master.gvPackage)
                    pm.configCode()()  # Run the code for the target module
                except ImportError:
                    Master._L.warning('Unable to import'
                                      f' {self.gvPackage}.{targetModule}')
                    errors += 1
                errors += pm.shutdown()
        return errors

