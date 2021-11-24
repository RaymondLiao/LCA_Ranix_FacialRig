#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# File Name: control_zone.py
# Author: Sheng (Raymond) Liao
# Date: October 2021
#

"""
A module organizing the control elements of the eyebrow zone
"""

import warnings
import maya.cmds as cmds

import control_zone; reload(control_zone)

# ======================================================================================================================
class eyebrowControlZone(controlZone):
    """ Subclass of the controlZone, whose instances manage the control elements of the eyebrow zone

    [description of an eyebrow zone's composition here]
    """
