#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# File Name: lv3chr_facialsys_hierarchy.py
# Author: Sheng (Raymond) Liao
# Date: October 2021
#

"""
A module containing group hierarchy information for the LCA level three character facial system
"""

import maya.cmds as cmds

class groupTree:

    def __init__(self, group_name='', child_nodes=[]):
        """
        :param group_node:string -- the name of the group
        """
        self._child_nodes = child_nodes
        self._group_name = group_name

    def get_group_name(self):
        return self._group_name

    def get_child_nodes(self):
        return self._child_nodes.copy()

    def setup_group_hierarchy(self):

        # Sometimes, Maya will repetitively establish this group hierarchy,
        # so we need to check if the group with the name already exists.
        if not cmds.objExists(self._group_name):
            cmds.group(name=self._group_name, empty=True)

        for child_node in self._child_nodes:
            # assert type(child_node) is groupTree

            # Recursively construct all child node's hierarchy
            try:
                child_node.setup_group_hierarchy()

                child_group_name = child_node.get_group_name()
                child_group_parent_list = cmds.listRelatives(child_group_name,
                                                             parent=True,
                                                             type='transform',
                                                             noIntermediate=True)

                # Sometimes, Maya will repetitively establish this group hierarchy,
                # so we need to check if the child groups have already been parented.
                if not (None != child_group_parent_list and self._group_name in child_group_parent_list):
                    cmds.parent(child_node.get_group_name(), self._group_name)
            except Exception as e:
                cmds.warning('Exception thrown during establishing the group hierarchy: {}'.format(str(e)))

# eyelid rig group hierarchy ===========================================================================================
eyelid_zone_prefix = 'fm_eyelidProject'
# translation plane ----------------------------------------------------------------------------------------------------
eyelid_ctrl_RU_grp = groupTree(eyelid_zone_prefix+'_RU_ctrl')
eyelid_ctrlcrv_loc_RU_A_grp = groupTree(eyelid_zone_prefix+'Point_RU_A_grp')
eyelid_ctrlcrv_loc_RU_B_grp = groupTree(eyelid_zone_prefix+'Point_RU_B_grp')
eyelid_ctrlcrv_loc_RU_C_grp = groupTree(eyelid_zone_prefix+'Point_RU_C_grp')
eyelid_ctrlcrv_loc_RU_D_grp = groupTree(eyelid_zone_prefix+'Point_RU_D_grp')

eyelid_ctrlcrv_RU_grp = groupTree(eyelid_zone_prefix+'_RU_grp',
                                  [
                                      eyelid_ctrl_RU_grp,
                                      eyelid_ctrlcrv_loc_RU_A_grp,
                                      eyelid_ctrlcrv_loc_RU_B_grp,
                                      eyelid_ctrlcrv_loc_RU_C_grp,
                                      eyelid_ctrlcrv_loc_RU_D_grp
                                  ])

eyelid_ctrl_RD_grp = groupTree(eyelid_zone_prefix+'_RD_ctrl')
eyelid_ctrlcrv_loc_RD_A_grp = groupTree(eyelid_zone_prefix+'Point_RD_A_grp')
eyelid_ctrlcrv_loc_RD_B_grp = groupTree(eyelid_zone_prefix+'Point_RD_B_grp')
eyelid_ctrlcrv_loc_RD_C_grp = groupTree(eyelid_zone_prefix+'Point_RD_C_grp')
eyelid_ctrlcrv_loc_RD_D_grp = groupTree(eyelid_zone_prefix+'Point_RD_D_grp')

eyelid_ctrlcrv_RD_grp = groupTree(eyelid_zone_prefix+'_RD_grp',
                                  [
                                      eyelid_ctrl_RD_grp,
                                      eyelid_ctrlcrv_loc_RD_A_grp,
                                      eyelid_ctrlcrv_loc_RD_B_grp,
                                      eyelid_ctrlcrv_loc_RD_C_grp,
                                      eyelid_ctrlcrv_loc_RD_D_grp
                                  ])

eyelid_ctrlcrv_R_grp = groupTree(eyelid_zone_prefix+'_R_grp',
                                 [
                                     eyelid_ctrlcrv_RU_grp,
                                     eyelid_ctrlcrv_RD_grp
                                 ])

eyelid_ctrl_LU_grp = groupTree(eyelid_zone_prefix+'_LU_ctrl')
eyelid_ctrlcrv_loc_LU_A_grp = groupTree(eyelid_zone_prefix+'Point_LU_A_grp')
eyelid_ctrlcrv_loc_LU_B_grp = groupTree(eyelid_zone_prefix+'Point_LU_B_grp')
eyelid_ctrlcrv_loc_LU_C_grp = groupTree(eyelid_zone_prefix+'Point_LU_C_grp')
eyelid_ctrlcrv_loc_LU_D_grp = groupTree(eyelid_zone_prefix+'Point_LU_D_grp')

eyelid_ctrlcrv_LU_grp = groupTree(eyelid_zone_prefix+'_LU_grp',
                                  [
                                      eyelid_ctrl_LU_grp,
                                      eyelid_ctrlcrv_loc_LU_A_grp,
                                      eyelid_ctrlcrv_loc_LU_B_grp,
                                      eyelid_ctrlcrv_loc_LU_C_grp,
                                      eyelid_ctrlcrv_loc_LU_D_grp
                                  ])

eyelid_ctrl_LD_grp = groupTree(eyelid_zone_prefix+'_LD_ctrl')
eyelid_ctrlcrv_loc_LD_A_grp = groupTree(eyelid_zone_prefix+'Point_LD_A_grp')
eyelid_ctrlcrv_loc_LD_B_grp = groupTree(eyelid_zone_prefix+'Point_LD_B_grp')
eyelid_ctrlcrv_loc_LD_C_grp = groupTree(eyelid_zone_prefix+'Point_LD_C_grp')
eyelid_ctrlcrv_loc_LD_D_grp = groupTree(eyelid_zone_prefix+'Point_LD_D_grp')

eyelid_ctrlcrv_LD_grp = groupTree(eyelid_zone_prefix+'_LD_grp',
                                  [
                                      eyelid_ctrl_LD_grp,
                                      eyelid_ctrlcrv_loc_LD_A_grp,
                                      eyelid_ctrlcrv_loc_LD_B_grp,
                                      eyelid_ctrlcrv_loc_LD_C_grp,
                                      eyelid_ctrlcrv_loc_LD_D_grp
                                  ])

eyelid_ctrlcrv_L_grp = groupTree(eyelid_zone_prefix+'_L_grp',
                                 [
                                     eyelid_ctrlcrv_LU_grp,
                                     eyelid_ctrlcrv_LD_grp
                                 ])

# projection surface ---------------------------------------------------------------------------------------------------
eyelid_projsrf_loc_RU_A_grp = groupTree('fm_eyelidMask_RU_A_grp')
eyelid_projsrf_loc_RU_B_grp = groupTree('fm_eyelidMask_RU_B_grp')
eyelid_projsrf_loc_RU_C_grp = groupTree('fm_eyelidMask_RU_C_grp')
eyelid_projsrf_loc_RU_D_grp = groupTree('fm_eyelidMask_RU_D_grp')

eyelid_projsrf_RU_grp = groupTree('fm_eyelidMask_RU_grp',
                                  [
                                      eyelid_projsrf_loc_RU_A_grp,
                                      eyelid_projsrf_loc_RU_B_grp,
                                      eyelid_projsrf_loc_RU_C_grp,
                                      eyelid_projsrf_loc_RU_D_grp
                                  ])

eyelid_projsrf_loc_RD_A_grp = groupTree('fm_eyelidMask_RD_A_grp')
eyelid_projsrf_loc_RD_B_grp = groupTree('fm_eyelidMask_RD_B_grp')
eyelid_projsrf_loc_RD_C_grp = groupTree('fm_eyelidMask_RD_C_grp')
eyelid_projsrf_loc_RD_D_grp = groupTree('fm_eyelidMask_RD_D_grp')

eyelid_projsrf_RD_grp = groupTree('fm_eyelidMask_RD_grp',
                                  [
                                      eyelid_projsrf_loc_RD_A_grp,
                                      eyelid_projsrf_loc_RD_B_grp,
                                      eyelid_projsrf_loc_RD_C_grp,
                                      eyelid_projsrf_loc_RD_D_grp
                                  ])

eyelid_projsrf_R_grp = groupTree('fm_eyelidMask_R_grp',
                                 [
                                     eyelid_projsrf_RU_grp,
                                     eyelid_projsrf_RD_grp
                                 ])

eyelid_projsrf_loc_LU_A_grp = groupTree('fm_eyelidMask_LU_A_grp')
eyelid_projsrf_loc_LU_B_grp = groupTree('fm_eyelidMask_LU_B_grp')
eyelid_projsrf_loc_LU_C_grp = groupTree('fm_eyelidMask_LU_C_grp')
eyelid_projsrf_loc_LU_D_grp = groupTree('fm_eyelidMask_LU_D_grp')

eyelid_projsrf_LU_grp = groupTree('fm_eyelidMask_LU_grp',
                                  [
                                      eyelid_projsrf_loc_LU_A_grp,
                                      eyelid_projsrf_loc_LU_B_grp,
                                      eyelid_projsrf_loc_LU_C_grp,
                                      eyelid_projsrf_loc_LU_D_grp
                                  ])

eyelid_projsrf_loc_LD_A_grp = groupTree('fm_eyelidMask_LD_A_grp')
eyelid_projsrf_loc_LD_B_grp = groupTree('fm_eyelidMask_LD_B_grp')
eyelid_projsrf_loc_LD_C_grp = groupTree('fm_eyelidMask_LD_C_grp')
eyelid_projsrf_loc_LD_D_grp = groupTree('fm_eyelidMask_LD_D_grp')

eyelid_projsrf_LD_grp = groupTree('fm_eyelidMask_LD_grp',
                                  [
                                      eyelid_projsrf_loc_LD_A_grp,
                                      eyelid_projsrf_loc_LD_B_grp,
                                      eyelid_projsrf_loc_LD_C_grp,
                                      eyelid_projsrf_loc_LD_D_grp
                                  ])

eyelid_projsrf_L_grp = groupTree('fm_eyelidMask_L_grp',
                                 [
                                     eyelid_projsrf_LU_grp,
                                     eyelid_projsrf_LD_grp
                                 ])

eyelid_grp = groupTree('eyelid_grp',
                       [
                           eyelid_ctrlcrv_R_grp,
                           eyelid_ctrlcrv_L_grp,
                           eyelid_projsrf_R_grp,
                           eyelid_projsrf_L_grp
                       ])