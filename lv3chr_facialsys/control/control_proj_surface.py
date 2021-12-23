#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# File Name: control_proj_surface.py
# Author: Sheng (Raymond) Liao
# Date: October 2021
#

"""
A module containing the definitions of control-curves projection plane classes
"""

import warnings
import maya.cmds as cmds

from general import config; reload(config)
from general.config import *

# ======================================================================================================================
class controlTransPlane(object):
    """ translation plane indicating the movement area of facial rig control
    data curves' CVs
    """

    def __init__(self,
                 name_prefix = '',
                 name = 'control_translation_plane',
                 degree = 1,
                 patchesU = 4,
                 patchesV = 6,
                 translation = [0.0, 0.0, 0.0],
                 rotation = [0.0, 0.0, 0.0],
                 scale = [1.0, 1.0, 1.0],
                 mirror = [1, 1, 1],
                 cv_list = []):
        """
        :param cv_list: A list of CV coordinates for the NURBS plane to construct;
                        Note that the maximum length of this list is (patchesU+1)*(patchesV+1).
        """

        # Member Variable Definitions ----------------------------------------------------------------------------------
        self._degree = degree
        self._patchesU = patchesU
        self._patchesV = patchesV

        self._cv_coords = []
        self._nurbs_srf = None
        # ---------------------------------------------------------------------------------- Member Variable Definitions

        assert len(cv_list) <= (patchesU + 1) * (patchesV + 1)

        self._nurbs_srf = cmds.nurbsPlane(degree=self._degree,
                                          patchesU=self._patchesU,
                                          patchesV=self._patchesV)[0]   # Note the [0] indexing

        if len(cv_list) > 0:
            self._cv_coords = cv_list

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
        # if mirror[0] < 0:
        #     cmds.reverseSurface(self._nurbs_srf, direction=0) # "0" means "U"

        self._nurbs_srf = cmds.rename(self._nurbs_srf, name_prefix+'_'+name)

        cmds.setAttr(self._nurbs_srf+'.overrideEnabled', True)
        cmds.setAttr(self._nurbs_srf+'.overrideColor', COLOR_INDEX_BLACK)
        cmds.toggle(self._nurbs_srf, template=True)
        cmds.select(deselect=True)

    def __repr__(self):
        return NotImplemented

    def get_name(self):
        return str(self._nurbs_srf)

# ======================================================================================================================
class controlProjSurface(object):
    """ projection surface constraining on which the movement area of locator_data
    projected from the movement of joints on the control data curves
    """

    def get_locator_row_ids(self):
        """
        :return: a list of all identity characters of rows of locators, e.g. ['A', 'B', 'C']
        """
        return self._locator_dict.keys()
    def get_locator_col_ids(self, row_id):
        """
        :param row_id: the identity character of a locator row, e.g. 'A'
        :return: a list of all identity numbers of locators belonging to this projection surface
        """
        assert row_id in self._locator_dict.keys()
        return self._locator_dict[row_id].keys()

    def get_locator_info(self, row_id, col_id):
        """
        :param row_id: the locator row identity character, starts from 'A'
        :param col_id: the locator column identity number, starts from 1
        :return: a tuple of the format (locator's name, bind joint's name, pointOnSurfaceInfo node's name)
        """
        if row_id not in self._locator_dict.keys():
            cmds.warning('[controlProjSurface] Try to access the locator of the row whose row_id does not exist.')
            return None
        if col_id not in self._locator_dict[row_id].keys():
            cmds.warning('[controlProjSurface] Try to access the locator of the column whose col_id does not exist.')
            return None

        return self._locator_dict[row_id][col_id]

    def __init__(self,
                 name_prefix = '',
                 name = 'control_projection_plane',
                 degree = 1,
                 patchesU = 4,
                 patchesV = 6,
                 translation = [0.0, 0.0, 0.0],
                 rotation = [0.0, 0.0, 0.0],
                 scale = [1.0, 1.0, 1.0],
                 mirror = [1, 1, 1],
                 cv_list = [],
                 locator_data = [],
                 locator_scale = [1, 1, 1],
                 bind_joint_data = {},
                 bind_joint_color = COLOR_INDEX_DARK_WHITE):
        """
        :param cv_list: A list of CV coordinates for the NURBS plane to construct;
                        Note that the maximum length of this list is (patchesU+1)*(patchesV+1).
        """

        # Member Variable Definitions ----------------------------------------------------------------------------------
        # NURBS surface construction parameters
        self._degree = degree
        self._patchesU = patchesU
        self._patchesV = patchesV

        self._cv_coords = []
        self._nurbs_srf = None

        # locator_data pinned on the projection surface
        # The 2-dimensional dictionary format is:
        # {row_id: {col_id: (locator's name, bind joint's name, pointOnSurfaceInfo node's name)}}
        # e.g. {'A': {1: ('fm_eyelidMask_RU_A1_loc', 'fm_eyelidMask_RU_A1_bind', 'fm_eyelidMask_RU_A1_loc_ptOnSrf')}}
        self._locator_dict = {}
        # ---------------------------------------------------------------------------------- Member Variable Definitions

        assert len(cv_list) <= (patchesU+1) * (patchesV+1)

        self._nurbs_srf = cmds.nurbsPlane(degree=self._degree,
                                          patchesU=self._patchesU,
                                          patchesV=self._patchesV)[0]   # Note the [0] indexing
        if len(cv_list) > 0:
            self._cv_coords = cv_list

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
        # if mirror[0] < 0:
        #     cmds.reverseSurface(self._nurbs_srf, direction=0) # "0" means "U"

        self._nurbs_srf = cmds.rename(self._nurbs_srf, name_prefix+'_'+name)
        # cmds.toggle(self._nurbs_srf, template=True)
        cmds.select(deselect=True)

        # Set display attributes.
        cmds.select(self._nurbs_srf, replace=True)
        cmds.sets(edit=True, forceElement=PROJ_SRF_SHADER+'_SG')
        cmds.select(deselect=True)

        cmds.setAttr(self._nurbs_srf+'.overrideEnabled', True)
        cmds.setAttr(self._nurbs_srf+'.overrideColor', PROJ_SURFACE_COLOR_INDEX)
        cmds.toggle(self._nurbs_srf, controlVertex=True)

        # Create the locator belongs to this projection surface, then use pointOnSurface
        for loc_dict in locator_data:
            loc_id = loc_dict['id'].split('_')
            loc_row_id = loc_id[0]
            loc_col_id = loc_id[1]
            loc_name = loc_dict['name']
            loc_param_uv = loc_dict['pt_on_srf_param_UV']

            loc = cmds.spaceLocator(name=name_prefix+'_'+loc_name)[0]
            assert cmds.objExists(loc+'Shape')
            for idx, axis in {0:'X', 1:'Y', 2:'Z'}.items():
                cmds.setAttr(loc+'Shape.localScale'+axis, locator_scale[idx])

            cmds.setAttr(loc+'.overrideEnabled', True)
            cmds.setAttr(loc+'.overrideColor', PROJ_SURFACE_LOC_COLOR_INDEX)

            pt_on_srf_info_node = cmds.createNode('pointOnSurfaceInfo', name=name_prefix+'_'+loc_name+'_ptOnSrf')
            cmds.setAttr(pt_on_srf_info_node+'.parameterU', loc_param_uv[0])
            cmds.setAttr(pt_on_srf_info_node+'.parameterV', loc_param_uv[1])
            cmds.connectAttr(self._nurbs_srf+'.worldSpace[0]', pt_on_srf_info_node+'.inputSurface')
            cmds.connectAttr(pt_on_srf_info_node+'.position', loc+'.translate')

            cmds.select(deselect=True)

            # Create a joint to pin this locator onto the target skinning mesh.
            bind_jnt_data_keys = bind_joint_data.keys()
            assert 'suffix' in bind_jnt_data_keys
            assert 'radius' in bind_jnt_data_keys

            bind_jnt_name = name_prefix + '_' + loc_name.rsplit('_', 1)[0] + '_' + bind_joint_data['suffix']
            bind_jnt = cmds.joint(name=bind_jnt_name, radius=bind_joint_data['radius'])

            cmds.setAttr(bind_jnt+'.overrideEnabled', True)
            cmds.setAttr(bind_jnt+'.overrideColor', bind_joint_color)

            cmds.parent(bind_jnt, loc)
            cmds.xform(bind_jnt, translation=[0, 0, 0])

            if loc_row_id in self._locator_dict.keys():
                self._locator_dict[str(loc_row_id)][int(loc_col_id)] = (loc, bind_jnt, pt_on_srf_info_node)
            else:
                self._locator_dict[str(loc_row_id)] = {int(loc_col_id): (loc, bind_jnt, pt_on_srf_info_node)}

        # # Bind the projection surface to the created joints.
        # cmds.select(deselect=True)
        # for loc_row_id in self._locator_dict.keys():
        #     loc_col_id_list = self.get_locator_col_ids(loc_row_id)
        #     for loc_col_id in loc_col_id_list:
        #         loc_info = self.get_locator_info(loc_row_id, loc_col_id)
        #         cmds.select(loc_info[1], add=True)
        # cmds.select(self._nurbs_srf, add=True)
        #
        # skincluster_node = cmds.skinCluster(toSelectedBones=True)
        # cmds.rename(skincluster_node, self._nurbs_srf+'_skinCluster')


    def __repr__(self):
        return NotImplemented

    def get_name(self):
        return str(self._nurbs_srf)