#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# File Name: control_zone.py
# Author: Sheng (Raymond) Liao
# Date: October 2021
#

"""
A module organizing the control elements
"""

import warnings
import maya.cmds as cmds

from general import config; reload(config)
from general.config import *

from general import hierarchy; reload(hierarchy)

import control_curve; reload(control_curve)
from control_curve import controlCurve

import controller; reload(controller)
from controller import controller

# ======================================================================================================================
class controlZone(object):
    """ A control zone organizes the controllers, the control curves, and the locator_data as well as the bind joints
    corresponding to the CVs on the curves functioning as a whole.

    For eyelid module, a control zone should contain 4 control curves, 4*5 locators, and 5 controllers binding to
    5 joints as a unit to transfer the translations of controllers to the locators on a projection plane.
    """

    def get_ctrlcrv_count(self):
        return len(self._ctrl_crv_dict)

    def get_controller_count(self):
        return len(self._controller_dict)

    def __init__(self,
                 zone = controlZoneEnum.eyelid,
                 direction = controlZoneDirEnum.right,
                 ctrl_crv_data = None,
                 ctrlproj_transplane_LRUD       = None,
                 ctrlproj_transplane_LRFB_list  = [],
                 ctrlproj_transplane_UDFB_list  = [],
                 ctrlproj_projsurface_LRUD      = None,
                 ctrlproj_projsurface_LRFB_list = [],
                 ctrlproj_projsurface_UDFB_list = []
                 ):
        """
        :param zone: the facial zone this control unit manages
        :param direction: the direction in which the controllers of this control unit move
        :param ctrl_crv_data: the control curves' and controllers' construction data
        :param ctrlproj_transplane: the controllers translation plane this control unit belongs to
        :param ctrlproj_projsurface: the controllers translation-projection surface this control unit belongs to
        """

        # Member Variable Definitions ----------------------------------------------------------------------------------
        # The keys of this dictionary are curves' IDs.
        self._ctrl_crv_dict = {
            # 'A': None,
        }
        # The keys of this dictionary are:
        #   'original'
        #   'right_side_up', 'middle_side_up', 'left_side_up'
        #   'right_side_left, 'middle_side_left', 'left_side_left',
        #   'right_side_front', 'middle_side_front', 'left_side_front'
        self._ctrl_crv_bs_dict = {
            # 'original': None,
        }

        # The keys of this dictionary are follow controller's IDs.
        self._follow_ctrl = None

        # The keys of this dictionary are controllers' IDs.
        self._controller_dict = {
            # 'A': None,
        }

        self._ctrl_crv_data = ctrl_crv_data
        self._direction = direction

        self._ctrlproj_transplane_LRUD          = ctrlproj_transplane_LRUD
        self._ctrlproj_transplane_LRFB_list     = ctrlproj_transplane_LRFB_list
        self._ctrlproj_transplane_UDFB_list     = ctrlproj_transplane_UDFB_list
        self._ctrlproj_projsurface_LRUD         = ctrlproj_projsurface_LRUD
        self._ctrlproj_projsurface_LRFB_list    = ctrlproj_projsurface_LRFB_list
        self._ctrlproj_projsurface_UDFB_list    = ctrlproj_projsurface_UDFB_list
        # ---------------------------------------------------------------------------------- Member Variable Definitions

        assert None != self._ctrl_crv_data