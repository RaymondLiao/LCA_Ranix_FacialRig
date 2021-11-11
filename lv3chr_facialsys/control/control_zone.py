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

import controller; reload(controller)
from controller import controller

# ======================================================================================================================
class controlZone(object):
    """ A control zone organizes the controllers, the control curves, and the locator_data as well as the bind joints
    corresponding to the CVs on the curves functioning as a whole.

    For eyelid module, a control zone should contain 4 control curves, 4*5 locator_data, and 5 controllers binding to
    5 joints as a unit to transfer the translations of controllers to the locator_data on a projection plane.
    """

    # The keys of this dictionary are curves' IDs.
    _ctrl_crv_dict = {
        'A': None,
    }
    def get_ctrlcrv_count(self):
        return len(self._ctrl_crv_dict)

    # The keys of this dictionary are controllers' IDs.
    _controller_dict = {
        'A': None,
    }
    def get_controller_count(self):
        return len(self._controller_dict)

    _ctrlproj_transplane = None
    _ctrlproj_projsurface = None

    def __init__(self,
                 zone=controlZoneEnum.eyelid,
                 direction=controlZoneDirEnum.right_up,
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
                eyelid_ctrl_crv = controlCurve(name_prefix = ctrl_crv_data['eyelid_zone_prefix'],
                                               name = eyelid_dir_ctrlcrv_data['name'],
                                               degree = eyelid_ctrlcrv_degree,
                                               translation=eyelid_dir_ctrlcrv_data['xform']['translation'],
                                               points = eyelid_dir_ctrlcrv_data['points'],
                                               locator_data = eyelid_dir_ctrlcrv_data['locators'],
                                               locator_scale = eyelid_ctrlcrv_data['locator_scale'])

                loc_count = eyelid_ctrl_crv.get_locator_count()

                if controlZoneDirEnum.right_up == direction:
                    cmds.parent(eyelid_ctrl_crv.get_name(),
                                lv3chr_facialsys_hierarchy.eyelid_ctrlcrv_RU_grp.get_group_name())

                    for loc_idx in range(loc_count):
                        loc_id = loc_idx + 1
                        if 'A' == crv_id:
                            cmds.parent(eyelid_ctrl_crv.get_locator_info(locator_id=loc_id)[0],
                                        lv3chr_facialsys_hierarchy.eyelid_ctrlcrv_loc_RU_A_grp.get_group_name())
                        elif 'B' == crv_id:
                            cmds.parent(eyelid_ctrl_crv.get_locator_info(locator_id=loc_id)[0],
                                        lv3chr_facialsys_hierarchy.eyelid_ctrlcrv_loc_RU_B_grp.get_group_name())
                        elif 'C' == crv_id:
                            cmds.parent(eyelid_ctrl_crv.get_locator_info(locator_id=loc_id)[0],
                                        lv3chr_facialsys_hierarchy.eyelid_ctrlcrv_loc_RU_C_grp.get_group_name())
                        elif 'D' == crv_id:
                            cmds.parent(eyelid_ctrl_crv.get_locator_info(locator_id=loc_id)[0],
                                        lv3chr_facialsys_hierarchy.eyelid_ctrlcrv_loc_RU_D_grp.get_group_name())

                elif controlZoneDirEnum.right_dn == direction:
                    cmds.parent(eyelid_ctrl_crv.get_name(),
                                lv3chr_facialsys_hierarchy.eyelid_ctrlcrv_RD_grp.get_group_name())

                    for loc_idx in range(loc_count):
                        loc_id = loc_idx + 1
                        if 'A' == crv_id:
                            cmds.parent(eyelid_ctrl_crv.get_locator_info(locator_id=loc_id)[0],
                                        lv3chr_facialsys_hierarchy.eyelid_ctrlcrv_loc_RD_A_grp.get_group_name())
                        elif 'B' == crv_id:
                            cmds.parent(eyelid_ctrl_crv.get_locator_info(locator_id=loc_id)[0],
                                        lv3chr_facialsys_hierarchy.eyelid_ctrlcrv_loc_RD_B_grp.get_group_name())
                        elif 'C' == crv_id:
                            cmds.parent(eyelid_ctrl_crv.get_locator_info(locator_id=loc_id)[0],
                                        lv3chr_facialsys_hierarchy.eyelid_ctrlcrv_loc_RD_C_grp.get_group_name())
                        elif 'D' == crv_id:
                            cmds.parent(eyelid_ctrl_crv.get_locator_info(locator_id=loc_id)[0],
                                        lv3chr_facialsys_hierarchy.eyelid_ctrlcrv_loc_RD_D_grp.get_group_name())

                elif controlZoneDirEnum.left_up == direction:
                    cmds.parent(eyelid_ctrl_crv.get_name(),
                                lv3chr_facialsys_hierarchy.eyelid_ctrlcrv_LU_grp.get_group_name())

                    for loc_idx in range(loc_count):
                        loc_id = loc_idx + 1
                        if 'A' == crv_id:
                            cmds.parent(eyelid_ctrl_crv.get_locator_info(locator_id=loc_id)[0],
                                        lv3chr_facialsys_hierarchy.eyelid_ctrlcrv_loc_LU_A_grp.get_group_name())
                        elif 'B' == crv_id:
                            cmds.parent(eyelid_ctrl_crv.get_locator_info(locator_id=loc_id)[0],
                                        lv3chr_facialsys_hierarchy.eyelid_ctrlcrv_loc_LU_B_grp.get_group_name())
                        elif 'C' == crv_id:
                            cmds.parent(eyelid_ctrl_crv.get_locator_info(locator_id=loc_id)[0],
                                        lv3chr_facialsys_hierarchy.eyelid_ctrlcrv_loc_LU_C_grp.get_group_name())
                        elif 'D' == crv_id:
                            cmds.parent(eyelid_ctrl_crv.get_locator_info(locator_id=loc_id)[0],
                                        lv3chr_facialsys_hierarchy.eyelid_ctrlcrv_loc_LU_D_grp.get_group_name())

                elif controlZoneDirEnum.left_dn == direction:
                    cmds.parent(eyelid_ctrl_crv.get_name(),
                                lv3chr_facialsys_hierarchy.eyelid_ctrlcrv_LD_grp.get_group_name())

                    for loc_idx in range(loc_count):
                        loc_id = loc_idx + 1
                        if 'A' == crv_id:
                            cmds.parent(eyelid_ctrl_crv.get_locator_info(locator_id=loc_id)[0],
                                        lv3chr_facialsys_hierarchy.eyelid_ctrlcrv_loc_LD_A_grp.get_group_name())
                        elif 'B' == crv_id:
                            cmds.parent(eyelid_ctrl_crv.get_locator_info(locator_id=loc_id)[0],
                                        lv3chr_facialsys_hierarchy.eyelid_ctrlcrv_loc_LD_B_grp.get_group_name())
                        elif 'C' == crv_id:
                            cmds.parent(eyelid_ctrl_crv.get_locator_info(locator_id=loc_id)[0],
                                        lv3chr_facialsys_hierarchy.eyelid_ctrlcrv_loc_LD_C_grp.get_group_name())
                        elif 'D' == crv_id:
                            cmds.parent(eyelid_ctrl_crv.get_locator_info(locator_id=loc_id)[0],
                                        lv3chr_facialsys_hierarchy.eyelid_ctrlcrv_loc_LD_D_grp.get_group_name())

                self._ctrl_crv_dict[crv_id] = eyelid_ctrl_crv

            # Create the controllers.
            eyelid_controller_data = ctrl_crv_data['eyelid_controller']
            eyelid_controller_degree = eyelid_controller_data['degree']
            eyelid_controller_color = 0
            eyelid_controller_points = []

            if 'u' in direction:
                eyelid_controller_color = CONTROLLER_UP_COLOR
                eyelid_controller_points = eyelid_controller_data['points_up']
            elif 'd' in direction:
                eyelid_controller_color = CONTROLLER_DN_COLOR
                eyelid_controller_points = eyelid_controller_data['points_dn']

            for crv_id in controller_id_list:
                eyelid_dir_ctrl_data = eyelid_controller_data[direction+'_'+crv_id]
                eyelid_controller = controller(name = ctrl_crv_data['eyelid_zone_prefix'] + '_' +
                                                      eyelid_dir_ctrl_data['name'],
                                               degree = eyelid_controller_degree,
                                               color = eyelid_controller_color,
                                               points = eyelid_controller_points,
                                               translation_ofs=eyelid_dir_ctrl_data['xform']['translation_ofs'],
                                               translation = eyelid_dir_ctrl_data['xform']['translation'])

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
