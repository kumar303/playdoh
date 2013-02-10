import os
from .base import *
try:
    from .local import *
except ImportError, exc:
    if not STACKATO:
        # Assume it's a local install or a non-stackato install.
        # A local.py file may not be necessary for stackato VMs.
        exc.args = tuple(['%s (did you rename settings/local.py-dist?)' % exc.args[0]])
        raise exc
