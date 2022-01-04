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