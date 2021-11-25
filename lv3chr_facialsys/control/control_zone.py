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

from general import lv3chr_facialsys_config; reload(lv3chr_facialsys_config)
from general.lv3chr_facialsys_config import *

from general import lv3chr_facialsys_hierarchy; reload(lv3chr_facialsys_hierarchy)

import control_curve; reload(control_curve)
from control_curve import controlCurve

import controller; reload( controller)
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
                 direction = controlZoneDirEnum.right_up,
                 ctrl_crv_data = None,
                 ctrlproj_transplane = None,
                 ctrlproj_projsurface = None
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
            'A': None,
        }

        # The keys of this dictionary are follow controller's IDs.
        self._follow_ctrl = None

        # The keys of this dictionary are controllers' IDs.
        self._controller_dict = {
            'A': None,
        }

        self._ctrlproj_transplane = None
        self._ctrlproj_projsurface = None
        # ---------------------------------------------------------------------------------- Member Variable Definitions

        assert None != ctrl_crv_data
        assert None != ctrlproj_transplane
        assert None != ctrlproj_projsurface

        self._ctrlproj_transplane = ctrlproj_transplane
        self._ctrlproj_projsurface = ctrlproj_projsurface

        ctrlcrv_data = {}
        ctrlcrv_degree = 1

        # Eyelid Zone
        if controlZoneEnum.eyelid == zone:
            ctrl_crv_id_list = ['A', 'B', 'C', 'D']
            controller_id_list = ['A', 'B', 'C', 'D', 'E']

            # Create the control curves.
            eyelid_ctrlcrv_data = ctrl_crv_data['eyelid_control_curve']
            eyelid_ctrlcrv_degree = eyelid_ctrlcrv_data['degree']

            for crv_id in ctrl_crv_id_list:
                eyelid_dir_ctrlcrv_data = eyelid_ctrlcrv_data[direction + '_' + crv_id]
                eyelid_ctrl_crv = controlCurve(name_prefix = ctrl_crv_data['eyelid_ctrlzone_prefix'],
                                               name = eyelid_dir_ctrlcrv_data['name'],
                                               degree = eyelid_ctrlcrv_degree,
                                               translation=eyelid_dir_ctrlcrv_data['xform']['translation'],
                                               points = eyelid_dir_ctrlcrv_data['points'],
                                               locator_data = eyelid_dir_ctrlcrv_data['locators'],
                                               locator_scale = eyelid_ctrlcrv_data['locator_scale'])

                loc_id_list = eyelid_ctrl_crv.get_locator_ids()

                if controlZoneDirEnum.right_up == direction:
                    cmds.parent(eyelid_ctrl_crv.get_name(),
                                lv3chr_facialsys_hierarchy.eyelid_ctrlzone_RU_grp.get_group_name())

                    for loc_id in loc_id_list:
                        loc_name = eyelid_ctrl_crv.get_locator_info(locator_id=loc_id)[0]
                        if 'A' == crv_id:
                            cmds.parent(loc_name,
                                        lv3chr_facialsys_hierarchy.eyelid_ctrlzone_loc_RU_A_grp.get_group_name())
                        elif 'B' == crv_id:
                            cmds.parent(loc_name,
                                        lv3chr_facialsys_hierarchy.eyelid_ctrlzone_loc_RU_B_grp.get_group_name())
                        elif 'C' == crv_id:
                            cmds.parent(loc_name,
                                        lv3chr_facialsys_hierarchy.eyelid_ctrlzone_loc_RU_C_grp.get_group_name())
                        elif 'D' == crv_id:
                            cmds.parent(loc_name,
                                        lv3chr_facialsys_hierarchy.eyelid_ctrlzone_loc_RU_D_grp.get_group_name())

                elif controlZoneDirEnum.right_dn == direction:
                    cmds.parent(eyelid_ctrl_crv.get_name(),
                                lv3chr_facialsys_hierarchy.eyelid_ctrlzone_RD_grp.get_group_name())

                    for loc_id in loc_id_list:
                        loc_name = eyelid_ctrl_crv.get_locator_info(locator_id=loc_id)[0]
                        if 'A' == crv_id:
                            cmds.parent(loc_name,
                                        lv3chr_facialsys_hierarchy.eyelid_ctrlzone_loc_RD_A_grp.get_group_name())
                        elif 'B' == crv_id:
                            cmds.parent(loc_name,
                                        lv3chr_facialsys_hierarchy.eyelid_ctrlzone_loc_RD_B_grp.get_group_name())
                        elif 'C' == crv_id:
                            cmds.parent(loc_name,
                                        lv3chr_facialsys_hierarchy.eyelid_ctrlzone_loc_RD_C_grp.get_group_name())
                        elif 'D' == crv_id:
                            cmds.parent(loc_name,
                                        lv3chr_facialsys_hierarchy.eyelid_ctrlzone_loc_RD_D_grp.get_group_name())

                elif controlZoneDirEnum.left_up == direction:
                    cmds.parent(eyelid_ctrl_crv.get_name(),
                                lv3chr_facialsys_hierarchy.eyelid_ctrlzone_LU_grp.get_group_name())

                    for loc_id in loc_id_list:
                        loc_name = eyelid_ctrl_crv.get_locator_info(locator_id=loc_id)[0]
                        if 'A' == crv_id:
                            cmds.parent(loc_name,
                                        lv3chr_facialsys_hierarchy.eyelid_ctrlzone_loc_LU_A_grp.get_group_name())
                        elif 'B' == crv_id:
                            cmds.parent(loc_name,
                                        lv3chr_facialsys_hierarchy.eyelid_ctrlzone_loc_LU_B_grp.get_group_name())
                        elif 'C' == crv_id:
                            cmds.parent(loc_name,
                                        lv3chr_facialsys_hierarchy.eyelid_ctrlzone_loc_LU_C_grp.get_group_name())
                        elif 'D' == crv_id:
                            cmds.parent(loc_name,
                                        lv3chr_facialsys_hierarchy.eyelid_ctrlzone_loc_LU_D_grp.get_group_name())

                elif controlZoneDirEnum.left_dn == direction:
                    cmds.parent(eyelid_ctrl_crv.get_name(),
                                lv3chr_facialsys_hierarchy.eyelid_ctrlzone_LD_grp.get_group_name())

                    for loc_id in loc_id_list:
                        loc_name = eyelid_ctrl_crv.get_locator_info(locator_id=loc_id)[0]
                        if 'A' == crv_id:
                            cmds.parent(loc_name,
                                        lv3chr_facialsys_hierarchy.eyelid_ctrlzone_loc_LD_A_grp.get_group_name())
                        elif 'B' == crv_id:
                            cmds.parent(loc_name,
                                        lv3chr_facialsys_hierarchy.eyelid_ctrlzone_loc_LD_B_grp.get_group_name())
                        elif 'C' == crv_id:
                            cmds.parent(loc_name,
                                        lv3chr_facialsys_hierarchy.eyelid_ctrlzone_loc_LD_C_grp.get_group_name())
                        elif 'D' == crv_id:
                            cmds.parent(loc_name,
                                        lv3chr_facialsys_hierarchy.eyelid_ctrlzone_loc_LD_D_grp.get_group_name())

                self._ctrl_crv_dict[crv_id] = eyelid_ctrl_crv

                cmds.select(deselect=True)

            # Create the control curve follow control locators.
            eyelid_follow_ctrl_data = ctrl_crv_data['eyelid_follow_controller']
            follow_ctrl_dir = ''
            if 'r' in direction:
                follow_ctrl_dir = 'R'
            elif 'l' in direction:
                follow_ctrl_dir = 'L'

            eyelid_follow_ctrl = eyelid_follow_ctrl_data[follow_ctrl_dir]['name']

            # If the follow controller has not been created, make one.
            if not cmds.objExists(eyelid_follow_ctrl):

                eyelid_follow_ctrl = cmds.spaceLocator(name=eyelid_follow_ctrl_data[follow_ctrl_dir]['name'])[0]
                cmds.xform(eyelid_follow_ctrl,
                           translation=eyelid_follow_ctrl_data[follow_ctrl_dir]['xform']['translation'])

                assert cmds.objExists(eyelid_follow_ctrl + 'Shape')
                for idx, axis in {0:'X', 1:'Y', 2:'Z'}.items():
                    cmds.setAttr(eyelid_follow_ctrl+'Shape.localScale'+axis,
                                 eyelid_follow_ctrl_data[follow_ctrl_dir]['xform']['scale'][idx])

                follow_data_list = eyelid_follow_ctrl_data['follow_data']
                for follow_attr, val in follow_data_list.items():
                    cmds.addAttr(eyelid_follow_ctrl, longName=follow_attr, attributeType='float',
                                 defaultValue=val, minValue=0.0, maxValue=1.0, keyable=True)

                cmds.setAttr(eyelid_follow_ctrl+'.overrideEnabled', True)
                if 'R' == follow_ctrl_dir:
                    cmds.setAttr(eyelid_follow_ctrl+'.overrideColor', CONTROLLER_RD_COLOR)
                elif 'L' == follow_ctrl_dir:
                    cmds.setAttr(eyelid_follow_ctrl+'.overrideColor', CONTROLLER_LD_COLOR)

                cmds.parent(eyelid_follow_ctrl, lv3chr_facialsys_hierarchy.eyelid_grp.get_group_name())

                cmds.select(deselect=True)

            self._follow_ctrl = eyelid_follow_ctrl

            # Create the controllers.
            eyelid_controller_data = ctrl_crv_data['eyelid_controller']
            eyelid_controller_degree = eyelid_controller_data['degree']
            eyelid_controller_color = 0
            eyelid_controller_points = []

            if 'u' in direction:
                eyelid_controller_points = eyelid_controller_data['points_up']

                if 'r' in direction:
                    eyelid_controller_color = CONTROLLER_RU_COLOR
                elif 'l' in direction:
                    eyelid_controller_color = CONTROLLER_LU_COLOR

            elif 'd' in direction:
                eyelid_controller_points = eyelid_controller_data['points_dn']

                if 'r' in direction:
                    eyelid_controller_color = CONTROLLER_RD_COLOR
                elif 'l' in direction:
                    eyelid_controller_color = CONTROLLER_LD_COLOR

            for ctrl_id in controller_id_list:
                eyelid_dir_ctrl_data = eyelid_controller_data[direction+'_'+ctrl_id]
                eyelid_controller = controller(name = ctrl_crv_data['eyelid_ctrlzone_prefix'] + '_' +
                                                      eyelid_dir_ctrl_data['name'],
                                               degree = eyelid_controller_degree,
                                               color = eyelid_controller_color,
                                               points = eyelid_controller_points,
                                               translation_ofs = eyelid_dir_ctrl_data['xform']['translation_ofs'],
                                               translation = eyelid_dir_ctrl_data['xform']['translation'],
                                               bind_joint_data = eyelid_controller_data['bind_joint'],
                                               bind_joint_color = BIND_JOINT_COLOR_INDEX)

                if controlZoneDirEnum.right_up == direction:
                    cmds.parent(eyelid_controller.get_offset_group(),
                                lv3chr_facialsys_hierarchy.eyelid_ctrl_RU_grp.get_group_name(),
                                relative=True)
                elif controlZoneDirEnum.right_dn == direction:
                    cmds.parent(eyelid_controller.get_offset_group(),
                                lv3chr_facialsys_hierarchy.eyelid_ctrl_RD_grp.get_group_name(),
                                relative=True)
                elif controlZoneDirEnum.left_up == direction:
                    cmds.parent(eyelid_controller.get_offset_group(),
                                lv3chr_facialsys_hierarchy.eyelid_ctrl_LU_grp.get_group_name(),
                                relative=True)
                elif controlZoneDirEnum.left_dn == direction:
                    cmds.parent(eyelid_controller.get_offset_group(),
                                lv3chr_facialsys_hierarchy.eyelid_ctrl_LD_grp.get_group_name(),
                                relative=True)

                self._controller_dict[ctrl_id] = eyelid_controller

            # ----------------------------------------------------------------------------------------------------------
            # Bind the control curves to the corresponding controllers' joints.
            cmds.select(deselect=True)
            for ctrl_id, ctrl in self._controller_dict.items():
                ctrl_bind_jnt = ctrl.get_bind_joint()
                cmds.select(ctrl_bind_jnt, add=True)
            cmds.select(self._ctrl_crv_dict[ctrl_crv_id_list[0]].get_name(), add=True)

            skincluster_node = cmds.skinCluster(toSelectedBones=True)
            cmds.rename(skincluster_node, self._ctrl_crv_dict[ctrl_crv_id_list[0]].get_name()+'_skinCluster')

            # Create blendshapes to control curves to transit the translations of controllers.
            cmds.select(deselect=True)
            eyelid_follow_B_attr = ''
            eyelid_follow_C_attr = ''
            eyelid_follow_D_attr = ''

            if 'u' in direction:
                eyelid_follow_B_attr = self._follow_ctrl+'.eyelid_up_follow_b'
                eyelid_follow_C_attr = self._follow_ctrl+'.eyelid_up_follow_c'
                eyelid_follow_D_attr = self._follow_ctrl+'.eyelid_up_follow_d'
            elif 'd' in direction:
                eyelid_follow_B_attr = self._follow_ctrl+'.eyelid_dn_follow_b'
                eyelid_follow_C_attr = self._follow_ctrl+'.eyelid_dn_follow_c'
                eyelid_follow_D_attr = self._follow_ctrl+'.eyelid_dn_follow_d'

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

                assert cmds.objExists(follow_attr)
                follow_val = cmds.getAttr(follow_attr)
                bs_node = cmds.blendShape(self._ctrl_crv_dict[ctrl_crv_id_list[0]].get_name(),
                                          ctrl_crv.get_name(),
                                          weight=[0, follow_val])
                bs_node = cmds.rename(bs_node, ctrl_crv.get_name()+'_bs')

                cmds.connectAttr(follow_attr, bs_node+'.weight[0]')

            # Use "closestPointOnSurface" node to establish the projecting relationships between
            # the locators on control curves and the locators on the projection surface.

            # cmds.warning('The translationPlane of this controlZone: {}'.format(self._ctrlproj_transplane.get_name()))
            # cmds.warning('The projectionSurface of this controlZone: {}'.format(self._ctrlproj_projsurface.get_name()))

            for ctrl_crv_id in ctrl_crv_id_list:
                ctrl_crv = self._ctrl_crv_dict[ctrl_crv_id]

                for loc_id in ctrl_crv.get_locator_ids():
                    ctrl_crv_loc_info = ctrl_crv.get_locator_info(loc_id)
                    proj_srf_loc_info = self._ctrlproj_projsurface.get_locator_info(ctrl_crv_id, loc_id)

                    # cmds.warning('--------------------------------------------------------------------')
                    # cmds.warning('zone direction: {}'.format(direction))
                    # cmds.warning('control curve: {}'.format(ctrl_crv.get_name()))
                    # cmds.warning('project surface: {}'.format(self._ctrlproj_projsurface.get_name()))
                    # cmds.warning('ctrl_crv_loc_info: {}'.format(ctrl_crv_loc_info))
                    # cmds.warning('proj_srf_loc_info: {}'.format(proj_srf_loc_info))
                    # cmds.warning('--------------------------------------------------------------------')

                    cls_pt_on_srf_node = cmds.createNode('closestPointOnSurface')
                    cls_pt_on_srf_node = cmds.rename(cls_pt_on_srf_node, ctrl_crv_loc_info[0]+'_clsPtOnSrf')

                    cmds.connectAttr(self._ctrlproj_transplane.get_name()+'.worldSpace[0]',
                                     cls_pt_on_srf_node+'.inputSurface')
                    cmds.connectAttr(ctrl_crv_loc_info[0]+'Shape.worldPosition[0]',
                                     cls_pt_on_srf_node+'.inPosition')

                    pt_on_srf_node = proj_srf_loc_info[2]
                    assert cmds.objExists(pt_on_srf_node)

                    cmds.connectAttr(cls_pt_on_srf_node+'.parameterU', pt_on_srf_node+'.parameterU')
                    cmds.connectAttr(cls_pt_on_srf_node+'.parameterV', pt_on_srf_node+'.parameterV')