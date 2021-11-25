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

from general import lv3chr_facialsys_config; reload(lv3chr_facialsys_config)
from general.lv3chr_facialsys_config import *

import control_zone; reload(control_zone)
from control_zone import controlZone

# ======================================================================================================================
class eyelidControlZone(controlZone):
    """ Subclass of the controlZone, whose instances manage the control elements of the eyelid zone

    An eyelid control zone of a third-level character should contain 4 control curves,
    4*5 locators, and 5 controllers binding to 5 joints.
    """

    def __init__(self,
                 direction = controlZoneDirEnum.right_up,
                 ctrl_crv_data = None,
                 ctrlproj_transplane = None,
                 ctrlproj_projsurface = None
                 ):
        """ An Eyelid Control Zone instance's direction attribute may have the value of
            "right_up/RU", "right_dn/RD", "left_up/LU" or "left_dn/LD".
        """
        super(eyelidControlZone, self).__init__(zone = controlZoneEnum.eyelid,
                                                direction = direction,
                                                ctrl_crv_data = ctrl_crv_data,
                                                ctrlproj_transplane = ctrlproj_transplane,
                                                ctrlproj_projsurface = ctrlproj_projsurface
                                                )
