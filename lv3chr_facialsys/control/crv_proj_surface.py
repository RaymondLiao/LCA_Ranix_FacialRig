#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# File Name: crv_proj_surface.py
# Author: Sheng (Raymond) Liao
# Date: October 2021
#

"""
A module containing the definitions of control-curves projection plane classes
"""

import warnings
import maya.cmds as cmds

from general import lv3chr_facialsys_config; reload(lv3chr_facialsys_config)
from general.lv3chr_facialsys_config import *

class curveTransPlane(object):
    """ translation plane indicating the movement area of facial rig control
    data curves' CVs
    """

    _degree = 1
    _patchesU = 4
    _patchesV = 6
    _nurbs_srf = None

    def __init__(self, name='curve_translation_plane', degree=1, patchesU=4, patchesV=6,
               translation=[0.0, 0.0, 0.0], rotation=[0.0, 0.0, 0.0], scale=[1.0, 1.0, 1.0],
               mirror=[1, 1, 1]):

        self._degree = degree
        self._patchesU = patchesU
        self._patchesV = patchesV

        self._nurbs_srf = cmds.nurbsPlane(degree=self._degree,
                                          patchesU=self._patchesU,
                                          patchesV=self._patchesV)[0]   # Note the [0] indexing

        cmds.xform(self._nurbs_srf,
                   translation=translation,
                   rotation=rotation,
                   scale=scale)
        cmds.makeIdentity(self._nurbs_srf, apply=True)
        cmds.xform(self._nurbs_srf, scale=mirror)
        # Reverse the surface normals if mirroring along x-axis.
        if mirror[0] < 0:
            cmds.reverseSurface(self._nurbs_srf, direction=0) # "0" means "U"

        self._nurbs_srf = cmds.rename(self._nurbs_srf, name)
        cmds.toggle(self._nurbs_srf, template=True)

    def __repr__(self):
        return NotImplemented

    def get_name(self):
        return str(self._nurbs_srf)


class curveProjSurface(object):
    """ projection plane constraining on which the movement area of locators
    projected from the movement of joints on the control data curves
    """

    _degree = 1
    _patchesU = 4
    _patchesV = 6
    _cv_coords = []
    _nurbs_srf = None

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

        self._nurbs_srf = cmds.nurbsPlane(degree=self._degree,
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
                cmds.setAttr(self._nurbs_srf + '.cv[{}][{}]'.format(idx_u, idx_v),
                             cv_coord[0], cv_coord[1], cv_coord[2])

        cmds.xform(self._nurbs_srf,
                   translation=translation,
                   rotation=rotation,
                   scale=scale)
        cmds.makeIdentity(self._nurbs_srf, apply=True)
        cmds.xform(self._nurbs_srf, scale=mirror)
        # Reverse the surface normals if mirroring along x-axis.
        if mirror[0] < 0:
            cmds.reverseSurface(self._nurbs_srf, direction=0) # "0" means "U"

        self._nurbs_srf = cmds.rename(self._nurbs_srf, name)

        # Set display attributes.
        cmds.select(self._nurbs_srf, replace=True)
        cmds.sets(edit=True, forceElement=PROJ_SRF_SHADER+'_SG')
        cmds.select(deselect=True)

        cmds.setAttr(self._nurbs_srf+'.overrideEnabled', True)
        cmds.setAttr(self._nurbs_srf+'.overrideColor', PROJ_SURFACE_COLOR_INDEX)
        cmds.toggle(self._nurbs_srf, controlVertex=True)

    def __repr__(self):
        return NotImplemented

    def get_name(self):
        return str(self._nurbs_srf)

# ----------------------------------------------------------------------------------------------------------------------
    # eyelid control curves translation planes' names:
    # -- fm_eyelidProjectPlane_RU_nbs
    # -- fm_eyelidProjectPlane_RD_nbs
    # -- fm_eyelidProjectPlane_LU_nbs
    # -- fm_eyelidProjectPlane_LD_nbs

    # eyelid control curves (translation) projection planes' names:
    # -- fm_eyelidFaceMask_RU_nbs
    # -- fm_eyelidFaceMask_RD_nbs
    # -- fm_eyelidFaceMask_LU_nbs
    # -- fm_eyelidFaceMask_LD_nbs