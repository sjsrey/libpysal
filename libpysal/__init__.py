__version__ = "4.2.2"

# __version__ has to be define in the first line

"""
libpysal: Python Spatial Analysis Library (core)
================================================


Documentation
-------------
PySAL documentation is available in two forms: python docstrings and an html \
        webpage at http://pysal.org/

Available sub-packages
----------------------

cg
    Basic data structures and tools for Computational Geometry
examples
    Example data sets for testing and documentation
io
    Basic functions used by several sub-packages
weights
    Tools for creating and manipulating weights
"""
import importlib
import sys
import importlib
from types import ModuleType

from . import cg
from . import io
from . import weights



class LazyLoader(ModuleType):
    @property
    def examples(self):
        if not self.__dict__.get('examples'):
            self.__dict__['examples'] = importlib.import_module('.examples', __package__)

        return self.__dict__['examples']

    @examples.setter
    def examples(self, mod):
        self.__dict__['examples'] = mod

    # and so on for all the modules

old = sys.modules[__name__]
new = LazyLoader(__name__)
new.__path__ = old.__path__

for k, v in list(old.__dict__.items()):
    new.__dict__[k] = v

sys.modules[__name__] = new


