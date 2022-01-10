#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# File Name: control.zone.eyelid.py
# Author: Sheng (Raymond) Liao
# Date: November 2021
#

"""
A module organizing the control elements of the eyelid zone
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
class eyelidControlZone(controlZone):
    """ Subclass of the controlZone, whose instances manage the control elements of the eyelid zone

    An eyelid control zone of a third-level character should contain 4 control curves,
    4*5 locators, and 5 controllers binding to 5 joints.
    """

    def __init__(self,
                 direction = controlZoneDirEnum.right + '_' + controlZoneDirEnum.up,
                 ctrl_crv_data = None,
                 ctrlproj_transplane_LRUD = None,
                 ctrlproj_projsurface_LRUD = None):
        """ An Eyelid Control Zone instance's direction attribute may have the value of
            "right_up/RU", "right_dn/RD", "left_up/LU" or "left_dn/LD".
        """

        super(eyelidControlZone, self).__init__(zone = controlZoneEnum.eyelid,
                                                direction = direction,
                                                ctrl_crv_data = ctrl_crv_data,
                                                ctrlproj_transplane_LRUD = ctrlproj_transplane_LRUD,
                                                ctrlproj_projsurface_LRUD = ctrlproj_projsurface_LRUD)
        ctrl_crv_id_list = ['A', 'B', 'C', 'D', 'E']
        controller_id_list = ['A', 'B', 'C', 'D', 'E']
        if controlZoneDirEnum.right in direction:
            controller_id_list.reverse()

        # Create the control curves.
        ctrlcrv_data = self._ctrl_crv_data['eyelid_control_curve']
        ctrlcrv_degree = ctrlcrv_data['degree']

        for crv_id in ctrl_crv_id_list:
            dir_ctrlcrv_data = ctrlcrv_data[direction + '_' + crv_id]
            ctrl_crv = controlCurve(name_prefix = self._ctrl_crv_data['eyelid_ctrlzone_prefix'],
                                    name = dir_ctrlcrv_data['name'],
                                    degree = ctrlcrv_degree,
                                    translation = dir_ctrlcrv_data['xform']['translation'],
                                    points = dir_ctrlcrv_data['points'],
                                    locator_data = dir_ctrlcrv_data['locators'],
                                    locator_scale = ctrlcrv_data['locator_scale'])

            loc_id_list = ctrl_crv.get_locator_ids()

            if controlZoneDirEnum.right in direction and controlZoneDirEnum.up in direction:
                cmds.parent(ctrl_crv.get_name(),
                            hierarchy.eyelid_ctrlzone_RU_grp.get_group_name())

                for loc_id in loc_id_list:
                    loc_name = ctrl_crv.get_locator_info(locator_id=loc_id)[0]
                    if 'A' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.eyelid_ctrlzone_loc_RU_A_grp.get_group_name())
                    elif 'B' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.eyelid_ctrlzone_loc_RU_B_grp.get_group_name())
                    elif 'C' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.eyelid_ctrlzone_loc_RU_C_grp.get_group_name())
                    elif 'D' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.eyelid_ctrlzone_loc_RU_D_grp.get_group_name())
                    elif 'E' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.eyelid_ctrlzone_loc_RU_E_grp.get_group_name())

            elif controlZoneDirEnum.right in direction and controlZoneDirEnum.down in direction:
                cmds.parent(ctrl_crv.get_name(),
                            hierarchy.eyelid_ctrlzone_RD_grp.get_group_name())

                for loc_id in loc_id_list:
                    loc_name = ctrl_crv.get_locator_info(locator_id=loc_id)[0]
                    if 'A' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.eyelid_ctrlzone_loc_RD_A_grp.get_group_name())
                    elif 'B' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.eyelid_ctrlzone_loc_RD_B_grp.get_group_name())
                    elif 'C' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.eyelid_ctrlzone_loc_RD_C_grp.get_group_name())
                    elif 'D' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.eyelid_ctrlzone_loc_RD_D_grp.get_group_name())
                    elif 'E' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.eyelid_ctrlzone_loc_RD_E_grp.get_group_name())

            elif controlZoneDirEnum.left in direction and controlZoneDirEnum.up in direction:
                cmds.parent(ctrl_crv.get_name(),
                            hierarchy.eyelid_ctrlzone_LU_grp.get_group_name())

                for loc_id in loc_id_list:
                    loc_name = ctrl_crv.get_locator_info(locator_id=loc_id)[0]
                    if 'A' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.eyelid_ctrlzone_loc_LU_A_grp.get_group_name())
                    elif 'B' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.eyelid_ctrlzone_loc_LU_B_grp.get_group_name())
                    elif 'C' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.eyelid_ctrlzone_loc_LU_C_grp.get_group_name())
                    elif 'D' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.eyelid_ctrlzone_loc_LU_D_grp.get_group_name())
                    elif 'E' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.eyelid_ctrlzone_loc_LU_E_grp.get_group_name())

            elif controlZoneDirEnum.left in direction and controlZoneDirEnum.down in direction:
                cmds.parent(ctrl_crv.get_name(),
                            hierarchy.eyelid_ctrlzone_LD_grp.get_group_name())

                for loc_id in loc_id_list:
                    loc_name = ctrl_crv.get_locator_info(locator_id=loc_id)[0]
                    if 'A' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.eyelid_ctrlzone_loc_LD_A_grp.get_group_name())
                    elif 'B' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.eyelid_ctrlzone_loc_LD_B_grp.get_group_name())
                    elif 'C' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.eyelid_ctrlzone_loc_LD_C_grp.get_group_name())
                    elif 'D' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.eyelid_ctrlzone_loc_LD_D_grp.get_group_name())
                    elif 'E' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.eyelid_ctrlzone_loc_LD_E_grp.get_group_name())

            self._ctrl_crv_dict[crv_id] = ctrl_crv

        cmds.select(deselect=True)

        # Create the curves serving as blend-shape targets for the control curves.
        zone_LR = 'right'
        zone_UD = 'up'

        if controlZoneDirEnum.left in direction:
            zone_LR = 'left'
        if controlZoneDirEnum.down in direction:
            zone_UD = 'down'

        ctrlcrv_bs_data = self._ctrl_crv_data['eyelid_control_curve_bs']
        ctrlcrv_bs_degree = ctrlcrv_bs_data['degree']

        for ctrl_crv_bs_dir in G_CTRLCRV_BS_DIR_LIST:
            if 'original' in ctrl_crv_bs_dir or 'front' in ctrl_crv_bs_dir:
                continue

            dir_ctrlcrv_bs_data = ctrlcrv_bs_data[zone_LR+'_'+ctrl_crv_bs_dir]

            bs_nurbs_crv = cmds.curve(degree=ctrlcrv_bs_degree,
                                      point=dir_ctrlcrv_bs_data['points'])
            cmds.xform(bs_nurbs_crv, translation=dir_ctrlcrv_bs_data['xform']['translation'])
            bs_nurbs_crv = cmds.rename(bs_nurbs_crv,
                                       self._ctrl_crv_data['mouth_ctrlzone_prefix'] + '_' +
                                       zone_LR[0].upper() + zone_UD[0].upper() + '_' + dir_ctrlcrv_bs_data['name'])

            cmds.setAttr(bs_nurbs_crv + '.overrideEnabled', True)
            if controlZoneDirEnum.left in direction:
                cmds.setAttr(bs_nurbs_crv + '.overrideColor', COLOR_INDEX_DARK_RED)
            elif controlZoneDirEnum.right in direction:
                cmds.setAttr(bs_nurbs_crv + '.overrideColor', COLOR_INDEX_INDIGO)

            cmds.toggle(bs_nurbs_crv, controlVertex=True)
            cmds.select(deselect=True)

            if controlZoneDirEnum.right in direction:
                cmds.parent(bs_nurbs_crv,
                            hierarchy.eyelid_ctrlcrv_bs_R_grp.get_group_name())
            elif controlZoneDirEnum.left in direction:
                cmds.parent(bs_nurbs_crv,
                            hierarchy.eyelid_ctrlcrv_bs_L_grp.get_group_name())

            self._ctrl_crv_bs_dict[ctrl_crv_bs_dir] = bs_nurbs_crv

        # Create the control curve follow controllers.
        follow_ctrl_data = self._ctrl_crv_data['eyelid_follow_controller']
        follow_ctrl_dir = ''
        if controlZoneDirEnum.right in direction:
            follow_ctrl_dir = 'R'
        elif controlZoneDirEnum.left in direction:
            follow_ctrl_dir = 'L'

        follow_ctrl = follow_ctrl_data[follow_ctrl_dir]['name']

        # If the follow controller has not been created, make one.
        if not cmds.objExists(follow_ctrl):

            follow_ctrl_crv = cmds.curve(degree=follow_ctrl_data['degree'],
                                         point=follow_ctrl_data['points'])

            cmds.xform(follow_ctrl_crv,
                       translation=follow_ctrl_data[follow_ctrl_dir]['xform']['translation'],
                       scale=follow_ctrl_data[follow_ctrl_dir]['xform']['scale'])

            follow_ctrl_crv = cmds.rename(follow_ctrl_crv, follow_ctrl_data[follow_ctrl_dir]['name'])

            follow_data_list = follow_ctrl_data['follow_data']
            for follow_attr, val in follow_data_list.items():
                cmds.addAttr(follow_ctrl, longName=follow_attr, attributeType='float',
                             defaultValue=val, minValue=0.0, maxValue=1.0, keyable=True)

            cmds.setAttr(follow_ctrl + '.overrideEnabled', True)
            cmds.setAttr(follow_ctrl + '.overrideColor', CONTROL_M_COLOR)

            cmds.parent(follow_ctrl, hierarchy.eyelid_grp.get_group_name())

            cmds.select(deselect=True)

        self._follow_ctrl = follow_ctrl

        # Create the controllers.
        controller_data = self._ctrl_crv_data['eyelid_controller']
        controller_degree = controller_data['degree']
        controller_color = 0
        controller_points = []

        if controlZoneDirEnum.up in direction:
            controller_points = controller_data['points_up']

            if controlZoneDirEnum.right in direction:
                controller_color = CONTROLLER_RU_COLOR
            elif controlZoneDirEnum.left in direction:
                controller_color = CONTROLLER_LU_COLOR

        elif controlZoneDirEnum.down in direction:
            controller_points = controller_data['points_dn']

            if controlZoneDirEnum.right in direction:
                controller_color = CONTROLLER_RD_COLOR
            elif controlZoneDirEnum.left in direction:
                controller_color = CONTROLLER_LD_COLOR

        for ctrl_id in controller_id_list:
            dir_ctrl_data = controller_data[direction + '_' + ctrl_id]
            rig_controller = controller(name = self._ctrl_crv_data['eyelid_ctrlzone_prefix'] + '_' +
                                               dir_ctrl_data['name'],
                                        degree = controller_degree,
                                        color = controller_color,
                                        points = controller_points,
                                        translation_ofs = dir_ctrl_data['xform']['translation_ofs'],
                                        translation = dir_ctrl_data['xform']['translation'],
                                        lock_trans_axes = controller_data['lock_trans_axes'],
                                        lock_rot_axes = controller_data['lock_rot_axes'])
                                        # bind_joint_data = controller_data['bind_joint']
                                        # bind_joint_color = BIND_JOINT_LRUD_COLOR_INDEX)

            if controlZoneDirEnum.right in direction and controlZoneDirEnum.up in direction:
                cmds.parent(rig_controller.get_offset_group(),
                            hierarchy.eyelid_ctrl_RU_grp.get_group_name(),
                            relative=True)
            elif controlZoneDirEnum.right in direction and controlZoneDirEnum.down in direction:
                cmds.parent(rig_controller.get_offset_group(),
                            hierarchy.eyelid_ctrl_RD_grp.get_group_name(),
                            relative=True)
            elif controlZoneDirEnum.left in direction and controlZoneDirEnum.up:
                cmds.parent(rig_controller.get_offset_group(),
                            hierarchy.eyelid_ctrl_LU_grp.get_group_name(),
                            relative=True)
            elif controlZoneDirEnum.left in direction and controlZoneDirEnum.down in direction:
                cmds.parent(rig_controller.get_offset_group(),
                            hierarchy.eyelid_ctrl_LD_grp.get_group_name(),
                            relative=True)

            self._controller_dict[ctrl_id] = rig_controller

        # Drive the eyelid corner controllers by their adjacent ones.
        corner_driving_R_controller = self._controller_dict['B'].get_name()
        corner_R_controller = self._controller_dict['A'].get_name()

        cmds.addAttr(corner_driving_R_controller, longName='eyecorner_x_follow', attributeType='float',
                     defaultValue=0.25, minValue=0.0, maxValue=1.0, keyable=True)
        cmds.addAttr(corner_driving_R_controller, longName='eyecorner_y_follow', attributeType='float',
                     defaultValue=0.25, minValue=0.0, maxValue=1.0, keyable=True)

        corner_R_trans_multi_node = cmds.createNode('multiplyDivide', name=corner_R_controller+'_follow_multiplyDivide')

        cmds.connectAttr(corner_driving_R_controller+'.translateX', corner_R_trans_multi_node+'.input1X')
        cmds.connectAttr(corner_driving_R_controller+'.eyecorner_x_follow', corner_R_trans_multi_node+'.input2X')
        cmds.connectAttr(corner_driving_R_controller+'.translateY', corner_R_trans_multi_node+'.input1Y')
        cmds.connectAttr(corner_driving_R_controller+'.eyecorner_y_follow', corner_R_trans_multi_node+'.input2Y')
        cmds.connectAttr(corner_R_trans_multi_node+'.outputX', corner_R_controller+'.translateX')
        cmds.connectAttr(corner_R_trans_multi_node+'.outputY', corner_R_controller+'.translateY')

        corner_driving_L_controller = self._controller_dict['D'].get_name()
        corner_L_controller = self._controller_dict['E'].get_name()

        cmds.addAttr(corner_driving_L_controller, longName='eyecorner_x_follow', attributeType='float',
                     defaultValue=0.25, minValue=0.0, maxValue=1.0, keyable=True)
        cmds.addAttr(corner_driving_L_controller, longName='eyecorner_y_follow', attributeType='float',
                     defaultValue=0.25, minValue=0.0, maxValue=1.0, keyable=True)

        corner_L_trans_multi_node = cmds.createNode('multiplyDivide', name=corner_L_controller+'_follow_multiplyDivide')

        cmds.connectAttr(corner_driving_L_controller+'.translateX', corner_L_trans_multi_node+'.input1X')
        cmds.connectAttr(corner_driving_L_controller+'.eyecorner_x_follow', corner_L_trans_multi_node+'.input2X')
        cmds.connectAttr(corner_driving_L_controller+'.translateY', corner_L_trans_multi_node+'.input1Y')
        cmds.connectAttr(corner_driving_L_controller+'.eyecorner_y_follow', corner_L_trans_multi_node+'.input2Y')
        cmds.connectAttr(corner_L_trans_multi_node+'.outputX', corner_L_controller+'.translateX')
        cmds.connectAttr(corner_L_trans_multi_node+'.outputY', corner_L_controller+'.translateY')

        # # ----------------------------------------------------------------------------------------------------------
        # # Bind the control curves to the corresponding controllers' joints.

        # cmds.select(deselect=True)
        # for ctrl_id, ctrl in self._controller_dict.items():
        #     ctrl_bind_jnt = ctrl.get_bind_joint()
        #     cmds.select(ctrl_bind_jnt, add=True)
        # cmds.select(self._ctrl_crv_dict[ctrl_crv_id_list[0]].get_name(), add=True)
        #
        # skincluster_node = cmds.skinCluster(toSelectedBones=True)
        # cmds.rename(skincluster_node, self._ctrl_crv_dict[ctrl_crv_id_list[0]].get_name() + '_skinCluster')

        # --------------------------------------------------------------------------------------------------------------
        # Drive the control curves using blend-shape and
        # five-curves each in the LR and UD directions, as the targets.

        ctrl_crv_bs = cmds.blendShape(self._ctrl_crv_bs_dict['right_end_up'],
                                      self._ctrl_crv_bs_dict['right_side_up'],
                                      self._ctrl_crv_bs_dict['middle_side_up'],
                                      self._ctrl_crv_bs_dict['left_side_up'],
                                      self._ctrl_crv_bs_dict['left_end_up'],

                                      self._ctrl_crv_bs_dict['right_end_left'],
                                      self._ctrl_crv_bs_dict['right_side_left'],
                                      self._ctrl_crv_bs_dict['middle_side_left'],
                                      self._ctrl_crv_bs_dict['left_side_left'],
                                      self._ctrl_crv_bs_dict['left_end_left'],

                                      self._ctrl_crv_dict['A'].get_name(),
                                      name = self._ctrl_crv_dict['A'].get_name() + '_blendShape'
                                      )[0]
        cmds.setAttr(ctrl_crv_bs + '.supportNegativeWeights', True)

        cmds.connectAttr(self._controller_dict['A'].get_name() + '.translateX',
                         ctrl_crv_bs + '.' + self._ctrl_crv_bs_dict['right_end_left'])
        cmds.connectAttr(self._controller_dict['A'].get_name() + '.translateY',
                         ctrl_crv_bs + '.' + self._ctrl_crv_bs_dict['right_end_up'])

        cmds.connectAttr(self._controller_dict['B'].get_name() + '.translateX',
                         ctrl_crv_bs + '.' + self._ctrl_crv_bs_dict['right_side_left'])
        cmds.connectAttr(self._controller_dict['B'].get_name() + '.translateY',
                         ctrl_crv_bs + '.' + self._ctrl_crv_bs_dict['right_side_up'])

        cmds.connectAttr(self._controller_dict['C'].get_name() + '.translateX',
                         ctrl_crv_bs + '.' + self._ctrl_crv_bs_dict['middle_side_left'])
        cmds.connectAttr(self._controller_dict['C'].get_name() + '.translateY',
                         ctrl_crv_bs + '.' + self._ctrl_crv_bs_dict['middle_side_up'])

        cmds.connectAttr(self._controller_dict['D'].get_name() + '.translateX',
                         ctrl_crv_bs + '.' + self._ctrl_crv_bs_dict['left_side_left'])
        cmds.connectAttr(self._controller_dict['D'].get_name() + '.translateY',
                         ctrl_crv_bs + '.' + self._ctrl_crv_bs_dict['left_side_up'])

        cmds.connectAttr(self._controller_dict['E'].get_name() + '.translateX',
                         ctrl_crv_bs + '.' + self._ctrl_crv_bs_dict['left_end_left'])
        cmds.connectAttr(self._controller_dict['E'].get_name() + '.translateY',
                         ctrl_crv_bs + '.' + self._ctrl_crv_bs_dict['left_end_up'])

        # Create blend-shapes to control curves to transit the translations of controllers.

        cmds.select(deselect=True)
        eyelid_follow_B_attr = ''
        eyelid_follow_C_attr = ''
        eyelid_follow_D_attr = ''
        eyelid_follow_E_attr = ''
        eyelid_follow_F_attr = ''

        if controlZoneDirEnum.up in direction:
            eyelid_follow_B_attr = self._follow_ctrl + '.eyelid_up_follow_b'
            eyelid_follow_C_attr = self._follow_ctrl + '.eyelid_up_follow_c'
            eyelid_follow_D_attr = self._follow_ctrl + '.eyelid_up_follow_d'
            eyelid_follow_E_attr = self._follow_ctrl + '.eyelid_up_follow_e'
            eyelid_follow_F_attr = self._follow_ctrl + '.eyelid_up_follow_f'
        elif controlZoneDirEnum.down in direction:
            eyelid_follow_B_attr = self._follow_ctrl + '.eyelid_dn_follow_b'
            eyelid_follow_C_attr = self._follow_ctrl + '.eyelid_dn_follow_c'
            eyelid_follow_D_attr = self._follow_ctrl + '.eyelid_dn_follow_d'
            eyelid_follow_E_attr = self._follow_ctrl + '.eyelid_dn_follow_e'
            eyelid_follow_F_attr = self._follow_ctrl + '.eyelid_dn_follow_f'

        for ctrl_crv_id in ctrl_crv_id_list[1:]:
            ctrl_crv = self._ctrl_crv_dict[ctrl_crv_id]

            follow_attr = ''
            follow_val = 0.0

            if 'B' in ctrl_crv_id:
                follow_attr = eyelid_follow_B_attr
            elif 'C' in ctrl_crv_id:
                follow_attr = eyelid_follow_C_attr
            elif 'D' in ctrl_crv_id:
                follow_attr = eyelid_follow_D_attr
            elif 'E' in ctrl_crv_id:
                follow_attr = eyelid_follow_E_attr
            elif 'F' in ctrl_crv_id:
                follow_attr = eyelid_follow_F_attr

            assert cmds.objExists(follow_attr)
            follow_val = cmds.getAttr(follow_attr)
            bs_node = cmds.blendShape(self._ctrl_crv_dict[ctrl_crv_id_list[0]].get_name(),
                                      ctrl_crv.get_name(),
                                      weight=[0, follow_val])
            bs_node = cmds.rename(bs_node, ctrl_crv.get_name() + '_bs')

            cmds.connectAttr(follow_attr, bs_node + '.weight[0]')

        # Use "closestPointOnSurface" nodes to establish the projecting relationships between
        # the locators on the control curves and the locators on the projection surface.

        for ctrl_crv_id in ctrl_crv_id_list:
            ctrl_crv = self._ctrl_crv_dict[ctrl_crv_id]

            for loc_id in ctrl_crv.get_locator_ids():
                ctrlcrv_loc_info = ctrl_crv.get_locator_info(loc_id)
                projsrf_loc_info = self._ctrlproj_projsurface_LRUD.get_locator_info(ctrl_crv_id, loc_id)

                cls_pt_on_transplane_node = cmds.createNode('closestPointOnSurface')
                cls_pt_on_transplane_node = cmds.rename(cls_pt_on_transplane_node, ctrlcrv_loc_info[0] + '_clsPtOnSrf')

                cmds.connectAttr(self._ctrlproj_transplane_LRUD.get_name() + '.worldSpace[0]',
                                 cls_pt_on_transplane_node + '.inputSurface')
                cmds.connectAttr(ctrlcrv_loc_info[0] + 'Shape.worldPosition[0]',
                                 cls_pt_on_transplane_node + '.inPosition')

                pt_on_projsrf_node = projsrf_loc_info[2]
                assert cmds.objExists(pt_on_projsrf_node)

                cmds.connectAttr(cls_pt_on_transplane_node + '.parameterU', pt_on_projsrf_node + '.parameterU')
                cmds.connectAttr(cls_pt_on_transplane_node + '.parameterV', pt_on_projsrf_node + '.parameterV')