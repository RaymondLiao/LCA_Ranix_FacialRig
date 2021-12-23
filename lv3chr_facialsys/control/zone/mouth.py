#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# File Name: control.zone.mouth_cheek.py
# Author: Sheng (Raymond) Liao
# Date: December 2021
#

"""
A module organizing the control elements of the mouth zone
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
class mouthControlZone(controlZone):
    """ Subclass of the controlZone, whose instances manage the control elements of the mouth zone
    """

    def __init__(self,
                 direction=controlZoneDirEnum.middle + '_' + controlZoneDirEnum.up,
                 ctrl_crv_data = None,
                 ctrlproj_transplane_LRUD = None,
                 ctrlproj_projsurface_LRUD = None):
        """ A Mouth-Cheek Control Zone instance's direction attribute has only one valid value: the "middle".
        """
        super(mouthControlZone, self).__init__(zone = controlZoneEnum.mouth,
                                               direction = direction,
                                               ctrl_crv_data=ctrl_crv_data,
                                               ctrlproj_transplane_LRUD = ctrlproj_transplane_LRUD,
                                               ctrlproj_projsurface_LRUD = ctrlproj_projsurface_LRUD)

        ctrl_crv_id_list = ['A']
        controller_dir_list = ['R', 'M', 'L']

        # Create the control curves
        ctrlcrv_data = self._ctrl_crv_data['mouth_control_curve']
        ctrlcrv_degree = ctrlcrv_data['degree']

        for crv_id in ctrl_crv_id_list:
            dir_ctrlcrv_data = ctrlcrv_data[direction + '_' + crv_id]
            ctrl_crv = controlCurve(name_prefix = self._ctrl_crv_data['mouth_ctrlzone_prefix'],
                                    name = dir_ctrlcrv_data['name'],
                                    degree = ctrlcrv_degree,
                                    translation = dir_ctrlcrv_data['xform']['translation'],
                                    points = dir_ctrlcrv_data['points'],
                                    locator_data = dir_ctrlcrv_data['locators'],
                                    locator_scale = ctrlcrv_data['locator_scale'])

            loc_id_list = ctrl_crv.get_locator_ids()

            if controlZoneDirEnum.up in direction:
                cmds.parent(ctrl_crv.get_name(),
                            hierarchy.mouth_ctrlzone_MU_grp.get_group_name())

                for loc_id in loc_id_list:
                    loc_name = ctrl_crv.get_locator_info(locator_id=loc_id)[0]
                    cmds.parent(loc_name,
                                hierarchy.mouth_ctrlzone_loc_MU_A_grp.get_group_name())

            elif controlZoneDirEnum.down in direction:
                cmds.parent(ctrl_crv.get_name(),
                            hierarchy.mouth_ctrlzone_MD_grp.get_group_name())

                for loc_id in loc_id_list:
                    loc_name = ctrl_crv.get_locator_info(locator_id=loc_id)[0]
                    cmds.parent(loc_name,
                                hierarchy.mouth_ctrlzone_loc_MD_A_grp.get_group_name())

            self._ctrl_crv_dict[crv_id] = ctrl_crv

        cmds.select(deselect=True)

        # Create the curves serving as blend-shape targets for the control curves.
        ctrlcrv_bs_data = self._ctrl_crv_data['mouth_control_curve_bs']
        ctrlcrv_bs_degree = ctrlcrv_bs_data['degree']

        for ctrl_crv_bs_dir in ctrl_crv_bs_dir_list:
            dir_ctrlcrv_bs_data = ctrlcrv_bs_data[ctrl_crv_bs_dir]

            bs_nurbs_crv = cmds.curve(degree=ctrlcrv_bs_degree,
                                      point=dir_ctrlcrv_bs_data['points'])
            cmds.xform(bs_nurbs_crv, translation=dir_ctrlcrv_bs_data['xform']['translation'])
            bs_nurbs_crv = cmds.rename(bs_nurbs_crv, dir_ctrlcrv_bs_data['name'])

            cmds.setAttr(bs_nurbs_crv + '.overrideEnabled', True)
            if 'left' in ctrl_crv_bs_dir:
                cmds.setAttr(bs_nurbs_crv + '.overrideColor', COLOR_INDEX_DARK_RED)
            elif 'right' in ctrl_crv_bs_dir:
                cmds.setAttr(bs_nurbs_crv + '.overrideColor', COLOR_INDEX_INDIGO)
            else:
                cmds.setAttr(bs_nurbs_crv + '.overrideColor', COLOR_INDEX_OLIVE)

            cmds.toggle(bs_nurbs_crv, controlVertex=True)
            cmds.select(deselect=True)

            cmds.parent(bs_nurbs_crv,
                        hierarchy.mouth_ctrlzone_curve_bs_grp.get_group_name())

        # Create the controllers
        controller_data = self._ctrl_crv_data['mouth_controller']
        controller_degree = controller_data['degree']
        direction_UD = direction.split('_')[1]
        controller_points = []
        controller_color = 0

        for ctrl_dir in controller_dir_list:
            if 'R' == ctrl_dir:
                controller_points = controller_data['points_right_' + direction_UD]
                direction = 'right_' + direction_UD
                controller_color = CONTROL_R_COLOR
            elif 'M' == ctrl_dir:
                controller_points = controller_data['points_middle_' + direction_UD]
                direction = 'middle_' + direction_UD
                controller_color = CONTROL_M_COLOR
            elif 'L' == ctrl_dir:
                controller_points = controller_data['points_left_' + direction_UD]
                direction = 'left_' + direction_UD
                controller_color = CONTROL_L_COLOR

            dir_ctrl_data = controller_data[direction]
            rig_controller = controller(name=self._ctrl_crv_data['mouth_ctrlzone_prefix'] + '_' +
                                             dir_ctrl_data['name'],
                                        degree=controller_degree,
                                        color=controller_color,
                                        points=controller_points,
                                        translation_ofs=dir_ctrl_data['xform']['translation_ofs'],
                                        translation=dir_ctrl_data['xform']['translation'],
                                        lock_trans_axes=controller_data['lock_trans_axes'],
                                        lock_rot_axes=controller_data['lock_rot_axes'],
                                        bind_joint_data=controller_data['bind_joint'],
                                        bind_joint_color=BIND_JOINT_COLOR_INDEX)

            cmds.parent(rig_controller.get_offset_group(),
                        hierarchy.eyebrow_ctrl_M_grp.get_group_name(),
                        relative=True)

            self._controller_dict[ctrl_dir] = rig_controller

        # --------------------------------------------------------------------------------------------------------------
        # Bind the control curves to the corresponding controllers' joints

        # Use "closestPointOnSurface" nodes to establish the projecting relationships between
        # the locators on the control curves and the locators on the projection surfaces.