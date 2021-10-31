#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# File Name: crv_proj_plane.py
# Author: Sheng (Raymond) Liao
# Date: October 2021
#

"""
A module containing the definitions of control-curves projection plane classes
"""

import warnings
import maya.cmds as cmds

class curveTransPlane(object):
    """ translation plane indicating the movement area of facial rig control
    data curves' CVs
    """

    _degree = 1
    _patchesU = 4
    _patchesV = 6
    _curve = None

    def __init__(self, name='curve_translation_plane', degree=1, patchesU=4, patchesV=6,
               translation=[0.0, 0.0, 0.0], rotation=[0.0, 0.0, 0.0], scale=[1.0, 1.0, 1.0],
               mirror=[1, 1, 1]):

        self._degree = degree
        self._patchesU = patchesU
        self._patchesV = patchesV

        self._curve = cmds.nurbsPlane(degree=self._degree,
                                      patchesU=self._patchesU,
                                      patchesV=self._patchesV)[0]   # Note the [0] indexing

        cmds.xform(self._curve,
                   translation=translation,
                   rotation=rotation,
                   scale=scale)
        cmds.makeIdentity(self._curve, apply=True)
        cmds.xform(self._curve, scale=mirror)

        self._curve = cmds.rename(self._curve, name)

    def __repr__(self):
        warnings.warn('No Implementation.')
        pass

    def name(self):
        return str(self._curve)


class curveProjPlane(object):
    """ projection plane constraining on which the movement area of locators
    projected from the movement of joints on the control data curves
    """

    _degree = 1
    _patchesU = 4
    _patchesV = 6
    _curve = None

    def __init__(self, name='curve_projection_plane', degree=1, patchesU=4, patchesV=6,
               translation=[0.0, 0.0, 0.0], rotation=[0.0, 0.0, 0.0], scale=[1.0, 1.0, 1.0],
               mirror=[1, 1, 1]):

        self._degree = degree
        self._patchesU = patchesU
        self._patchesV = patchesV

        self._curve = cmds.nurbsPlane(degree=self._degree,
                                      patchesU=self._patchesU,
                                      patchesV=self._patchesV)[0]   # Note the [0] indexing

        cmds.xform(self._curve,
                   translation=translation,
                   rotation=rotation,
                   scale=scale)
        cmds.makeIdentity(self._curve, apply=True)
        cmds.xform(self._curve, scale=mirror)

        self._curve = cmds.rename(self._curve, name)

    def __repr__(self):
        warnings.warn('No Implementation.')
        pass

    def name(self):
        return str(self._curve)