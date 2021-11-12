#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# File Name: contrl_crv.py
# Author: Sheng (Raymond) Liao
# Date: October 2021
#

"""
A module containing the definitions of control curves.
"""

import warnings
import maya.cmds as cmds

from general import lv3chr_facialsys_config; reload(lv3chr_facialsys_config)
from general.lv3chr_facialsys_config import *

from general import lv3chr_facialsys_hierarchy; reload(lv3chr_facialsys_hierarchy)

# ======================================================================================================================
class controlCurve(object):
    """ Control Curves are used to transit the translation of
    locator_data binding joints on the projected surface.
    """

    # NURBS curve construction parameters
    _degree = 1
    _nurbs_crv = None

    # locator_data pinned on the curve
    # The dictionary format is {locator_id: (locator's name, pointOnCurveInfo node's name)}
    # e.g {1: ('fm_eyelidProject_RU_A1_loc', 'fm_eyelidProject_RU_A1_loc_ptOnCrv)}
    _locator_dict = {}
    def get_locator_ids(self):
        """
        :return: a list of all identity numbers of the locators belonging to this control curve, e.g. [1, 2, 3]
        """
        return self._locator_dict.keys()
    def get_locator_info(self, locator_id):
        """
        :param locator_id: the locator identity number, starts from 1
        :return: a tuple of the format (locator's name, pointOnCurveInfo node's name)
        """
        if locator_id not in self._locator_dict.keys():
            cmds.warning('[controlCurve] Try to access the locator whose locator_id does not exist.')
            return None

        return self._locator_dict[locator_id]

    def __init__(self,
                 name_prefix = '',
                 name='control_curve',
                 degree=1,
                 translation=[0, 0, 0],
                 points=[],
                 locator_data=[],
                 locator_scale=[1, 1, 1]):

        # Create the NURBS curve as the control curve and move it into position.
        self._degree = degree
        assert len(points) > 0

        self._nurbs_crv = cmds.curve(degree=self._degree,
                                     point=points)

        cmds.xform(self._nurbs_crv,
                   translation=translation)

        self._nurbs_crv = cmds.rename(self._nurbs_crv, name_prefix+'_'+name)

        cmds.setAttr(self._nurbs_crv+'.overrideEnabled', True)
        cmds.setAttr(self._nurbs_crv+'.overrideColor',
                     CTRL_CURVE_COLOR_INDEX)
        cmds.toggle(self._nurbs_crv, controlVertex=True)
        cmds.select(deselect=True)

        # Create the locator_data belongs to this control curve, then use pointOnCurveInfo nodes to pin them onto it.
        for loc_dict in locator_data:
            loc_id = loc_dict['id']
            loc_name = loc_dict['name']
            loc_param = loc_dict['pt_on_crv_param']

            loc = cmds.spaceLocator(name=name_prefix+'_'+loc_name)[0]
            assert cmds.objExists(loc+'Shape')
            for idx, axis in {0:'X', 1:'Y', 2:'Z'}.items():
                cmds.setAttr(loc+'Shape.localScale'+axis, locator_scale[idx])

            cmds.setAttr(loc+'.overrideEnabled', True)
            cmds.setAttr(loc+'.overrideColor', CTRL_CURVE_LOC_COLOR_INDEX)

            pt_on_crv_info_node = cmds.createNode('pointOnCurveInfo', name=name_prefix+'_'+loc_name+'_ptOnCrv')
            cmds.setAttr(pt_on_crv_info_node+'.parameter', loc_param)
            cmds.connectAttr(self._nurbs_crv+'.worldSpace[0]', pt_on_crv_info_node+'.inputCurve')
            cmds.connectAttr(pt_on_crv_info_node+'.position', loc+'.translate')

            self._locator_dict[int(loc_id)] = (loc, pt_on_crv_info_node)

            cmds.select(deselect=True)

    def __repr__(self):
        return NotImplemented

    def get_name(self):
        return str(self._nurbs_crv)