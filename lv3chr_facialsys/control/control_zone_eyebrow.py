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
from control_zone import controlZone

# ======================================================================================================================
class eyebrowControlZone(controlZone):
    """ Subclass of the controlZone, whose instances manage the control elements of the eyebrow zone

    [description of an eyebrow zone's composition here]
    """

    def __init__(self,
                 ctrl_crv_data = None,
                 ctrlproj_transplane = None,
                 ctrlproj_projsurface = None
                 ):
        """ An Eyebrow Control Zone instance's direction attribute have only one value "middle".
        """
        super(eyebrowControlZone, self).__int__(zone = controlZoneEnum.eyebrow,
                                                direction = controlZoneDirEnum.middle,
                                                ctrl_crv_data = ctrl_crv_data,
                                                ctrlproj_transplane = ctrlproj_transplane,
                                                ctrlproj_projsurface = ctrlproj_projsurface
                                                )