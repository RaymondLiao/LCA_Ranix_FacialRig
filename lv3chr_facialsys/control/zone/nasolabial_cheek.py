#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# File Name: control.zone.cheek.py
# Author: Sheng (Raymond) Liao
# Date: December 2021
#

"""
A module organizing the control elements of the nasolabial and the cheek zones
"""

import warnings
import maya.cmds as cmds

from general import config; reload(config)
from general.config import *

from general import hierarchy; reload(hierarchy)

from .. import control_zone; reload(control_zone)
from ..control_zone import controlZone

from .. import control_curve; reload(control_curve)
from ..control_curve import controlCurve

from .. import controller; reload(controller)
from ..controller import controller

# ======================================================================================================================
class nasoCheekControlZone(controlZone):
    """ Subclass of the controlZone, whose instances manage the control elements of the cheek zone
    """

    def __init__(self,
                 direction=controlZoneDirEnum.right):
        pass