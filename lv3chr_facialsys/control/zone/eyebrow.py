#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# File Name: control.zone.eyebrow.py
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
        controller_id_list = ['R_D', 'R_C', 'R_B', 'R_A', 'M_A', 'L_A', 'L_B', 'L_C', 'L_D']


        # Create the control curves.
        ctrlcrv_data = self._ctrl_crv_data['eyebrow_control_curve']
        ctrlcrv_degree = ctrlcrv_data['degree']

        for crv_id in ctrl_crv_id_list:
            dir_ctrlcrv_data = ctrlcrv_data[controlZoneDirEnum.middle + '_' + crv_id]
            ctrl_crv = controlCurve(name_prefix = self._ctrl_crv_data['eyebrow_ctrlzone_prefix'],
                                    name = dir_ctrlcrv_data['name'],
                                    degree = ctrlcrv_degree,
                                    translation = dir_ctrlcrv_data['xform']['translation'],
                                    points = dir_ctrlcrv_data['points'],
                                    locator_data = dir_ctrlcrv_data['locators'],
                                    locator_scale = ctrlcrv_data['locator_scale'])

            cmds.parent(ctrl_crv.get_name(),
                        hierarchy.eyebrow_ctrlzone_M_grp.get_group_name())

            loc_id_list = ctrl_crv.get_locator_ids()
            for loc_id in loc_id_list:
                loc_name = ctrl_crv.get_locator_info(locator_id=loc_id)[0]
                if 'A' == crv_id:
                    cmds.parent(loc_name,
                                hierarchy.eyebrow_ctrlzone_loc_M_A_grp.get_group_name())
                elif 'B' == crv_id:
                    cmds.parent(loc_name,
                                hierarchy.eyebrow_ctrlzone_loc_M_B_grp.get_group_name())
                elif 'C' == crv_id:
                    cmds.parent(loc_name,
                                hierarchy.eyebrow_ctrlzone_loc_M_C_grp.get_group_name())

            self._ctrl_crv_dict[crv_id] = ctrl_crv

        cmds.select(deselect=True)

        # Create the controllers.
        controller_data = self._ctrl_crv_data['eyebrow_controller']
        controller_degree = controller_data['degree']
        direction = None
        controller_points = []
        controller_color = 0

        for ctrl_id in controller_id_list:
            if 'R' in ctrl_id:
                controller_points = controller_data['points_right']
                direction = controlZoneDirEnum.right
                controller_color = CONTROL_R_COLOR
            elif 'M' in ctrl_id:
                controller_points = controller_data['points_middle']
                direction = controlZoneDirEnum.middle
                controller_color = CONTROL_M_COLOR
            elif 'L' in ctrl_id:
                controller_points = controller_data['points_left']
                direction = controlZoneDirEnum.left
                controller_color = CONTROL_L_COLOR

            dir_ctrl_data = controller_data[direction + '_' + ctrl_id.split('_')[1]]
            rig_controller = controller(name = self._ctrl_crv_data['eyebrow_ctrlzone_prefix'] + '_' +
                                               dir_ctrl_data['name'],
                                        degree = controller_degree,
                                        color = controller_color,
                                        points = controller_points,
                                        translation_ofs = dir_ctrl_data['xform']['translation_ofs'],
                                        translation = dir_ctrl_data['xform']['translation'],
                                        lock_trans_axes = controller_data['lock_trans_axes'],
                                        lock_rot_axes = controller_data['lock_rot_axes'],
                                        bind_joint_data = controller_data['bind_joint'],
                                        bind_joint_color = BIND_JOINT_COLOR_INDEX)

            cmds.parent(rig_controller.get_offset_group(),
                        hierarchy.eyebrow_ctrl_M_grp.get_group_name(),
                        relative=True)

            self._controller_dict[ctrl_id] = rig_controller