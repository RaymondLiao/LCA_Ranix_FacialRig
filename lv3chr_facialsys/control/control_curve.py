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

class controlCurve(object):
    """ Control Curves are used to transit the translation of
    locators binding joints on the projected surface.
    """

    _degree = 1
    _nurbs_crv = None

    # The dictionary format is "id: (name of the locator, point-on-curve parameter)"
    # e.g 1: ('fm_eyelidProject_RU_A1_loc', 0.0)
    _loc_dict = {}
    def get_locator_count(self):
        return len(self._loc_dict)
    def get_locator_info(self, id):
        """
        :param id: the locator index
        :return: the (name, point-on-curve param) tuple
        """
        if id > len(self._loc_dict) - 1:
            cmds.warning('[controlCurve] Try to access the locator whose id is larger than \
                         the greatest one of this control curve.')
            return None

        return self._loc_dict[id]

    def __init__(self,
                 name_prefix = '',
                 name='control_curve',
                 degree=1,
                 translation=[0, 0, 0],
                 points=[],
                 locators=[],
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

        # Create the locators belongs to this curve, then use pointOnCurveInfo nodes to pin them onto it.
        for loc_dict in locators:
            loc_id = loc_dict.keys()[0]
            loc_name = loc_dict[loc_id]['name']
            loc_param = loc_dict[loc_id]['pt_on_crv_param']

            loc = cmds.spaceLocator(name=name_prefix+'_'+loc_name)[0]
            assert cmds.objExists(loc+'Shape')
            for idx, axis in {0:'X', 1:'Y', 2:'Z'}.items():
                cmds.setAttr(loc+'Shape.localScale'+axis, locator_scale[idx])

            cmds.setAttr(loc+'.overrideEnabled', True)
            cmds.setAttr(loc+'.overrideColor', CTRL_DURVE_LOC_COLOR_INDEX)

            self._loc_dict[int(loc_id)-1] = (loc, loc_param)

            pt_on_crv_info_node = cmds.createNode('pointOnCurveInfo', name=name_prefix+'_'+loc_name)
            cmds.setAttr(pt_on_crv_info_node+'.parameter', loc_param)
            cmds.connectAttr(self._nurbs_crv+'.worldSpace[0]', pt_on_crv_info_node+'.inputCurve')
            cmds.connectAttr(pt_on_crv_info_node+'.position', loc+'.translate')

    def __repr__(self):
        return NotImplemented

    def get_name(self):
        return str(self._nurbs_crv)