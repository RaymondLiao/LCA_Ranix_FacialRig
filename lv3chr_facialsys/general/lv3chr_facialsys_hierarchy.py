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
        return _child_nodes.copy()

    def setup_group_hierarchy(self):

        cmds.group(name=self._group_name, empty=True)

        for child_node in self._child_nodes:
            # assert type(child_node) is groupTree

            # Recursively construct all child node's hierarchy
            child_node.setup_group_hierarchy()

            cmds.parent(child_node.get_group_name(), self._group_name)

# eyelid rig group hierarchy ------------------------------
eyelid_ctrlcrv_RU_grp = groupTree('fm_eyelidProject_RU_grp')
eyelid_ctrlcrv_RD_grp = groupTree('fm_eyelidProject_RD_grp')
eyelid_ctrlcrv_R_grp = groupTree('fm_eyelidProject_R_grp', [eyelid_ctrlcrv_RU_grp, eyelid_ctrlcrv_RD_grp])

eyelid_ctrlcrv_LU_grp = groupTree('fm_eyelidProject_LU_grp')
eyelid_ctrlcrv_LD_grp = groupTree('fm_eyelidProject_LD_grp')
eyelid_ctrlcrv_L_grp = groupTree('fm_eyelidProject_L_grp', [eyelid_ctrlcrv_LU_grp, eyelid_ctrlcrv_LD_grp])

eyelid_projsrf_RU_grp = groupTree('fm_eyelidMask_RU_grp')
eyelid_projsrf_RD_grp = groupTree('fm_eyelidMask_RD_grp')
eyelid_projsrf_R_grp = groupTree('fm_eyelidMask_R_grp', [eyelid_projsrf_RU_grp, eyelid_projsrf_RD_grp])

eyelid_projsrf_LU_grp = groupTree('fm_eyelidMask_LU_grp')
eyelid_projsrf_LD_grp = groupTree('fm_eyelidMask_LD_grp')
eyelid_projsrf_L_grp = groupTree('fm_eyelidMask_L_grp', [eyelid_projsrf_LU_grp, eyelid_projsrf_LD_grp])

eyelid_grp = groupTree('eyelid_grp', [eyelid_ctrlcrv_R_grp, eyelid_ctrlcrv_L_grp,
                                     eyelid_projsrf_R_grp, eyelid_projsrf_L_grp])