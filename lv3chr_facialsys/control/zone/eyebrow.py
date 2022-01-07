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
    and 4 Translation Planes with 4 Projection Surfaces in the front direction.
    """

    def __init__(self,
                 ctrl_crv_data = None,
                 ctrlproj_transplane_LRUD       = None,
                 ctrlproj_transplane_LRFB_list  = [],
                 ctrlproj_projsurface_LRUD      = None,
                 ctrlproj_projsurface_LRFB_list = []):
        """ An Eyebrow Control Zone instance's direction attribute has only one valid value: the "middle".
        """
        super(eyebrowControlZone, self).__init__(zone = controlZoneEnum.eyebrow,
                                                 direction = controlZoneDirEnum.middle,
                                                 ctrl_crv_data = ctrl_crv_data,
                                                 ctrlproj_transplane_LRUD       = ctrlproj_transplane_LRUD,
                                                 ctrlproj_transplane_LRFB_list  = ctrlproj_transplane_LRFB_list,
                                                 ctrlproj_projsurface_LRUD      = ctrlproj_projsurface_LRUD,
                                                 ctrlproj_projsurface_LRFB_list = ctrlproj_projsurface_LRFB_list)

        assert None != ctrlproj_transplane_LRUD
        assert None != ctrlproj_projsurface_LRUD
        assert None != ctrlproj_transplane_LRFB_list and \
               isinstance(ctrlproj_transplane_LRFB_list, list) and 1 == len(ctrlproj_transplane_LRFB_list)
        assert None != ctrlproj_projsurface_LRFB_list and \
               isinstance(ctrlproj_projsurface_LRFB_list, list) and 4 == len(ctrlproj_projsurface_LRFB_list)

        ctrl_crv_id_list = ['A', 'B', 'C', 'D']
        controller_id_list = ['R_A', 'R_B', 'R_C', 'M_A', 'L_A', 'L_B', 'L_C']


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

                self._ctrl_crv_bs_dict[zone_dir+'_'+ctrl_crv_bs_dir] = bs_nurbs_crv

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

        # --------------------------------------------------------------------------------------------------------------
        # Drive the control curves using blend-shape and
        # five-curves each in the LR and UD directions, as the targets.

        ctrl_crv_bs = cmds.blendShape(self._ctrl_crv_bs_dict['right_right_side_up'],
                                      self._ctrl_crv_bs_dict['right_middle_side_up'],
                                      self._ctrl_crv_bs_dict['right_left_side_up'],
                                      self._ctrl_crv_bs_dict['middle_middle_side_up'],
                                      self._ctrl_crv_bs_dict['left_right_side_up'],
                                      self._ctrl_crv_bs_dict['left_middle_side_up'],
                                      self._ctrl_crv_bs_dict['left_left_side_up'],

                                      self._ctrl_crv_bs_dict['right_right_side_left'],
                                      self._ctrl_crv_bs_dict['right_middle_side_left'],
                                      self._ctrl_crv_bs_dict['right_left_side_left'],
                                      self._ctrl_crv_bs_dict['middle_middle_side_left'],
                                      self._ctrl_crv_bs_dict['left_right_side_left'],
                                      self._ctrl_crv_bs_dict['left_middle_side_left'],
                                      self._ctrl_crv_bs_dict['left_left_side_left'],

                                      self._ctrl_crv_bs_dict['right_right_side_front'],
                                      self._ctrl_crv_bs_dict['right_middle_side_front'],
                                      self._ctrl_crv_bs_dict['right_left_side_front'],
                                      self._ctrl_crv_bs_dict['middle_middle_side_front'],
                                      self._ctrl_crv_bs_dict['left_right_side_front'],
                                      self._ctrl_crv_bs_dict['left_middle_side_front'],
                                      self._ctrl_crv_bs_dict['left_left_side_front'],

                                      self._ctrl_crv_dict['A'].get_name(),
                                      name = self._ctrl_crv_dict['A'].get_name() + '_blendShape'
                                      )[0]
        cmds.setAttr(ctrl_crv_bs + '.supportNegativeWeights', True)

        cmds.connectAttr(self._controller_dict['R_A'].get_name() + '.translateX',
                         ctrl_crv_bs + '.' + self._ctrl_crv_bs_dict['right_right_side_left'])
        cmds.connectAttr(self._controller_dict['R_A'].get_name() + '.translateY',
                         ctrl_crv_bs + '.' + self._ctrl_crv_bs_dict['right_right_side_up'])
        cmds.connectAttr(self._controller_dict['R_A'].get_name() + '.translateZ',
                         ctrl_crv_bs + '.' + self._ctrl_crv_bs_dict['right_right_side_front'])

        cmds.connectAttr(self._controller_dict['R_B'].get_name() + '.translateX',
                         ctrl_crv_bs + '.' + self._ctrl_crv_bs_dict['right_middle_side_left'])
        cmds.connectAttr(self._controller_dict['R_B'].get_name() + '.translateY',
                         ctrl_crv_bs + '.' + self._ctrl_crv_bs_dict['right_middle_side_up'])
        cmds.connectAttr(self._controller_dict['R_B'].get_name() + '.translateZ',
                         ctrl_crv_bs + '.' + self._ctrl_crv_bs_dict['right_middle_side_front'])

        cmds.connectAttr(self._controller_dict['R_C'].get_name() + '.translateX',
                         ctrl_crv_bs + '.' + self._ctrl_crv_bs_dict['right_left_side_left'])
        cmds.connectAttr(self._controller_dict['R_C'].get_name() + '.translateY',
                         ctrl_crv_bs + '.' + self._ctrl_crv_bs_dict['right_left_side_up'])
        cmds.connectAttr(self._controller_dict['R_C'].get_name() + '.translateZ',
                         ctrl_crv_bs + '.' + self._ctrl_crv_bs_dict['right_left_side_front'])

        cmds.connectAttr(self._controller_dict['M_A'].get_name() + '.translateX',
                         ctrl_crv_bs + '.' + self._ctrl_crv_bs_dict['middle_middle_side_left'])
        cmds.connectAttr(self._controller_dict['M_A'].get_name() + '.translateY',
                         ctrl_crv_bs + '.' + self._ctrl_crv_bs_dict['middle_middle_side_up'])
        cmds.connectAttr(self._controller_dict['M_A'].get_name() + '.translateZ',
                         ctrl_crv_bs + '.' + self._ctrl_crv_bs_dict['middle_middle_side_front'])

        cmds.connectAttr(self._controller_dict['L_A'].get_name() + '.translateX',
                         ctrl_crv_bs + '.' + self._ctrl_crv_bs_dict['left_right_side_left'])
        cmds.connectAttr(self._controller_dict['L_A'].get_name() + '.translateY',
                         ctrl_crv_bs + '.' + self._ctrl_crv_bs_dict['left_right_side_up'])
        cmds.connectAttr(self._controller_dict['L_A'].get_name() + '.translateZ',
                         ctrl_crv_bs + '.' + self._ctrl_crv_bs_dict['left_right_side_front'])

        cmds.connectAttr(self._controller_dict['L_B'].get_name() + '.translateX',
                         ctrl_crv_bs + '.' + self._ctrl_crv_bs_dict['left_middle_side_left'])
        cmds.connectAttr(self._controller_dict['L_B'].get_name() + '.translateY',
                         ctrl_crv_bs + '.' + self._ctrl_crv_bs_dict['left_middle_side_up'])
        cmds.connectAttr(self._controller_dict['L_B'].get_name() + '.translateZ',
                         ctrl_crv_bs + '.' + self._ctrl_crv_bs_dict['left_middle_side_front'])

        cmds.connectAttr(self._controller_dict['L_C'].get_name() + '.translateX',
                         ctrl_crv_bs + '.' + self._ctrl_crv_bs_dict['left_left_side_left'])
        cmds.connectAttr(self._controller_dict['L_C'].get_name() + '.translateY',
                         ctrl_crv_bs + '.' + self._ctrl_crv_bs_dict['left_left_side_up'])
        cmds.connectAttr(self._controller_dict['L_C'].get_name() + '.translateZ',
                         ctrl_crv_bs + '.' + self._ctrl_crv_bs_dict['left_left_side_front'])

        # Create blend-shapes to control curves to transit the translations of controllers.

        cmds.select(deselect=True)
        eyebrow_follow_B_attr = self._follow_ctrl + '.eyebrow_follow_b'
        eyebrow_follow_C_attr = self._follow_ctrl + '.eyebrow_follow_c'
        eyebrow_follow_D_attr = self._follow_ctrl + '.eyebrow_follow_d'

        for ctrl_crv_id in ctrl_crv_id_list[1:]:
            ctrl_crv = self._ctrl_crv_dict[ctrl_crv_id]

            follow_attr = ''
            follow_val = 0.0

            if 'B' in ctrl_crv_id:
                follow_attr = eyebrow_follow_B_attr
            elif 'C' in ctrl_crv_id:
                follow_attr = eyebrow_follow_C_attr
            elif 'D' in ctrl_crv_id:
                follow_attr = eyebrow_follow_D_attr

            assert cmds.objExists(follow_attr)
            follow_val = cmds.getAttr(follow_attr)
            bs_node = cmds.blendShape(self._ctrl_crv_dict[ctrl_crv_id_list[0]].get_name(),
                                      ctrl_crv.get_name(),
                                      weight=[0, follow_val])
            bs_node = cmds.rename(bs_node, ctrl_crv.get_name() + '_bs')

            cmds.connectAttr(follow_attr, bs_node + '.weight[0]')

        # Use "closestPointOnSurface" nodes to establish the projecting relationships between
        # the locators on the control curves and the locators on the projection surfaces.

        for ctrl_crv_id in ctrl_crv_id_list:
            ctrl_crv = self._ctrl_crv_dict[ctrl_crv_id]

            loc_id_list = ctrl_crv.get_locator_ids()
            for loc_id in loc_id_list:
                ctrlcrv_loc_info = ctrl_crv.get_locator_info(loc_id)

                # Establish the projecting relationships in the up-down/UD directions.
                UD_projsrf_loc_info = self._ctrlproj_projsurface_LRUD.get_locator_info(ctrl_crv_id, loc_id)

                cls_pt_on_UD_transplane_node = cmds.createNode('closestPointOnSurface')
                cls_pt_on_UD_transplane_node = cmds.rename(cls_pt_on_UD_transplane_node,
                                                           ctrlcrv_loc_info[0] + '_srfUD_clsPtOnSrf')

                cmds.connectAttr(self._ctrlproj_transplane_LRUD.get_name() + '.worldSpace[0]',
                                 cls_pt_on_UD_transplane_node + '.inputSurface')
                cmds.connectAttr(ctrlcrv_loc_info[0] + 'Shape.worldPosition[0]',
                                 cls_pt_on_UD_transplane_node + '.inPosition')

                pt_on_UD_projsrf_node = UD_projsrf_loc_info[2]
                assert cmds.objExists(pt_on_UD_projsrf_node)

                cmds.connectAttr(cls_pt_on_UD_transplane_node + '.parameterU', pt_on_UD_projsrf_node + '.parameterU')
                cmds.connectAttr(cls_pt_on_UD_transplane_node + '.parameterV', pt_on_UD_projsrf_node + '.parameterV')

                # Establish the projecting relationships in the front/F direction.
                # Note that the eyebrow projection surface in the FB direction has 2 less locators on each side.
                front_projsrf_id = ord(ctrl_crv_id)-65

                # if loc_id <= 2:
                #     continue
                # if loc_id > len(loc_id_list)-2:
                #     break
                F_projsrf_loc_info = \
                    ctrlproj_projsurface_LRFB_list[front_projsrf_id].get_locator_info(ctrl_crv_id, loc_id)
                # if None == F_projsrf_loc_info:
                #     continue

                cls_pt_on_F_transplane_node = cmds.createNode('closestPointOnSurface')
                cls_pt_on_F_transplane_node = cmds.rename(cls_pt_on_F_transplane_node,
                                                          ctrlcrv_loc_info[0] + '_srfF_clsPtOnSrf')

                cmds.connectAttr(self._ctrlproj_transplane_LRFB_list[0].get_name() + '.worldSpace[0]',
                                 cls_pt_on_F_transplane_node + '.inputSurface')
                cmds.connectAttr(ctrlcrv_loc_info[0] + 'Shape.worldPosition[0]',
                                 cls_pt_on_F_transplane_node + '.inPosition')

                pt_on_F_projsrf_node = F_projsrf_loc_info[2]
                assert cmds.objExists(pt_on_F_projsrf_node)

                cmds.connectAttr(cls_pt_on_F_transplane_node + '.parameterU', pt_on_F_projsrf_node + '.parameterU')
                cmds.connectAttr(cls_pt_on_F_transplane_node + '.parameterV', pt_on_F_projsrf_node + '.parameterV')
