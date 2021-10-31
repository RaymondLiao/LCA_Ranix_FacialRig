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
        cmds.toggle(self._curve, template=True)

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
    _cv_coords = []
    _curve = None

    def __init__(self, name='curve_projection_plane',
                 degree=1, patchesU=4, patchesV=6, cv_list=[],
                 translation=[0.0, 0.0, 0.0], rotation=[0.0, 0.0, 0.0], scale=[1.0, 1.0, 1.0],
                 mirror=[1, 1, 1]):
        """
        :param cv_list: A list of CV coordinates for the NURBS plane to construct;
                        Note that the maximum length of this list is (patchesU+1)*(patchesV+1).
        """

        self._degree = degree
        self._patchesU = patchesU
        self._patchesV = patchesV
        assert len(cv_list) <= (patchesU+1) * (patchesV+1)

        self._curve = cmds.nurbsPlane(degree=self._degree,
                                      patchesU=self._patchesU,
                                      patchesV=self._patchesV)[0]   # Note the [0] indexing
        if len(cv_list) > 0:
            for cv_coord_dict in cv_list:
                cv_coord_idx = list(cv_coord_dict.keys())[0]
                idx_u = cv_coord_idx.split(',')[0]
                idx_v = cv_coord_idx.split(',')[1]

                cv_coord = cv_coord_dict[cv_coord_idx]

                # print('cv_coord: ({},{}) : {}'.format(idx_u, idx_v, cv_coord))
                assert len(cv_coord) == 3
                cmds.setAttr(self._curve+'.cv[{}][{}]'.format(idx_u, idx_v),
                             cv_coord[0], cv_coord[1], cv_coord[2])

        cmds.xform(self._curve,
                   translation=translation,
                   rotation=rotation,
                   scale=scale)
        cmds.makeIdentity(self._curve, apply=True)
        cmds.xform(self._curve, scale=mirror)

        self._curve = cmds.rename(self._curve, name)
        cmds.toggle(self._curve, template=True, controlVertex=True)

    def __repr__(self):
        warnings.warn('No Implementation.')
        pass

    def name(self):
        return str(self._curve)