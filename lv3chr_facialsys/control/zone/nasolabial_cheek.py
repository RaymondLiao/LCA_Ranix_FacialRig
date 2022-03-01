#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# File Name: control.zone.nasolabial_cheek.py
# Author: Sheng (Raymond) Liao
# Date: December 2021
#

"""
A module organizing the control elements of the nasolabial and the cheek zones
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
class nasoCheekControlZone(controlZone):
    """ Subclass of the controlZone, whose instances manage the control elements of the cheek zone
    """

    def __init__(self,
                 direction=controlZoneDirEnum.right+'_'+controlZoneDirEnum.up+'_'+controlZoneDirEnum.down,
                 ctrl_crv_data = None,
                 ctrlproj_transplane_LRUD       = None,
                 ctrlproj_transplane_LRFB_list  = [],
                 ctrlproj_projsurface_LRUD      = None,
                 ctrlproj_projsurface_LRFB_list = []):
        """ A Nasolabial-Cheek Control Zone instance's direction attribute may have the value of
            "right_up_dn/RUD" or "left_up_dn/LUD".
        """

        super(nasoCheekControlZone, self).__init__(zone = controlZoneEnum.nasocheek,
                                                   direction = direction,
                                                   ctrl_crv_data                    = ctrl_crv_data,
                                                   ctrlproj_transplane_LRUD         = ctrlproj_transplane_LRUD,
                                                   ctrlproj_transplane_LRFB_list    = ctrlproj_transplane_LRFB_list,
                                                   ctrlproj_projsurface_LRUD        = ctrlproj_projsurface_LRUD,
                                                   ctrlproj_projsurface_LRFB_list   = ctrlproj_projsurface_LRFB_list)

        assert None != ctrlproj_transplane_LRUD
        assert None != ctrlproj_projsurface_LRUD
        assert None != ctrlproj_transplane_LRFB_list and \
            isinstance(ctrlproj_transplane_LRFB_list, list) and True
        assert None != ctrlproj_projsurface_LRFB_list and \
            isinstance(ctrlproj_projsurface_LRFB_list, list) and 6 == len(ctrlproj_projsurface_LRFB_list)

        ctrl_crv_id_list = ['A', 'B', 'C', 'D', 'E', 'F']

        # Create the control curves.
        ctrlcrv_data = self._ctrl_crv_data['nasocheek_control_curve']
        ctrlcrv_degree = ctrlcrv_data['degree']

        for crv_id in ctrl_crv_id_list:
            dir_ctrlcrv_data = ctrlcrv_data[direction.split('_')[0]+'_'+crv_id]
            ctrl_crv = controlCurve(name_prefix = self._ctrl_crv_data['nasocheek_ctrlzone_prefix'],
                                    name = dir_ctrlcrv_data['name'],
                                    degree = ctrlcrv_degree,
                                    translation = dir_ctrlcrv_data['xform']['translation'],
                                    points = dir_ctrlcrv_data['points'],
                                    locator_data = dir_ctrlcrv_data['locators'],
                                    locator_scale = ctrlcrv_data['locator_scale'])

            loc_id_list = ctrl_crv.get_locator_ids()

            if controlZoneDirEnum.right in direction:
                cmds.parent(ctrl_crv.get_name(),
                            hierarchy.nasocheek_ctrlzone_R_grp.get_group_name())

                for loc_id in loc_id_list:
                    loc_name = ctrl_crv.get_locator_info(locator_id=loc_id)[0]
                    if 'A' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.nasocheek_ctrlzone_loc_R_A_grp.get_group_name())
                    elif 'B' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.nasocheek_ctrlzone_loc_R_B_grp.get_group_name())
                    elif 'C' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.nasocheek_ctrlzone_loc_R_C_grp.get_group_name())
                    elif 'D' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.nasocheek_ctrlzone_loc_R_D_grp.get_group_name())
                    elif 'E' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.nasocheek_ctrlzone_loc_R_E_grp.get_group_name())
                    elif 'F' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.nasocheek_ctrlzone_loc_R_F_grp.get_group_name())

            elif controlZoneDirEnum.left in direction:
                cmds.parent(ctrl_crv.get_name(),
                            hierarchy.nasocheek_ctrlzone_L_grp.get_group_name())

                for loc_id in loc_id_list:
                    loc_name = ctrl_crv.get_locator_info(locator_id=loc_id)[0]
                    if 'A' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.nasocheek_ctrlzone_loc_L_A_grp.get_group_name())
                    elif 'B' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.nasocheek_ctrlzone_loc_L_B_grp.get_group_name())
                    elif 'C' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.nasocheek_ctrlzone_loc_L_C_grp.get_group_name())
                    elif 'D' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.nasocheek_ctrlzone_loc_L_D_grp.get_group_name())
                    elif 'E' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.nasocheek_ctrlzone_loc_L_E_grp.get_group_name())
                    elif 'F' == crv_id:
                        cmds.parent(loc_name,
                                    hierarchy.nasocheek_ctrlzone_loc_L_F_grp.get_group_name())

            self._ctrl_crv_dict[crv_id] = ctrl_crv

        # Create the curves serving as blend-shape targets for the control curves.
        ctrlcrv_bs_data = self._ctrl_crv_data['nasocheek_control_curve_bs']
        ctrlcrv_bs_degree = ctrlcrv_bs_data['degree']

        for crv_id in ctrl_crv_id_list:
            dir_ctrlcrv_bs_data = None

            for bs_type in G_BLENDSHAPE_TYPE_LIST:
                if controlZoneDirEnum.right in direction:
                    dir_ctrlcrv_bs_data = ctrlcrv_bs_data[bs_type+'_R_'+crv_id]
                else:
                    dir_ctrlcrv_bs_data = ctrlcrv_bs_data[bs_type+'_L_'+crv_id]

                bs_nurbs_crv = cmds.curve(degree=ctrlcrv_bs_degree,
                                          point=dir_ctrlcrv_bs_data['points'])
                cmds.xform(bs_nurbs_crv, translation=dir_ctrlcrv_bs_data['xform']['translation'])

                bs_nurbs_crv = cmds.rename(bs_nurbs_crv,
                                           self._ctrl_crv_data['nasocheek_ctrlzone_prefix']+
                                           '_'+dir_ctrlcrv_bs_data['name'])

                cmds.setAttr(bs_nurbs_crv+'.overrideEnabled', True)
                if controlZoneDirEnum.right in direction:
                    cmds.setAttr(bs_nurbs_crv+'.overrideColor', COLOR_INDEX_INDIGO)
                    cmds.parent(bs_nurbs_crv,
                                hierarchy.nasocheek_ctrlcrv_bs_R_grp.get_group_name())
                else:
                    cmds.setAttr(bs_nurbs_crv+'.overrideColor', COLOR_INDEX_DARK_RED)
                    cmds.parent(bs_nurbs_crv,
                                hierarchy.nasocheek_ctrlcrv_bs_L_grp.get_group_name())

                cmds.toggle(bs_nurbs_crv, controlVertex=True)
                cmds.select(deselect=True)

                self._ctrl_crv_bs_dict[bs_type+'_'+crv_id] = bs_nurbs_crv

        # Create the control curve follow controllers.
        follow_ctrl_data = self._ctrl_crv_data['nasocheek_follow_controller']
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

            follow_data_dict = follow_ctrl_data['follow_data']
            for follow_attr in sorted(follow_data_dict):
                cmds.addAttr(follow_ctrl, longName=follow_attr, attributeType='float',
                             defaultValue=follow_data_dict[follow_attr], minValue=0.0, maxValue=1.0, keyable=True)

            cmds.setAttr(follow_ctrl+'.overrideEnabled', True)
            if 'R' == follow_ctrl_dir:
                cmds.setAttr(follow_ctrl+'.overrideColor', CONTROL_R_COLOR)
            elif 'L' == follow_ctrl_dir:
                cmds.setAttr(follow_ctrl+'.overrideColor', CONTROL_L_COLOR)

            cmds.parent(follow_ctrl, hierarchy.nasocheek_grp.get_group_name())

            cmds.select(deselect=True)

        self._follow_ctrl = follow_ctrl

        # --------------------------------------------------------------------------------------------------------------
        # Drive the control curves using blend-shape and
        # five-curves each in the LR and UD directions, as the targets.
        zone_dir = 'right'
        mouth_corner_U_controller = 'fm_mouthProject_RU_ctrl'
        mouth_corner_D_controller = 'fm_mouthProject_RD_ctrl'

        if controlZoneDirEnum.left in direction:
            zone_dir = 'left'
            mouth_corner_U_controller = 'fm_mouthProject_LU_ctrl'
            mouth_corner_D_controller = 'fm_mouthProject_LD_ctrl'

        assert cmds.objExists(mouth_corner_U_controller)
        assert cmds.objExists(mouth_corner_D_controller)

        cheek_follow_B_attr = self._follow_ctrl+'.cheek_follow_b'
        cheek_follow_C_attr = self._follow_ctrl+'.cheek_follow_c'
        cheek_follow_D_attr = self._follow_ctrl+'.cheek_follow_d'
        cheek_follow_E_attr = self._follow_ctrl+'.cheek_follow_e'
        cheek_follow_F_attr = self._follow_ctrl+'.cheek_follow_f'

        for crv_id in ctrl_crv_id_list:
            cheek_follow_attr = ''
            cheek_follow_multi_node = None

            if 'B' == crv_id:
                cheek_follow_attr = cheek_follow_B_attr
            elif 'C' == crv_id:
                cheek_follow_attr = cheek_follow_C_attr
            elif 'D' == crv_id:
                cheek_follow_attr = cheek_follow_D_attr
            elif 'E' == crv_id:
                cheek_follow_attr = cheek_follow_E_attr
            elif 'F' == crv_id:
                cheek_follow_attr = cheek_follow_F_attr

            if '' != cheek_follow_attr:
                assert cmds.objExists(cheek_follow_attr)

                cheek_follow_multi_node = cmds.createNode('multiplyDivide',
                                                          name=cheek_follow_attr.split('.')[1]+
                                                               '_'+follow_ctrl_dir+'_multiplyDivide')

            bs_LR_crv = self._ctrl_crv_bs_dict['bs_LR'+'_'+crv_id]
            bs_UD_crv = self._ctrl_crv_bs_dict['bs_UD'+'_'+crv_id]
            bs_FB_crv = self._ctrl_crv_bs_dict['bs_FB'+'_'+crv_id]
            bs_all_crv = self._ctrl_crv_bs_dict['bs_all'+'_'+crv_id]
            bs_orig_crv = self._ctrl_crv_bs_dict['original'+'_'+crv_id]
            proj_crv = self._ctrl_crv_dict[crv_id].get_name()

            bs_all_crv_bs = cmds.blendShape(bs_LR_crv,
                                            bs_UD_crv,
                                            bs_FB_crv,

                                            bs_all_crv,

                                            name=bs_all_crv+'_blendShape'
                                            )[0]
            cmds.setAttr(bs_all_crv_bs+'.supportNegativeWeights', True)

            proj_crv_bs = cmds.blendShape(bs_orig_crv,
                                          bs_all_crv,

                                          proj_crv,

                                          name=proj_crv+'_blendShape'
                                          )[0]
            cmds.setAttr(proj_crv_bs+'.'+bs_orig_crv, 1.0)
            cmds.setAttr(proj_crv_bs+'.'+bs_all_crv, 1.0)
            cmds.setAttr(proj_crv_bs+'.supportNegativeWeights', True)

            mouth_corner_trans_avg_node = cmds.createNode('plusMinusAverage',
                                                          name='mouth_corner_trans_'+zone_dir+'_'+crv_id+'_avg')
            cmds.setAttr(mouth_corner_trans_avg_node+'.operation', 3)

            cmds.connectAttr(mouth_corner_U_controller+'.translateX', mouth_corner_trans_avg_node+'.input3D[0].input3Dx')
            cmds.connectAttr(mouth_corner_U_controller+'.translateY', mouth_corner_trans_avg_node+'.input3D[0].input3Dy')
            cmds.connectAttr(mouth_corner_U_controller+'.translateZ', mouth_corner_trans_avg_node+'.input3D[0].input3Dz')

            cmds.connectAttr(mouth_corner_D_controller+'.translateX', mouth_corner_trans_avg_node+'.input3D[1].input3Dx')
            cmds.connectAttr(mouth_corner_D_controller+'.translateY', mouth_corner_trans_avg_node+'.input3D[1].input3Dy')
            cmds.connectAttr(mouth_corner_D_controller+'.translateZ', mouth_corner_trans_avg_node+'.input3D[1].input3Dz')

            if 'right' == zone_dir:
                mouth_corner_transx_rev_node = cmds.createNode('multiplyDivide',
                                                               name='mouth_corner_transX_'+zone_dir+'_'+crv_id+'_rev')
                cmds.connectAttr(mouth_corner_trans_avg_node+'.output3Dx', mouth_corner_transx_rev_node+'.input1X')
                cmds.setAttr(mouth_corner_transx_rev_node+'.input2X', -1.0)

                if '' != cheek_follow_attr:
                    cmds.connectAttr(mouth_corner_transx_rev_node+'.outputX', cheek_follow_multi_node+'.input1X')
                    cmds.connectAttr(cheek_follow_attr, cheek_follow_multi_node+'.input2X')
                    cmds.connectAttr(cheek_follow_multi_node+'.outputX', bs_all_crv_bs+'.'+bs_LR_crv)
                else:
                    cmds.connectAttr(mouth_corner_transx_rev_node+'.outputX', bs_all_crv_bs+'.'+bs_LR_crv)
            else:
                if '' != cheek_follow_attr:
                    cmds.connectAttr(mouth_corner_trans_avg_node+'.output3Dx', cheek_follow_multi_node+'.input1X')
                    cmds.connectAttr(cheek_follow_attr, cheek_follow_multi_node+'.input2X')
                    cmds.connectAttr(cheek_follow_multi_node+'.outputX', bs_all_crv_bs+'.'+bs_LR_crv)
                else:
                    cmds.connectAttr(mouth_corner_trans_avg_node+'.output3Dx', bs_all_crv_bs+'.'+bs_LR_crv)

            if '' != cheek_follow_attr:
                cmds.connectAttr(mouth_corner_trans_avg_node+'.output3Dy', cheek_follow_multi_node+'.input1Y')
                cmds.connectAttr(cheek_follow_attr, cheek_follow_multi_node+'.input2Y')
                cmds.connectAttr(cheek_follow_multi_node+'.outputY', bs_all_crv_bs+'.'+bs_UD_crv)
            else:
                cmds.connectAttr(mouth_corner_trans_avg_node+'.output3Dy', bs_all_crv_bs+'.'+bs_UD_crv)

            if '' != cheek_follow_attr:
                cmds.connectAttr(mouth_corner_trans_avg_node+'.output3Dz', cheek_follow_multi_node+'.input1Z')
                cmds.connectAttr(cheek_follow_attr, cheek_follow_multi_node+'.input2Z')
                cmds.connectAttr(cheek_follow_multi_node+'.outputZ', bs_all_crv_bs+'.'+bs_FB_crv)
            else:
                cmds.connectAttr(mouth_corner_trans_avg_node+'.output3Dz', bs_all_crv_bs+'.'+bs_FB_crv)

        # Use "closestPointOnSurface" nodes to establish the projecting relationships between
        # the locators on the control curves and the locators on the projection surface.

        for ctrl_crv_id in ctrl_crv_id_list:
            ctrl_crv = self._ctrl_crv_dict[ctrl_crv_id]

            for loc_id in ctrl_crv.get_locator_ids():
                ctrlcrv_loc_info = ctrl_crv.get_locator_info(loc_id)

                # Establish the projecting relationships in the up-down/UD directions.
                UD_projsrf_loc_info = self._ctrlproj_projsurface_LRUD.get_locator_info(ctrl_crv_id, loc_id)

                cls_pt_on_UD_transplane_node = cmds.createNode('closestPointOnSurface')
                cls_pt_on_UD_transplane_node = cmds.rename(cls_pt_on_UD_transplane_node,
                                                           ctrlcrv_loc_info[0]+'_clsPtOnSrf')

                cmds.connectAttr(self._ctrlproj_transplane_LRUD.get_name()+'.worldSpace[0]',
                                 cls_pt_on_UD_transplane_node+'.inputSurface')
                cmds.connectAttr(ctrlcrv_loc_info[0]+'Shape.worldPosition[0]',
                                 cls_pt_on_UD_transplane_node+'.inPosition')

                pt_on_UD_projsrf_node = UD_projsrf_loc_info[2]
                assert cmds.objExists(pt_on_UD_projsrf_node)

                cmds.connectAttr(cls_pt_on_UD_transplane_node+'.parameterU', pt_on_UD_projsrf_node+'.parameterU')
                cmds.connectAttr(cls_pt_on_UD_transplane_node+'.parameterV', pt_on_UD_projsrf_node+'.parameterV')

                # Establish the projecting relationships in the front/F direction.
                front_projsrf_id = ord(ctrl_crv_id) - 65

                F_projsrf_loc_info = \
                    ctrlproj_projsurface_LRFB_list[front_projsrf_id].get_locator_info(ctrl_crv_id, loc_id)

                cls_pt_on_F_transplane_node = cmds.createNode('closestPointOnSurface')
                cls_pt_on_F_transplane_node = cmds.rename(cls_pt_on_F_transplane_node,
                                                          ctrlcrv_loc_info[0]+'_srfF_clsPtOnSrf')

                cmds.connectAttr(self._ctrlproj_transplane_LRFB_list[front_projsrf_id].get_name()+'.worldSpace[0]',
                                 cls_pt_on_F_transplane_node+'.inputSurface')
                cmds.connectAttr(ctrlcrv_loc_info[0]+'Shape.worldPosition[0]',
                                 cls_pt_on_F_transplane_node+'.inPosition')

                pt_on_F_projsrf_node = F_projsrf_loc_info[2]
                assert cmds.objExists(pt_on_F_projsrf_node)

                cmds.connectAttr(cls_pt_on_F_transplane_node+'.parameterU', pt_on_F_projsrf_node+'.parameterU')
                cmds.connectAttr(cls_pt_on_F_transplane_node+'.parameterV', pt_on_F_projsrf_node+'.parameterV')

        # Bind the projection surfaces in the front-back direction to the
        # corresponding joint chain on the projection surface in the left-right direction.
        projsrf_FB_span_V = ctrlproj_projsurface_LRFB_list[0]._patchesV

        projsrf_FB_ids = ctrl_crv_id_list
        projsrf_LRUD_jnt_row_ids = UD_projsrf_loc_row_ids = self._ctrlproj_projsurface_LRUD.get_locator_row_ids()
        assert len(projsrf_FB_ids) == len(projsrf_LRUD_jnt_row_ids)

        for projsrf_FB_id in projsrf_FB_ids:
            projsrf_FB = ctrlproj_projsurface_LRFB_list[projsrf_FB_ids.index(projsrf_FB_id)].get_name()
            LR_jnt_list = []
            for LR_jnt_id in range(0, projsrf_FB_span_V+1):
                LR_loc_info = self._ctrlproj_projsurface_LRUD.get_locator_info(projsrf_FB_id, LR_jnt_id+1)
                LR_jnt_list.append(LR_loc_info[1])

            projsrf_FB_skinCluster = cmds.skinCluster(LR_jnt_list, projsrf_FB,
                                                      toSelectedBones=True, name=projsrf_FB+'_skinCluster')[0]
            for cv_id in range(projsrf_FB_span_V, -1, -1):
                cv_1 = '{}.cv[0][{}]'.format(projsrf_FB, cv_id)
                cv_2 = '{}.cv[1][{}]'.format(projsrf_FB, cv_id)
                jnt = LR_jnt_list[projsrf_FB_span_V-cv_id]

                cmds.skinPercent(projsrf_FB_skinCluster, cv_1, transformValue=[(jnt, 1.0)], zeroRemainingInfluences=True)
                cmds.skinPercent(projsrf_FB_skinCluster, cv_2, transformValue=[(jnt, 1.0)], zeroRemainingInfluences=True)