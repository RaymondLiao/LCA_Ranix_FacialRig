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

    An eyebrow control zone of a third-level character should contain 3 control curves,
    3*9 locators, and 9 controllers (4 on the left, 1 in the middle, 4 on the right) binding to 9 joints.

    Also, an eyebrow control zone composites 1 Translation Plane with 1 Projection Surface in the up-down direction,
    and 1 Translation Plane with 1 Projection Surface in the front direction.
    """

    def __init__(self,
                 ctrl_crv_data = None,
                 ctrlproj_transplane_LRUD = None,
                 ctrlproj_transplane_LRFB = None,
                 ctrlproj_projsurface_LRUD = None,
                 ctrlproj_projsurface_LRFB = None
                 ):
        """ An Eyebrow Control Zone instance's direction attribute has only one valid value: the "middle".
        """
        super(eyebrowControlZone, self).__init__(zone = controlZoneEnum.eyebrow,
                                                 direction = controlZoneDirEnum.middle,
                                                 ctrl_crv_data = ctrl_crv_data,
                                                 ctrlproj_transplane_LRUD = ctrlproj_transplane_LRUD,
                                                 ctrlproj_transplane_LRFB = ctrlproj_transplane_LRFB,
                                                 ctrlproj_projsurface_LRUD = ctrlproj_projsurface_LRUD,
                                                 ctrlproj_projsurface_LRFB = ctrlproj_projsurface_LRFB,
                                                )

        ctrl_crv_id_list = ['A', 'B', 'C', 'D']
        controller_id_list = ['R_H', 'R_G', 'R_F', 'R_E', 'R_D', 'R_C', 'R_B', 'R_A',
                              'M_A',
                              'L_H', 'L_A', 'L_B', 'L_C', 'L_D', 'L_E', 'L_F', 'L_G']


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
                elif 'D' == crv_id:
                    cmds.parent(loc_name,
                                hierarchy.eyebrow_ctrlzone_loc_M_D_grp.get_group_name())

            self._ctrl_crv_dict[crv_id] = ctrl_crv

        cmds.select(deselect=True)

        # Create the curves serving as blend-shape targets for the control curves.
        ctrlcrv_bs_data = self._ctrl_crv_data['eyebrow_control_curve_bs']
        ctrlcrv_bs_degree = ctrlcrv_bs_data['degree']

        for ctrl_crv_bs_dir in G_CTRLCRV_BS_DIR_LIST:
            if 'original' in ctrl_crv_bs_dir or 'end' in ctrl_crv_bs_dir:
                continue

            for zone_dir in ['right', 'middle', 'left']:
                if 'middle' == zone_dir and 'middle_side' not in ctrl_crv_bs_dir:
                    continue

                dir_ctrlcrv_bs_data = ctrlcrv_bs_data[zone_dir+'_'+ctrl_crv_bs_dir]

                bs_nurbs_crv = cmds.curve(degree=ctrlcrv_bs_degree,
                                          point=dir_ctrlcrv_bs_data['points'])
                cmds.xform(bs_nurbs_crv, translation=dir_ctrlcrv_bs_data['xform']['translation'])
                bs_nurbs_crv = cmds.rename(bs_nurbs_crv,
                                           self._ctrl_crv_data['mouth_ctrlzone_prefix'] + '_' +
                                           zone_dir[0].upper() + '_' + dir_ctrlcrv_bs_data['name'])

                cmds.setAttr(bs_nurbs_crv + '.overrideEnabled', True)
                if controlZoneDirEnum.left in zone_dir:
                    cmds.setAttr(bs_nurbs_crv + '.overrideColor', COLOR_INDEX_DARK_RED)
                elif controlZoneDirEnum.right in zone_dir:
                    cmds.setAttr(bs_nurbs_crv + '.overrideColor', COLOR_INDEX_INDIGO)
                else:
                    cmds.setAttr(bs_nurbs_crv + '.overrideColor', COLOR_INDEX_OLIVE)

                cmds.toggle(bs_nurbs_crv, controlVertex=True)
                cmds.select(deselect=True)

                cmds.parent(bs_nurbs_crv,
                            hierarchy.eyebrow_ctrlcrv_bs_R_grp.get_group_name())

            # Create the control curve follow controllers.
            follow_ctrl_data = self._ctrl_crv_data['eyebrow_follow_controller']

            follow_ctrl = follow_ctrl_data['M']['name']

            # If the follow controller has not been created, make one.
            if not cmds.objExists(follow_ctrl):

                follow_ctrl_crv = cmds.curve(degree=follow_ctrl_data['degree'],
                                             point=follow_ctrl_data['points'])

                cmds.xform(follow_ctrl_crv,
                           translation=follow_ctrl_data['M']['xform']['translation'],
                           scale=follow_ctrl_data['M']['xform']['scale'])

                follow_ctrl_crv = cmds.rename(follow_ctrl_crv, follow_ctrl_data['M']['name'])

                follow_data_list = follow_ctrl_data['follow_data']
                for follow_attr, val in follow_data_list.items():
                    cmds.addAttr(follow_ctrl, longName=follow_attr, attributeType='float',
                                 defaultValue=val, minValue=0.0, maxValue=1.0, keyable=True)

                cmds.setAttr(follow_ctrl + '.overrideEnabled', True)
                cmds.setAttr(follow_ctrl + '.overrideColor', CONTROL_M_COLOR)

                cmds.parent(follow_ctrl, hierarchy.eyebrow_grp.get_group_name())

                cmds.select(deselect=True)

            self._follow_ctrl = follow_ctrl

        # # Create the controllers.
        # controller_data = self._ctrl_crv_data['eyebrow_controller']
        # controller_degree = controller_data['degree']
        # direction = None
        # controller_points = []
        # controller_color = 0
        #
        # for ctrl_id in controller_id_list:
        #     if 'R' in ctrl_id:
        #         controller_points = controller_data['points_right']
        #         direction = controlZoneDirEnum.right
        #         controller_color = CONTROL_R_COLOR
        #     elif 'M' in ctrl_id:
        #         controller_points = controller_data['points_middle']
        #         direction = controlZoneDirEnum.middle
        #         controller_color = CONTROL_M_COLOR
        #     elif 'L' in ctrl_id:
        #         controller_points = controller_data['points_left']
        #         direction = controlZoneDirEnum.left
        #         controller_color = CONTROL_L_COLOR
        #
        #     dir_ctrl_data = controller_data[direction + '_' + ctrl_id.split('_')[1]]
        #     rig_controller = controller(name = self._ctrl_crv_data['eyebrow_ctrlzone_prefix'] + '_' +
        #                                        dir_ctrl_data['name'],
        #                                 degree = controller_degree,
        #                                 color = controller_color,
        #                                 points = controller_points,
        #                                 translation_ofs = dir_ctrl_data['xform']['translation_ofs'],
        #                                 translation = dir_ctrl_data['xform']['translation'],
        #                                 lock_trans_axes = controller_data['lock_trans_axes'],
        #                                 lock_rot_axes = controller_data['lock_rot_axes'],
        #                                 bind_joint_data = controller_data['bind_joint'],
        #                                 bind_joint_color = BIND_JOINT_COLOR_INDEX)
        #
        #     cmds.parent(rig_controller.get_offset_group(),
        #                 hierarchy.eyebrow_ctrl_M_grp.get_group_name(),
        #                 relative=True)
        #
        #     self._controller_dict[ctrl_id] = rig_controller
        #
        # # --------------------------------------------------------------------------------------------------------------
        # # Bind the control curves to the corresponding controllers' joints.
        # cmds.select(deselect=True)
        # for ctrl_id, ctrl in self._controller_dict.items():
        #     ctrl_bind_jnt = ctrl.get_bind_joint()
        #     cmds.select(ctrl_bind_jnt, add=True)
        # cmds.select(self._ctrl_crv_dict[ctrl_crv_id_list[0]].get_name(), add=True)
        #
        # skincluster_node = cmds.skinCluster(toSelectedBones=True)
        # cmds.rename(skincluster_node, self._ctrl_crv_dict[ctrl_crv_id_list[0]].get_name() + '_skinCluster')
        #
        # # Create the blendshapes to control curves to transit the translations of controllers.
        # cmds.select(deselect=True)
        # follow_val = 0.5
        #
        # for ctrl_crv_id in ctrl_crv_id_list[1:]:
        #     ctrl_crv = self._ctrl_crv_dict[ctrl_crv_id]
        #     bs_node = cmds.blendShape(self._ctrl_crv_dict[ctrl_crv_id_list[0]].get_name(),
        #                               ctrl_crv.get_name(),
        #                               weight=[0, follow_val])
        #     bs_node = cmds.rename(bs_node, ctrl_crv.get_name() + '_bs')
        #
        # # Use "closestPointOnSurface" nodes to establish the projecting relationships between
        # # the locators on the control curves and the locators on the projection surfaces.
        #
        # for ctrl_crv_id in ctrl_crv_id_list:
        #     ctrl_crv = self._ctrl_crv_dict[ctrl_crv_id]
        #
        #     loc_id_list = ctrl_crv.get_locator_ids()
        #     for loc_id in loc_id_list:
        #         ctrlcrv_loc_info = ctrl_crv.get_locator_info(loc_id)
        #
        #         # Establish the projecting relationships in the up-down/UD directions.
        #         UD_projsrf_loc_info = self._ctrlproj_projsurface_LRUD.get_locator_info(ctrl_crv_id, loc_id)
        #
        #         cls_pt_on_UD_transplane_node = cmds.createNode('closestPointOnSurface')
        #         cls_pt_on_UD_transplane_node = cmds.rename(cls_pt_on_UD_transplane_node,
        #                                                    ctrlcrv_loc_info[0] + '_srfUD_clsPtOnSrf')
        #
        #         cmds.connectAttr(self._ctrlproj_transplane_LRUD.get_name() + '.worldSpace[0]',
        #                          cls_pt_on_UD_transplane_node + '.inputSurface')
        #         cmds.connectAttr(ctrlcrv_loc_info[0] + 'Shape.worldPosition[0]',
        #                          cls_pt_on_UD_transplane_node + '.inPosition')
        #
        #         pt_on_UD_projsrf_node = UD_projsrf_loc_info[2]
        #         assert cmds.objExists(pt_on_UD_projsrf_node)
        #
        #         cmds.connectAttr(cls_pt_on_UD_transplane_node + '.parameterU', pt_on_UD_projsrf_node + '.parameterU')
        #         cmds.connectAttr(cls_pt_on_UD_transplane_node + '.parameterV', pt_on_UD_projsrf_node + '.parameterV')
        #
        #         if ctrl_crv_id_list[0] in ctrl_crv.get_name():
        #             # Establish the projecting relationships in the front/F direction.
        #             # Note that the eyebrow projection surface in the FB direction has 2 less locators on each side.
        #             if loc_id <= 2:
        #                 continue
        #             if loc_id > len(loc_id_list)-2:
        #                 break
        #             F_projsrf_loc_info = self._ctrlproj_projsurface_LRFB.get_locator_info(ctrl_crv_id, loc_id-2)
        #             if None == F_projsrf_loc_info:
        #                 continue
        #
        #             cls_pt_on_F_transplane_node = cmds.createNode('closestPointOnSurface')
        #             cls_pt_on_F_transplane_node = cmds.rename(cls_pt_on_F_transplane_node,
        #                                                       ctrlcrv_loc_info[0] + '_srfF_clsPtOnSrf')
        #
        #             cmds.connectAttr(self._ctrlproj_transplane_LRFB.get_name() + '.worldSpace[0]',
        #                              cls_pt_on_F_transplane_node + '.inputSurface')
        #             cmds.connectAttr(ctrlcrv_loc_info[0] + 'Shape.worldPosition[0]',
        #                              cls_pt_on_F_transplane_node + '.inPosition')
        #
        #             pt_on_F_projsrf_node = F_projsrf_loc_info[2]
        #             assert cmds.objExists(pt_on_F_projsrf_node)
        #
        #             cmds.connectAttr(cls_pt_on_F_transplane_node + '.parameterU', pt_on_F_projsrf_node + '.parameterU')
        #             cmds.connectAttr(cls_pt_on_F_transplane_node + '.parameterV', pt_on_F_projsrf_node + '.parameterV')
