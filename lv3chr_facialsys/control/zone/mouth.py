#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# File Name: control.zone.mouth.py
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
                 direction=controlZoneDirEnum.middle+'_'+controlZoneDirEnum.up,
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

        zone_UD_abbr = 'up'
        ctrl_crv_id_list = []
        if controlZoneDirEnum.up in direction:
            ctrl_crv_id_list = ['A', 'B', 'C']
        elif controlZoneDirEnum.down in direction:
            ctrl_crv_id_list = ['A', 'B', 'C', 'D']
            zone_UD_abbr = 'dn'

        controller_dir_list = ['R', 'M', 'L']

        # Create the control curves
        ctrlcrv_data = self._ctrl_crv_data['mouth_control_curve']
        ctrlcrv_degree = ctrlcrv_data['degree']

        for crv_id in ctrl_crv_id_list:
            dir_ctrlcrv_data = ctrlcrv_data[direction+'_'+crv_id]
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

                    if 'A' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.mouth_ctrlzone_loc_MU_A_grp.get_group_name())
                    elif 'B' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.mouth_ctrlzone_loc_MU_B_grp.get_group_name())
                    elif 'C' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.mouth_ctrlzone_loc_MU_C_grp.get_group_name())

            elif controlZoneDirEnum.down in direction:
                cmds.parent(ctrl_crv.get_name(),
                            hierarchy.mouth_ctrlzone_MD_grp.get_group_name())

                for loc_id in loc_id_list:
                    loc_name = ctrl_crv.get_locator_info(locator_id=loc_id)[0]

                    if 'A' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.mouth_ctrlzone_loc_MD_A_grp.get_group_name())
                    elif 'B' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.mouth_ctrlzone_loc_MD_B_grp.get_group_name())
                    elif 'C' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.mouth_ctrlzone_loc_MD_C_grp.get_group_name())
                    elif 'D' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.mouth_ctrlzone_loc_MD_D_grp.get_group_name())

            self._ctrl_crv_dict[crv_id] = ctrl_crv

        cmds.select(deselect=True)

        # Create the curves serving as blend-shape targets for the control curves.
        ctrl_crv_id_list = []
        if controlZoneDirEnum.up in direction:
            ctrl_crv_id_list = ['A', 'B', 'C']
        elif controlZoneDirEnum.down in direction:
            ctrl_crv_id_list = ['A', 'B', 'C', 'D']

        ctrlcrv_bs_data = self._ctrl_crv_data['mouth_control_curve_bs']
        ctrlcrv_bs_degree = ctrlcrv_bs_data['degree']

        for ctrl_crv_bs_dir in G_CTRLCRV_BS_DIR_LIST:
            dir_ctrlcrv_bs_data = None
            if 'original' == ctrl_crv_bs_dir:
                for ctrl_crv_id in ctrl_crv_id_list:
                    dir_ctrlcrv_bs_data = ctrlcrv_bs_data[zone_UD_abbr+'_original_'+ctrl_crv_id]

                    self.generate_curve_bs_target(zone_dir = direction,
                                                  bs_dir = ctrl_crv_bs_dir,
                                                  bs_degree = ctrlcrv_bs_degree,
                                                  bs_data = dir_ctrlcrv_bs_data,
                                                  crv_id = ctrl_crv_id)
            elif 'end' in ctrl_crv_bs_dir:
                continue
            else:
                if 'front' not in ctrl_crv_bs_dir:
                    for ctrl_crv_id in ctrl_crv_id_list:
                        dir_ctrlcrv_bs_data = ctrlcrv_bs_data[zone_UD_abbr+'_'+ctrl_crv_bs_dir+'_'+ctrl_crv_id]

                        self.generate_curve_bs_target(zone_dir = direction,
                                                      bs_dir = ctrl_crv_bs_dir,
                                                      bs_degree = ctrlcrv_bs_degree,
                                                      bs_data = dir_ctrlcrv_bs_data,
                                                      crv_id = ctrl_crv_id)
                # else:
                #     dir_ctrlcrv_bs_data = ctrlcrv_bs_data[ctrl_crv_bs_dir]
                #
                #     self.generate_curve_bs_target(zone_dir = direction,
                #                                   bs_dir = ctrl_crv_bs_dir,
                #                                   bs_degree = ctrlcrv_bs_degree,
                #                                   bs_data = dir_ctrlcrv_bs_data)

        # Create the control curve follow controllers.
        follow_ctrl_data = self._ctrl_crv_data['mouth_follow_controller']
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

            cmds.setAttr(follow_ctrl+'.overrideEnabled', True)
            cmds.setAttr(follow_ctrl+'.overrideColor', CONTROL_M_COLOR)

            cmds.parent(follow_ctrl, hierarchy.mouth_grp.get_group_name())
            cmds.select(deselect=True)

        self._follow_ctrl = follow_ctrl

        # Create the controllers
        controller_data = self._ctrl_crv_data['mouth_controller']
        controller_degree = controller_data['degree']
        direction_UD = direction.split('_')[1]
        controller_points = []
        controller_color = 0

        for ctrl_dir in controller_dir_list:
            if 'R' == ctrl_dir:
                controller_points = controller_data['points_right_'+direction_UD]
                direction = 'right_'+direction_UD
                controller_color = CONTROL_R_COLOR
            elif 'M' == ctrl_dir:
                controller_points = controller_data['points_middle_'+direction_UD]
                direction = 'middle_'+direction_UD
                controller_color = CONTROL_M_COLOR
            elif 'L' == ctrl_dir:
                controller_points = controller_data['points_left_'+direction_UD]
                direction = 'left_'+direction_UD
                controller_color = CONTROL_L_COLOR

            dir_ctrl_data = controller_data[direction]
            rig_controller = controller(name = self._ctrl_crv_data['mouth_ctrlzone_prefix']+'_'+
                                             dir_ctrl_data['name'],
                                        degree = controller_degree,
                                        color = controller_color,
                                        points = controller_points,
                                        translation_ofs = dir_ctrl_data['xform']['translation_ofs'],
                                        translation = dir_ctrl_data['xform']['translation'],
                                        lock_trans_axes = controller_data['lock_trans_axes'],
                                        lock_rot_axes = controller_data['lock_rot_axes'])
                                        # bind_joint_data = controller_data['bind_joint'],
                                        # bind_joint_color = BIND_JOINT_LRUD_COLOR_INDEX)

            if controlZoneDirEnum.up in direction:
                cmds.parent(rig_controller.get_offset_group(),
                            hierarchy.mouth_ctrl_MU_grp.get_group_name())
            elif controlZoneDirEnum.down in direction:
                cmds.parent(rig_controller.get_offset_group(),
                            hierarchy.mouth_ctrl_MD_grp.get_group_name())

            self._controller_dict[ctrl_dir] = rig_controller

        # --------------------------------------------------------------------------------------------------------------
        # Drive the control curves using blend-shape and
        # three-curves each in the LR, UD and FB directions, as the targets.

        lip_up_follow_B_attr = self._follow_ctrl+'.lip_up_follow_b'
        lip_up_follow_C_attr = self._follow_ctrl+'.lip_up_follow_c'
        lip_dn_follow_B_attr = self._follow_ctrl+'.lip_dn_follow_b'
        lip_dn_follow_C_attr = self._follow_ctrl+'.lip_dn_follow_c'
        lip_dn_follow_D_attr = self._follow_ctrl+'.lip_dn_follow_d'

        for ctrl_crv_id in ctrl_crv_id_list:
            lip_follow_attr = ''
            lip_follow_multi_node = None

            if controlZoneDirEnum.up in direction:
                if 'B' == ctrl_crv_id:
                    lip_follow_attr = lip_up_follow_B_attr
                elif 'C' == ctrl_crv_id:
                    lip_follow_attr = lip_up_follow_C_attr
            elif controlZoneDirEnum.down in direction:
                if 'B' == ctrl_crv_id:
                    lip_follow_attr = lip_dn_follow_B_attr
                elif 'C' == ctrl_crv_id:
                    lip_follow_attr = lip_dn_follow_C_attr
                elif 'D' == ctrl_crv_id:
                    lip_follow_attr = lip_dn_follow_D_attr

            if '' != lip_follow_attr:
                assert cmds.objExists(lip_follow_attr)

                lip_follow_multi_node = cmds.createNode('multiplyDivide',
                                                        name=lip_follow_attr.split('.')[1]+'_multiplyDivide')
                cmds.connectAttr(self._controller_dict['M'].get_name()+'.translateY', lip_follow_multi_node+'.input1Y')
                cmds.connectAttr(lip_follow_attr, lip_follow_multi_node+'.input2Y')

            ctrl_crv_bs = None
            if 'A' == ctrl_crv_id:
                ctrl_crv_bs = cmds.blendShape(self._ctrl_crv_bs_dict[zone_UD_abbr+'_original_'+ctrl_crv_id],
                                self._ctrl_crv_bs_dict[zone_UD_abbr+'_right_side_up_'+ctrl_crv_id],
                                self._ctrl_crv_bs_dict[zone_UD_abbr+'_middle_side_up_'+ctrl_crv_id],
                                self._ctrl_crv_bs_dict[zone_UD_abbr+'_left_side_up_'+ctrl_crv_id],
                                self._ctrl_crv_bs_dict[zone_UD_abbr+'_right_side_left_'+ctrl_crv_id],
                                self._ctrl_crv_bs_dict[zone_UD_abbr+'_middle_side_left_'+ctrl_crv_id],
                                self._ctrl_crv_bs_dict[zone_UD_abbr+'_left_side_left_'+ctrl_crv_id],
                                # self._ctrl_crv_bs_dict['right_side_front'],
                                # self._ctrl_crv_bs_dict['middle_side_front'],
                                # self._ctrl_crv_bs_dict['left_side_front'],
                                self._ctrl_crv_dict[ctrl_crv_id].get_name(),
                                name = self._ctrl_crv_dict[ctrl_crv_id].get_name()+'_blendShape')[0]
            else:
                ctrl_crv_bs = cmds.blendShape(self._ctrl_crv_bs_dict[zone_UD_abbr+'_original_'+ctrl_crv_id],
                                self._ctrl_crv_bs_dict[zone_UD_abbr+'_right_side_up_'+ctrl_crv_id],
                                self._ctrl_crv_bs_dict[zone_UD_abbr+'_middle_side_up_'+ctrl_crv_id],
                                self._ctrl_crv_bs_dict[zone_UD_abbr+'_left_side_up_'+ctrl_crv_id],
                                self._ctrl_crv_bs_dict[zone_UD_abbr+'_right_side_left_'+ctrl_crv_id],
                                self._ctrl_crv_bs_dict[zone_UD_abbr+'_middle_side_left_'+ctrl_crv_id],
                                self._ctrl_crv_bs_dict[zone_UD_abbr+'_left_side_left_'+ctrl_crv_id],
                                self._ctrl_crv_dict[ctrl_crv_id].get_name(),
                                name = self._ctrl_crv_dict[ctrl_crv_id].get_name()+'_blendShape')[0]
            cmds.setAttr(ctrl_crv_bs+'.'+self._ctrl_crv_bs_dict[zone_UD_abbr+'_original_'+ctrl_crv_id], 1)
            cmds.setAttr(ctrl_crv_bs+'.supportNegativeWeights', True)

            # Right-Side Mouth Corner Controller
            cmds.connectAttr(self._controller_dict['R'].get_name()+'.translateX',
                             ctrl_crv_bs+'.'+self._ctrl_crv_bs_dict[zone_UD_abbr+'_right_side_left_'+ctrl_crv_id])


            cmds.connectAttr(self._controller_dict['R'].get_name()+'.translateY',
                             ctrl_crv_bs+'.'+self._ctrl_crv_bs_dict[zone_UD_abbr+'_right_side_up_'+ctrl_crv_id])

            # if 'A' == ctrl_crv_id:
            #     cmds.connectAttr(self._controller_dict['R'].get_name()+'.translateZ',
            #                      ctrl_crv_bs+'.'+self._ctrl_crv_bs_dict['right_side_front'])

            # Middle-Side Mouth Controller
            cmds.connectAttr(self._controller_dict['M'].get_name()+'.translateX',
                             ctrl_crv_bs+'.'+self._ctrl_crv_bs_dict[zone_UD_abbr+'_middle_side_left_'+ctrl_crv_id])

            if '' != lip_follow_attr:
                cmds.connectAttr(lip_follow_multi_node+'.outputY',
                                 ctrl_crv_bs+'.'+self._ctrl_crv_bs_dict[zone_UD_abbr+'_middle_side_up_'+ctrl_crv_id])
            else:
                cmds.connectAttr(self._controller_dict['M'].get_name()+'.translateY',
                                 ctrl_crv_bs+'.'+self._ctrl_crv_bs_dict[zone_UD_abbr+'_middle_side_up_'+ctrl_crv_id])

            # if 'A' == ctrl_crv_id:
            #     cmds.connectAttr(self._controller_dict['M'].get_name()+'.translateZ',
            #                      ctrl_crv_bs+'.'+self._ctrl_crv_bs_dict['middle_side_front'])


            # Left-Side Mouth Corner Controller
            cmds.connectAttr(self._controller_dict['L'].get_name()+'.translateX',
                             ctrl_crv_bs+'.'+self._ctrl_crv_bs_dict[zone_UD_abbr+'_left_side_left_'+ctrl_crv_id])

            cmds.connectAttr(self._controller_dict['L'].get_name()+'.translateY',
                             ctrl_crv_bs+'.'+self._ctrl_crv_bs_dict[zone_UD_abbr+'_left_side_up_'+ctrl_crv_id])

            # if 'A' == ctrl_crv_id:
            #     cmds.connectAttr(self._controller_dict['L'].get_name()+'.translateZ',
            #                      ctrl_crv_bs+'.'+self._ctrl_crv_bs_dict['left_side_front'])

        # Use "closestPointOnSurface" nodes to establish the projecting relationships between
        # the locators on the control curves and the locators on the projection surfaces.

        if controlZoneDirEnum.up in direction:
            ctrl_crv_id_list = ['A', 'B', 'C']
        elif controlZoneDirEnum.down in direction:
            ctrl_crv_id_list = ['A', 'B', 'C', 'D']

        for ctrl_crv_id in ctrl_crv_id_list:
            ctrl_crv = self._ctrl_crv_dict[ctrl_crv_id]

            for loc_id in ctrl_crv.get_locator_ids():
                ctrlcrv_loc_info = ctrl_crv.get_locator_info(loc_id)
                projsrf_loc_info = self._ctrlproj_projsurface_LRUD.get_locator_info(ctrl_crv_id, loc_id)

                cls_pt_on_transplane_node = cmds.createNode('closestPointOnSurface')
                cls_pt_on_transplane_node = cmds.rename(cls_pt_on_transplane_node, ctrlcrv_loc_info[0]+'_clsPtOnSrf')

                cmds.connectAttr(self._ctrlproj_transplane_LRUD.get_name()+'.worldSpace[0]',
                                 cls_pt_on_transplane_node+'.inputSurface')
                cmds.connectAttr(ctrlcrv_loc_info[0]+'Shape.worldPosition[0]',
                                 cls_pt_on_transplane_node+'.inPosition')

                pt_on_projsrf_node = projsrf_loc_info[2]
                assert cmds.objExists(pt_on_projsrf_node)

                cmds.connectAttr(cls_pt_on_transplane_node+'.parameterU', pt_on_projsrf_node+'.parameterU')
                cmds.connectAttr(cls_pt_on_transplane_node+'.parameterV', pt_on_projsrf_node+'.parameterV')


    def generate_curve_bs_target(self, zone_dir, bs_dir, bs_degree, bs_data, crv_id=''):
        bs_nurbs_crv = cmds.curve(degree=bs_degree,
                                  point=bs_data['points'])
        cmds.xform(bs_nurbs_crv, translation=bs_data['xform']['translation'])
        direction_abbr = 'MU'
        if controlZoneDirEnum.down in zone_dir:
            direction_abbr = 'MD'
        bs_nurbs_crv = cmds.rename(bs_nurbs_crv,
                                   self._ctrl_crv_data['mouth_ctrlzone_prefix']+'_'+
                                   direction_abbr+'_'+bs_data['name'])

        cmds.setAttr(bs_nurbs_crv+'.overrideEnabled', True)
        if 'middle' in bs_dir or 'orig' in bs_dir:
            cmds.setAttr(bs_nurbs_crv+'.overrideColor', COLOR_INDEX_OLIVE)
        elif 'right' in bs_dir: # right-side blend-shape targets' names also include the to 'left' movement direction,
                                # so we test the 'right' word including condition first.
            cmds.setAttr(bs_nurbs_crv+'.overrideColor', COLOR_INDEX_INDIGO)
        elif 'left' in bs_dir:
            cmds.setAttr(bs_nurbs_crv+'.overrideColor', COLOR_INDEX_DARK_RED)

        cmds.toggle(bs_nurbs_crv, controlVertex=True)
        cmds.select(deselect=True)

        zone_dir_abbr = 'up'
        if controlZoneDirEnum.up in zone_dir:
            cmds.parent(bs_nurbs_crv,
                        hierarchy.mouth_ctrlcrv_bs_MU_grp.get_group_name())
        elif controlZoneDirEnum.down in zone_dir:
            zone_dir_abbr = 'dn'
            cmds.parent(bs_nurbs_crv,
                        hierarchy.mouth_ctrlcrv_bs_MD_grp.get_group_name())

        if 'front' in bs_dir:
            self._ctrl_crv_bs_dict[bs_dir] = bs_nurbs_crv
        else:
            self._ctrl_crv_bs_dict[zone_dir_abbr+'_'+bs_dir+'_'+crv_id] = bs_nurbs_crv