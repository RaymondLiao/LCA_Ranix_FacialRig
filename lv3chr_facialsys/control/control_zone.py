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

class controlZone(object):
    """ A control zone organizes the controllers, the control curves, and the locators as well as the bind joints
    corresponding to the CVs on the curves functioning as a whole.

    For eyelid module, a control zone should contain 4 control curves, 4*5 locators, and 5 controllers binding to
    5 joints as a unit to transfer the translations of controllers to the locators on a projection plane.
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

    _crvproj_transplane = None
    _crvproj_projsurface = None

    def __init__(self,
                 zone=controlZoneEnum.eyelid,
                 direction=controlZoneDirEnum.right_up,
                 ctrl_crv_data = None,
                 crvproj_transplane = None,
                 crvproj_projsurface = None
                 ):
        """
        :param zone: the facial zone this control unit manages
        :param direction: the direction in which the controllers of this control unit move
        :param ctrl_crv_data: the control curves' and controllers' construction data
        :param crvproj_transplane: the controllers translation plane this control unit belongs to
        :param crvproj_projsurface: the controllers translation-projection surface this control unit belongs to
        """
        assert None != ctrl_crv_data
        assert None != crvproj_transplane
        assert None != crvproj_projsurface

        self._crvproj_transplane = crvproj_transplane
        self._crvproj_projsurface = crvproj_projsurface

        ctrlcrv_data = {}
        ctrlcrv_degree = 1

        # Eyelid Zone
        if controlZoneEnum.eyelid == zone:
            ctrl_crv_id_list = ['A', 'B', 'C', 'D']
            controller_id_list = ['A', 'B', 'C', 'D', 'E']

            # Create the control curves.
            eyelid_ctrlcrv_data = ctrl_crv_data['eyelid_control_curve']
            eyelid_ctrlcrv_degree = eyelid_ctrlcrv_data['degree']

            for id in ctrl_crv_id_list:
                eyelid_dir_ctrlcrv_data = eyelid_ctrlcrv_data[direction + '_' + id]
                eyelid_ctrl_crv = controlCurve(name = ctrl_crv_data['eyelid_zone_prefix'] + '_' +
                                                      eyelid_dir_ctrlcrv_data['name'],
                                               degree = eyelid_ctrlcrv_degree,
                                               points = eyelid_dir_ctrlcrv_data['points'],
                                               translation = eyelid_dir_ctrlcrv_data['xform']['translation'])

                if controlZoneDirEnum.right_up == direction:
                    cmds.parent(eyelid_ctrl_crv.get_name(),
                                lv3chr_facialsys_hierarchy.eyelid_ctrlcrv_RU_grp.get_group_name())
                elif controlZoneDirEnum.right_dn == direction:
                    cmds.parent(eyelid_ctrl_crv.get_name(),
                                lv3chr_facialsys_hierarchy.eyelid_ctrlcrv_RD_grp.get_group_name())
                elif controlZoneDirEnum.left_up == direction:
                    cmds.parent(eyelid_ctrl_crv.get_name(),
                                lv3chr_facialsys_hierarchy.eyelid_ctrlcrv_LU_grp.get_group_name())
                elif controlZoneDirEnum.left_dn == direction:
                    cmds.parent(eyelid_ctrl_crv.get_name(),
                                lv3chr_facialsys_hierarchy.eyelid_ctrlcrv_LD_grp.get_group_name())

                self._ctrl_crv_dict[id] = eyelid_ctrl_crv

            # Create the controllers.
            eyelid_controller_data = ctrl_crv_data['eyelid_controller']
            eyelid_controller_degree = eyelid_controller_data['degree']
            eyelid_controller_color = 0
            eyelid_controller_points = []

            if 'u' in direction:
                eyelid_controller_color = eyelid_controller_data['color_up']
                eyelid_controller_points = eyelid_controller_data['points_up']
            elif 'd' in direction:
                eyelid_controller_color = eyelid_controller_data['color_dn']
                eyelid_controller_points = eyelid_controller_data['points_dn']

            for id in controller_id_list:
                eyelid_dir_ctrl_data = eyelid_controller_data[direction+'_'+id]
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
