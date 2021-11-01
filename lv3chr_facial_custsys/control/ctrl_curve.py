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

class controlCurve(object):
    """ Control Curves are used to transit the translation of
    locators binding joints on the projected surface.
    """

    _degree = 1,
    _nurbs_crv = None

    def __init__(self, name='control_curve',
                 degree=1, points=[],
                 translation=[0, 0, 0]):

        self._degree = degree
        assert len(points) > 0

        self._nurbs_crv = cmds.curve(degree=self._degree,
                                     point=points)

        cmds.xform(self._nurbs_crv,
                   translation=translation)

        self._nurbs_crv = cmds.rename(self._nurbs_crv, name)
        cmds.toggle(self._nurbs_crv, controlVertex=True)

    def __repr__(self):
        warnings.warn('No Implementation')
        pass

    def name(self):
        return str(self._nurbs_crv)