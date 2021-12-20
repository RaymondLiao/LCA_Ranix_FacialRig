#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# File Name: control.zone.mouth_cheek.py
# Author: Sheng (Raymond) Liao
# Date: December 2021
#

"""
A module organizing the control elements of the mouth and cheek zones of the lower face
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
class mouthCheekControlZone(controlZone):
    """ Subclass of the controlZone, whose instances manage the control elements of the mouth and cheek lower-face zones

    The control curves of the cheek control zone each contains a straight curve as the blendShape base shape
    which is driven by the motion of controllers, a curve originally shaped along with the face topological edge,
    and a curve as the final projection curve using the first two as the BS targets, functioning as a whole.
    """

    def __init__(self,
                 ctrl_crv_data = None,
                 ctrlproj_transplane_LRUD = None,
                 ctrlproj_projsurface_LRUD = None):
        """ A Mouth-Cheek Control Zone instance's direction attribute has only one valid value: the "middle".
        """
        super(mouthCheekControlZone, self).__init__(zone = controlZoneEnum.mouth_cheek,
                                                    direction = controlZoneDirection.middle,
                                                    ctrlproj_transplane_LRUD = ctrlproj_transplane_LRUD,
                                                    ctrlproj_projsurface_LRUD = ctrlproj_projsurface_LRUD)

        # Create the control curves

        # Create the controllers

        # --------------------------------------------------------------------------------------------------------------
        # Bind the control curves to the corresponding controllers' joints

        # Use "closestPointOnSurface" nodes to establish the projecting relationships between
        # the locators on the control curves and the locators on the projection surfaces.