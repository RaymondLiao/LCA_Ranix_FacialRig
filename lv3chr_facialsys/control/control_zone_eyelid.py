#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# File Name: control_zone.py
# Author: Sheng (Raymond) Liao
# Date: October 2021
#

"""
A module organizing the control elements of the eyelid zone
"""

import warnings
import maya.cmds as cmds

import control_zone; reload(control_zone)
from control_zone import controlZone

# ======================================================================================================================
class eyelidControlZone(controlZone):
    """ Subclass of the controlZone, whose instances manage the control elements of the eyelid zone

    An eyelid control zone of a third-level character should contain 4 control curves,
    4*5 locators, and 5 controllers binding to 5 joints.
    """