#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# File Name: eyebrow.py
# Author: Sheng (Raymond) Liao
# Date: November 2021
#

"""
A module organizing the control elements of the eyebrow zone
"""

import warnings
import maya.cmds as cmds

from general import util; reload(util)

from general import config; reload(config)
from general.config import *

from general import hierarchy; reload(hierarchy)

from .. import control_zone; reload(control_zone)
from ..control_zone import controlZone

from ..import control_curve; reload(control_curve)
from ..control_curve import controlCurve

from .. import controller; reload(controller)
from ..controller import controller

# ======================================================================================================================
class eyebrowControlZone(controlZone):
    """ Subclass of the controlZone, whose instances manage the control elements of the eyebrow zone

    [description of an eyebrow zone's composition here]
    """

    def __init__(self,
                 ctrl_crv_data = None,
                 ctrlproj_transplane_LRUD = None,
                 ctrlproj_transplane_LRFB = None,
                 ctrlproj_projsurface_LRUD = None,
                 ctrlproj_projsurface_LRFB = None
                 ):
        """ An Eyebrow Control Zone instance's direction attribute have only one value "middle".
        """
        super(eyebrowControlZone, self).__init__(zone = controlZoneEnum.eyebrow,
                                                 direction = controlZoneDirEnum.middle,
                                                 ctrl_crv_data = ctrl_crv_data,
                                                 ctrlproj_transplane_LRUD = ctrlproj_transplane_LRUD,
                                                 ctrlproj_transplane_LRFB = ctrlproj_transplane_LRFB,
                                                 ctrlproj_projsurface_LRUD = ctrlproj_projsurface_LRUD,
                                                 ctrlproj_projsurface_LRFB = ctrlproj_projsurface_LRFB,
                                                )

        ctrl_crv_id_list = ['A', 'B', 'C']

        # Create the control curves.
        ctrlcrv_data = ctrl_crv_data['eyebrow_control_curve']
        ctrlcrv_degree = ctrlcrv_data['degree']

        for crv_id in ctrl_crv_id_list:
            dir_ctrlcrv_data = ctrlcrv_data[controlZoneDirEnum.middle + '_' + crv_id]
            ctrl_crv = controlCurve(name_prefix = ctrl_crv_data['eyebrow_ctrlzone_prefix'],
                                    name = dir_ctrlcrv_data['name'],
                                    degree = ctrlcrv_degree,
                                    translation = dir_ctrlcrv_data['xform']['translation'],
                                    points = dir_ctrlcrv_data['points'],
                                    locator_data = dir_ctrlcrv_data['locators'],
                                    locator_scale = ctrlcrv_data['locator_scale'])

            cmds.parent(ctrl_crv.get_name(),
                        hierarchy.eyebrow_ctrlzone_M_grp.get_group_name())

            self._ctrl_crv_dict[crv_id] = ctrl_crv

        cmds.select(deselect=True)