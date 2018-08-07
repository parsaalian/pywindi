"""
    pywindi
    ~~~~~~~

    Pywindi wraps and interfaces indi library, using PyIndi python package.
    Its aim is making indi more usable in a simple way. The audience may use
    this package without any knowledge of indi or PyIndi. It has its own
    architecture and methods and classes.

    It also provides synchronous functionality which can help for better
    usage.

    :copyright (c) 2018 by Parsa Alian & Emad Salehi & Seyed Sajad Kahani
    :license: GPL, see LICENSE for more details.
"""

# Utils
from .utils import EventManager, Queue

# Core classes
from .winclient import Winclient
from .windevice import Windevice

# Drivers
from .windrivers import SBIG_CCD, V4L2_CCD

__all__ = [
    # Utils
    'EventManager', 'Queue',

    # Core Classes
    'Winclient', 'Windevice',

    # Drivers
    'SBIG_CCD', 'V4L2_CCD',
]


__version__ = '0.3.0'
