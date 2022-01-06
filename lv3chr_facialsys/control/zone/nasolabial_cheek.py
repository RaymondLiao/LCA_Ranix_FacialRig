#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# File Name: control.zone.cheek.py
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
                 direction=controlZoneDirEnum.right + '_' + controlZoneDirEnum.up + '_' + controlZoneDirEnum.down,
                 ctrl_crv_data = None,
                 ctrlproj_transplane_LRUD = None,
                 ctrlproj_projsurface_LRUD = None
                 ):
        """ A Nasolabial-Cheek Control Zone instance's direction attribute may have the value of
            "right_up_dn/RUD" or "left_up_dn/LUD".
        """

        super(nasoCheekControlZone, self).__init__(zone = controlZoneEnum.nasocheek,
                                                   direction = direction,
                                                   ctrl_crv_data = ctrl_crv_data,
                                                   ctrlproj_transplane_LRUD = ctrlproj_transplane_LRUD,
                                                   ctrlproj_projsurface_LRUD = ctrlproj_projsurface_LRUD)

        ctrl_crv_id_list = ['A', 'B', 'C', 'D', 'E']

        # Create the control curves.
        ctrlcrv_data = self._ctrl_crv_data['nasocheek_control_curve']
        ctrlcrv_degree = ctrlcrv_data['degree']

        for crv_id in ctrl_crv_id_list:
            dir_ctrlcrv_data = ctrlcrv_data[direction.split('_')[0] + '_' + crv_id]
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
                                           self._ctrl_crv_data['nasocheek_ctrlzone_prefix'] +
                                           '_' + dir_ctrlcrv_bs_data['name'])

                cmds.setAttr(bs_nurbs_crv + '.overrideEnabled', True)
                if controlZoneDirEnum.right in direction:
                    cmds.setAttr(bs_nurbs_crv + '.overrideColor', COLOR_INDEX_INDIGO)
                    cmds.parent(bs_nurbs_crv,
                                hierarchy.nasocheek_ctrlcrv_bs_R_grp.get_group_name())
                else:
                    cmds.setAttr(bs_nurbs_crv + '.overrideColor', COLOR_INDEX_DARK_RED)
                    cmds.parent(bs_nurbs_crv,
                                hierarchy.nasocheek_ctrlcrv_bs_L_grp.get_group_name())

                cmds.toggle(bs_nurbs_crv, controlVertex=True)
                cmds.select(deselect=True)

                self._ctrl_crv_bs_dict[bs_type+'_'+crv_id] = bs_nurbs_crv

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

        for crv_id in ctrl_crv_id_list:
            bs_LR_crv = self._ctrl_crv_bs_dict['bs_LR'+'_'+crv_id]
            bs_UD_crv = self._ctrl_crv_bs_dict['bs_UD'+'_'+crv_id]
            bs_all_crv = self._ctrl_crv_bs_dict['bs_all'+'_'+crv_id]
            bs_orig_crv = self._ctrl_crv_bs_dict['original'+'_'+crv_id]
            proj_crv = self._ctrl_crv_dict[crv_id].get_name()

            bs_all_crv_bs = cmds.blendShape(bs_LR_crv,
                                            bs_UD_crv,

                                            bs_all_crv,

                                            name=bs_all_crv + '_blendShape'
                                            )[0]
            cmds.setAttr(bs_all_crv_bs + '.supportNegativeWeights', True)

            proj_crv_bs = cmds.blendShape(bs_orig_crv,
                                          bs_all_crv,

                                          proj_crv,

                                          name=proj_crv + '_blendShape'
                                          )[0]
            cmds.setAttr(proj_crv_bs+'.'+bs_orig_crv, 1.0)
            cmds.setAttr(proj_crv_bs+'.'+bs_all_crv, 1.0)
            cmds.setAttr(proj_crv_bs + '.supportNegativeWeights', True)

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
                cmds.connectAttr(mouth_corner_transx_rev_node+'.outputX', bs_all_crv_bs+'.'+bs_LR_crv)
            else:
                cmds.connectAttr(mouth_corner_trans_avg_node+'.output3Dx', bs_all_crv_bs+'.'+bs_LR_crv)
            cmds.connectAttr(mouth_corner_trans_avg_node+'.output3Dy', bs_all_crv_bs+'.'+bs_UD_crv)

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