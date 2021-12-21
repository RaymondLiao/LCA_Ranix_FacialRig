#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# File Name: hierarchy.py
# Author: Sheng (Raymond) Liao
# Date: October 2021
#

"""
A module containing group hierarchy information for the LCA third level character facial system
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
        cmds.group(name=self._group_name, empty=True)

        for child_node in self._child_nodes:
            # assert type(child_node) is groupTree

            # Recursively construct all child node's hierarchy
            child_node.setup_group_hierarchy()

            cmds.parent(child_node.get_group_name(), self._group_name)

# Eyelid Rig Group Hierarchy ====== ====================================================================================
eyelid_ctrlzone_prefix = 'fm_eyelidProject'
eyelid_projsrf_prefix = 'fm_eyelidMask'
# translation plane ----------------------------------------------------------------------------------------------------
eyelid_ctrl_RU_grp = groupTree(eyelid_ctrlzone_prefix + '_RU_ctrl_grp')
eyelid_ctrlzone_loc_RU_A_grp = groupTree(eyelid_ctrlzone_prefix + 'Point_RU_A_grp')
eyelid_ctrlzone_loc_RU_B_grp = groupTree(eyelid_ctrlzone_prefix + 'Point_RU_B_grp')
eyelid_ctrlzone_loc_RU_C_grp = groupTree(eyelid_ctrlzone_prefix + 'Point_RU_C_grp')
eyelid_ctrlzone_loc_RU_D_grp = groupTree(eyelid_ctrlzone_prefix + 'Point_RU_D_grp')
eyelid_ctrlzone_loc_RU_E_grp = groupTree(eyelid_ctrlzone_prefix + 'Point_RU_E_grp')
eyelid_ctrlzone_loc_RU_F_grp = groupTree(eyelid_ctrlzone_prefix + 'Point_RU_F_grp')

eyelid_ctrlzone_RU_grp = groupTree(eyelid_ctrlzone_prefix + '_RU_grp',
                                   [
                                       eyelid_ctrl_RU_grp,
                                       eyelid_ctrlzone_loc_RU_A_grp,
                                       eyelid_ctrlzone_loc_RU_B_grp,
                                       eyelid_ctrlzone_loc_RU_C_grp,
                                       eyelid_ctrlzone_loc_RU_D_grp,
                                       eyelid_ctrlzone_loc_RU_E_grp,
                                       eyelid_ctrlzone_loc_RU_F_grp
                                   ])

eyelid_ctrl_RD_grp = groupTree(eyelid_ctrlzone_prefix + '_RD_ctrl_grp')
eyelid_ctrlzone_loc_RD_A_grp = groupTree(eyelid_ctrlzone_prefix + 'Point_RD_A_grp')
eyelid_ctrlzone_loc_RD_B_grp = groupTree(eyelid_ctrlzone_prefix + 'Point_RD_B_grp')
eyelid_ctrlzone_loc_RD_C_grp = groupTree(eyelid_ctrlzone_prefix + 'Point_RD_C_grp')
eyelid_ctrlzone_loc_RD_D_grp = groupTree(eyelid_ctrlzone_prefix + 'Point_RD_D_grp')
eyelid_ctrlzone_loc_RD_E_grp = groupTree(eyelid_ctrlzone_prefix + 'Point_RD_E_grp')
eyelid_ctrlzone_loc_RD_F_grp = groupTree(eyelid_ctrlzone_prefix + 'Point_RD_F_grp')

eyelid_ctrlzone_RD_grp = groupTree(eyelid_ctrlzone_prefix + '_RD_grp',
                                   [
                                       eyelid_ctrl_RD_grp,
                                       eyelid_ctrlzone_loc_RD_A_grp,
                                       eyelid_ctrlzone_loc_RD_B_grp,
                                       eyelid_ctrlzone_loc_RD_C_grp,
                                       eyelid_ctrlzone_loc_RD_D_grp,
                                       eyelid_ctrlzone_loc_RD_E_grp,
                                       eyelid_ctrlzone_loc_RD_F_grp
                                   ])

eyelid_ctrlzone_R_grp = groupTree(eyelid_ctrlzone_prefix + '_R_grp',
                                  [
                                      eyelid_ctrlzone_RU_grp,
                                      eyelid_ctrlzone_RD_grp
                                  ])

eyelid_ctrl_LU_grp = groupTree(eyelid_ctrlzone_prefix + '_LU_ctrl_grp')
eyelid_ctrlzone_loc_LU_A_grp = groupTree(eyelid_ctrlzone_prefix + 'Point_LU_A_grp')
eyelid_ctrlzone_loc_LU_B_grp = groupTree(eyelid_ctrlzone_prefix + 'Point_LU_B_grp')
eyelid_ctrlzone_loc_LU_C_grp = groupTree(eyelid_ctrlzone_prefix + 'Point_LU_C_grp')
eyelid_ctrlzone_loc_LU_D_grp = groupTree(eyelid_ctrlzone_prefix + 'Point_LU_D_grp')
eyelid_ctrlzone_loc_LU_E_grp = groupTree(eyelid_ctrlzone_prefix + 'Point_LU_E_grp')
eyelid_ctrlzone_loc_LU_F_grp = groupTree(eyelid_ctrlzone_prefix + 'Point_LU_F_grp')


eyelid_ctrlzone_LU_grp = groupTree(eyelid_ctrlzone_prefix + '_LU_grp',
                                   [
                                       eyelid_ctrl_LU_grp,
                                       eyelid_ctrlzone_loc_LU_A_grp,
                                       eyelid_ctrlzone_loc_LU_B_grp,
                                       eyelid_ctrlzone_loc_LU_C_grp,
                                       eyelid_ctrlzone_loc_LU_D_grp,
                                       eyelid_ctrlzone_loc_LU_E_grp,
                                       eyelid_ctrlzone_loc_LU_F_grp
                                   ])

eyelid_ctrl_LD_grp = groupTree(eyelid_ctrlzone_prefix + '_LD_ctrl_grp')
eyelid_ctrlzone_loc_LD_A_grp = groupTree(eyelid_ctrlzone_prefix + 'Point_LD_A_grp')
eyelid_ctrlzone_loc_LD_B_grp = groupTree(eyelid_ctrlzone_prefix + 'Point_LD_B_grp')
eyelid_ctrlzone_loc_LD_C_grp = groupTree(eyelid_ctrlzone_prefix + 'Point_LD_C_grp')
eyelid_ctrlzone_loc_LD_D_grp = groupTree(eyelid_ctrlzone_prefix + 'Point_LD_D_grp')
eyelid_ctrlzone_loc_LD_E_grp = groupTree(eyelid_ctrlzone_prefix + 'Point_LD_E_grp')
eyelid_ctrlzone_loc_LD_F_grp = groupTree(eyelid_ctrlzone_prefix + 'Point_LD_F_grp')

eyelid_ctrlzone_LD_grp = groupTree(eyelid_ctrlzone_prefix + '_LD_grp',
                                   [
                                       eyelid_ctrl_LD_grp,
                                       eyelid_ctrlzone_loc_LD_A_grp,
                                       eyelid_ctrlzone_loc_LD_B_grp,
                                       eyelid_ctrlzone_loc_LD_C_grp,
                                       eyelid_ctrlzone_loc_LD_D_grp,
                                       eyelid_ctrlzone_loc_LD_E_grp,
                                       eyelid_ctrlzone_loc_LD_F_grp
                                   ])

eyelid_ctrlzone_L_grp = groupTree(eyelid_ctrlzone_prefix + '_L_grp',
                                  [
                                      eyelid_ctrlzone_LU_grp,
                                      eyelid_ctrlzone_LD_grp
                                  ])

# projection surface ---------------------------------------------------------------------------------------------------
eyelid_projsrf_loc_RU_A_grp = groupTree(eyelid_projsrf_prefix+'_RU_A_grp')
eyelid_projsrf_loc_RU_B_grp = groupTree(eyelid_projsrf_prefix+'_RU_B_grp')
eyelid_projsrf_loc_RU_C_grp = groupTree(eyelid_projsrf_prefix+'_RU_C_grp')
eyelid_projsrf_loc_RU_D_grp = groupTree(eyelid_projsrf_prefix+'_RU_D_grp')
eyelid_projsrf_loc_RU_E_grp = groupTree(eyelid_projsrf_prefix+'_RU_E_grp')
eyelid_projsrf_loc_RU_F_grp = groupTree(eyelid_projsrf_prefix+'_RU_F_grp')

eyelid_projsrf_RU_grp = groupTree(eyelid_projsrf_prefix+'_RU_grp',
                                  [
                                      eyelid_projsrf_loc_RU_A_grp,
                                      eyelid_projsrf_loc_RU_B_grp,
                                      eyelid_projsrf_loc_RU_C_grp,
                                      eyelid_projsrf_loc_RU_D_grp,
                                      eyelid_projsrf_loc_RU_E_grp,
                                      eyelid_projsrf_loc_RU_F_grp
                                  ])

eyelid_projsrf_loc_RD_A_grp = groupTree(eyelid_projsrf_prefix+'_RD_A_grp')
eyelid_projsrf_loc_RD_B_grp = groupTree(eyelid_projsrf_prefix+'_RD_B_grp')
eyelid_projsrf_loc_RD_C_grp = groupTree(eyelid_projsrf_prefix+'_RD_C_grp')
eyelid_projsrf_loc_RD_D_grp = groupTree(eyelid_projsrf_prefix+'_RD_D_grp')
eyelid_projsrf_loc_RD_E_grp = groupTree(eyelid_projsrf_prefix+'_RD_E_grp')
eyelid_projsrf_loc_RD_F_grp = groupTree(eyelid_projsrf_prefix+'_RD_F_grp')

eyelid_projsrf_RD_grp = groupTree(eyelid_projsrf_prefix+'_RD_grp',
                                  [
                                      eyelid_projsrf_loc_RD_A_grp,
                                      eyelid_projsrf_loc_RD_B_grp,
                                      eyelid_projsrf_loc_RD_C_grp,
                                      eyelid_projsrf_loc_RD_D_grp,
                                      eyelid_projsrf_loc_RD_E_grp,
                                      eyelid_projsrf_loc_RD_F_grp
                                  ])

eyelid_projsrf_R_grp = groupTree(eyelid_projsrf_prefix+'_R_grp',
                                 [
                                     eyelid_projsrf_RU_grp,
                                     eyelid_projsrf_RD_grp
                                 ])

eyelid_projsrf_loc_LU_A_grp = groupTree(eyelid_projsrf_prefix+'_LU_A_grp')
eyelid_projsrf_loc_LU_B_grp = groupTree(eyelid_projsrf_prefix+'_LU_B_grp')
eyelid_projsrf_loc_LU_C_grp = groupTree(eyelid_projsrf_prefix+'_LU_C_grp')
eyelid_projsrf_loc_LU_D_grp = groupTree(eyelid_projsrf_prefix+'_LU_D_grp')
eyelid_projsrf_loc_LU_E_grp = groupTree(eyelid_projsrf_prefix+'_LU_E_grp')
eyelid_projsrf_loc_LU_F_grp = groupTree(eyelid_projsrf_prefix+'_LU_F_grp')

eyelid_projsrf_LU_grp = groupTree(eyelid_projsrf_prefix+'_LU_grp',
                                  [
                                      eyelid_projsrf_loc_LU_A_grp,
                                      eyelid_projsrf_loc_LU_B_grp,
                                      eyelid_projsrf_loc_LU_C_grp,
                                      eyelid_projsrf_loc_LU_D_grp,
                                      eyelid_projsrf_loc_LU_E_grp,
                                      eyelid_projsrf_loc_LU_F_grp
                                  ])

eyelid_projsrf_loc_LD_A_grp = groupTree(eyelid_projsrf_prefix+'_LD_A_grp')
eyelid_projsrf_loc_LD_B_grp = groupTree(eyelid_projsrf_prefix+'_LD_B_grp')
eyelid_projsrf_loc_LD_C_grp = groupTree(eyelid_projsrf_prefix+'_LD_C_grp')
eyelid_projsrf_loc_LD_D_grp = groupTree(eyelid_projsrf_prefix+'_LD_D_grp')
eyelid_projsrf_loc_LD_E_grp = groupTree(eyelid_projsrf_prefix+'_LD_E_grp')
eyelid_projsrf_loc_LD_F_grp = groupTree(eyelid_projsrf_prefix+'_LD_F_grp')

eyelid_projsrf_LD_grp = groupTree(eyelid_projsrf_prefix+'_LD_grp',
                                  [
                                      eyelid_projsrf_loc_LD_A_grp,
                                      eyelid_projsrf_loc_LD_B_grp,
                                      eyelid_projsrf_loc_LD_C_grp,
                                      eyelid_projsrf_loc_LD_D_grp,
                                      eyelid_projsrf_loc_LD_E_grp,
                                      eyelid_projsrf_loc_LD_F_grp
                                  ])

eyelid_projsrf_L_grp = groupTree(eyelid_projsrf_prefix+'_L_grp',
                                 [
                                     eyelid_projsrf_LU_grp,
                                     eyelid_projsrf_LD_grp
                                 ])

# eyelid zone sub-master group -----------------------------------------------------------------------------------------
eyelid_grp = groupTree('eyelid_grp',
                       [
                           eyelid_ctrlzone_R_grp,
                           eyelid_ctrlzone_L_grp,
                           eyelid_projsrf_R_grp,
                           eyelid_projsrf_L_grp
                       ])

# Eyebrow Rig Group Hierarchy ==========================================================================================
eyebrow_ctrlzone_prefix = 'fm_eyebrowProject'
eyebrow_projsrf_prefix = 'fm_eyebrowMask'
# translation plane ----------------------------------------------------------------------------------------------------
eyebrow_ctrl_M_grp = groupTree(eyebrow_ctrlzone_prefix + '_M_ctrl_grp')
eyebrow_ctrlzone_loc_M_A_grp = groupTree(eyebrow_ctrlzone_prefix + 'Point_M_A_grp')
eyebrow_ctrlzone_loc_M_B_grp = groupTree(eyebrow_ctrlzone_prefix + 'Point_M_B_grp')
eyebrow_ctrlzone_loc_M_C_grp = groupTree(eyebrow_ctrlzone_prefix + 'Point_M_C_grp')

eyebrow_ctrlzone_M_grp = groupTree(eyebrow_ctrlzone_prefix + '_M_grp',
                                   [
                                       eyebrow_ctrl_M_grp,
                                       eyebrow_ctrlzone_loc_M_A_grp,
                                       eyebrow_ctrlzone_loc_M_B_grp,
                                       eyebrow_ctrlzone_loc_M_C_grp
                                   ])

# projection surface ---------------------------------------------------------------------------------------------------
eyebrow_projsrf_loc_M_UD_A_grp = groupTree(eyebrow_projsrf_prefix+'_M_UD_A_grp')
eyebrow_projsrf_loc_M_UD_B_grp = groupTree(eyebrow_projsrf_prefix+'_M_UD_B_grp')
eyebrow_projsrf_loc_M_UD_C_grp = groupTree(eyebrow_projsrf_prefix+'_M_UD_C_grp')

eyebrow_projsrf_loc_M_FB_grp = groupTree(eyebrow_projsrf_prefix+'_M_FB_grp')

eyebrow_projsrf_M_grp = groupTree(eyebrow_projsrf_prefix+'_M_grp',
                                  [
                                      eyebrow_projsrf_loc_M_UD_A_grp,
                                      eyebrow_projsrf_loc_M_UD_B_grp,
                                      eyebrow_projsrf_loc_M_UD_C_grp,
                                      eyebrow_projsrf_loc_M_FB_grp
                                  ])

# eyebrow zone sub-master group ----------------------------------------------------------------------------------------
eyebrow_grp = groupTree('eyebrow_grp',
                        [
                            eyebrow_ctrlzone_M_grp,
                            eyebrow_projsrf_M_grp
                        ])

# Mouth and Cheek Rig Group Hierarchy ====== ===========================================================================
mouth_ctrlzone_prefix = 'fm_mouthProject'
mouth_projsrf_prefix = 'fm_mouthMask'
cheek_ctrlzone_prefix = 'fm_cheekProject'
cheek_projsrf_prefix = 'fm_cheekMask'
# translation plane ----------------------------------------------------------------------------------------------------
# Mouth Control Zone
mouth_ctrl_MU_grp = groupTree(mouth_ctrlzone_prefix + '_MU_ctrl_grp')
mouth_ctrlzone_loc_MU_A_grp = groupTree(mouth_ctrlzone_prefix + 'Point_MU_A_grp')
mouth_ctrlzone_loc_MU_B_grp = groupTree(mouth_ctrlzone_prefix + 'Point_MU_B_grp')
mouth_ctrlzone_loc_MU_C_grp = groupTree(mouth_ctrlzone_prefix + 'Point_MU_C_grp')
mouth_ctrlzone_loc_MU_D_grp = groupTree(mouth_ctrlzone_prefix + 'Point_MU_D_grp')
mouth_ctrlzone_loc_MU_E_grp = groupTree(mouth_ctrlzone_prefix + 'Point_MU_E_grp')

mouth_ctrlzone_MU_grp = groupTree(mouth_ctrlzone_prefix + '_MU_grp',
                                  [
                                     mouth_ctrl_MU_grp,
                                     mouth_ctrlzone_loc_MU_A_grp,
                                     mouth_ctrlzone_loc_MU_B_grp,
                                     mouth_ctrlzone_loc_MU_C_grp,
                                     mouth_ctrlzone_loc_MU_D_grp,
                                     mouth_ctrlzone_loc_MU_E_grp
                                 ])

mouth_ctrl_MD_grp = groupTree(mouth_ctrlzone_prefix + '_MD_ctrl_grp')
mouth_ctrlzone_loc_MD_A_grp = groupTree(mouth_ctrlzone_prefix + 'Point_MD_A_grp')
mouth_ctrlzone_loc_MD_B_grp = groupTree(mouth_ctrlzone_prefix + 'Point_MD_B_grp')
mouth_ctrlzone_loc_MD_C_grp = groupTree(mouth_ctrlzone_prefix + 'Point_MD_C_grp')
mouth_ctrlzone_loc_MD_D_grp = groupTree(mouth_ctrlzone_prefix + 'Point_MD_D_grp')
mouth_ctrlzone_loc_MD_E_grp = groupTree(mouth_ctrlzone_prefix + 'Point_MD_E_grp')

mouth_ctrlzone_MD_grp = groupTree(mouth_ctrlzone_prefix + '_MD_grp',
                                 [
                                     mouth_ctrl_MD_grp,
                                     mouth_ctrlzone_loc_MD_A_grp,
                                     mouth_ctrlzone_loc_MD_B_grp,
                                     mouth_ctrlzone_loc_MD_C_grp,
                                     mouth_ctrlzone_loc_MD_E_grp,
                                     mouth_ctrlzone_loc_MD_E_grp
                                 ])

# Cheek Control Zone
cheek_ctrl_L_grp = groupTree(cheek_ctrlzone_prefix + '_L_ctrl_grp')
cheek_ctrlzone_loc_L_A_grp = groupTree(cheek_ctrlzone_prefix + '.Point_L_A_grp')
cheek_ctrlzone_loc_L_B_grp = groupTree(cheek_ctrlzone_prefix + '.Point_L_B_grp')
cheek_ctrlzone_loc_L_C_grp = groupTree(cheek_ctrlzone_prefix + '.Point_L_C_grp')
cheek_ctrlzone_loc_L_D_grp = groupTree(cheek_ctrlzone_prefix + '.Point_L_D_grp')
cheek_ctrlzone_loc_L_E_grp = groupTree(cheek_ctrlzone_prefix + '.Point_L_E_grp')

cheek_ctrlzone_L_grp = groupTree(cheek_ctrlzone_prefix + '_L_grp',
                                 [
                                     cheek_ctrl_L_grp,
                                     cheek_ctrlzone_loc_L_A_grp,
                                     cheek_ctrlzone_loc_L_B_grp,
                                     cheek_ctrlzone_loc_L_C_grp,
                                     cheek_ctrlzone_loc_L_D_grp,
                                     cheek_ctrlzone_loc_L_E_grp
                                 ])

cheek_ctrl_R_grp = groupTree(cheek_ctrlzone_prefix + '_R_ctrl_grp')
cheek_ctrlzone_loc_R_A_grp = groupTree(cheek_ctrlzone_prefix + '.Point_R_A_grp')
cheek_ctrlzone_loc_R_B_grp = groupTree(cheek_ctrlzone_prefix + '.Point_R_B_grp')
cheek_ctrlzone_loc_R_C_grp = groupTree(cheek_ctrlzone_prefix + '.Point_R_C_grp')
cheek_ctrlzone_loc_R_D_grp = groupTree(cheek_ctrlzone_prefix + '.Point_R_D_grp')
cheek_ctrlzone_loc_R_E_grp = groupTree(cheek_ctrlzone_prefix + '.Point_R_E_grp')

cheek_ctrlzone_R_grp = groupTree(cheek_ctrlzone_prefix + '_R_grp',
                                 [
                                     cheek_ctrlzone_loc_R_A_grp,
                                     cheek_ctrlzone_loc_R_B_grp,
                                     cheek_ctrlzone_loc_R_C_grp,
                                     cheek_ctrlzone_loc_R_D_grp,
                                     cheek_ctrlzone_loc_R_E_grp
                                 ])

# projection surface ---------------------------------------------------------------------------------------------------
# Mouth Control Zone
mouth_projsrf_loc_MU_A_grp = groupTree(mouth_projsrf_prefix + '_MU_A_grp')
mouth_projsrf_loc_MU_B_grp = groupTree(mouth_projsrf_prefix + '_MU_B_grp')
mouth_projsrf_loc_MU_C_grp = groupTree(mouth_projsrf_prefix + '_MU_C_grp')
mouth_projsrf_loc_MU_D_grp = groupTree(mouth_projsrf_prefix + '_MU_D_grp')
mouth_projsrf_loc_MU_E_grp = groupTree(mouth_projsrf_prefix + '_MU_E_grp')
mouth_projsrf_loc_MD_A_grp = groupTree(mouth_projsrf_prefix + '_MD_A_grp')
mouth_projsrf_loc_MD_B_grp = groupTree(mouth_projsrf_prefix + '_MD_B_grp')
mouth_projsrf_loc_MD_C_grp = groupTree(mouth_projsrf_prefix + '_MD_C_grp')
mouth_projsrf_loc_MD_D_grp = groupTree(mouth_projsrf_prefix + '_MD_D_grp')
mouth_projsrf_loc_MD_E_grp = groupTree(mouth_projsrf_prefix + '_MD_E_grp')
mouth_projsrf_loc_MD_F_grp = groupTree(mouth_projsrf_prefix + '_MD_F_grp')

mouth_projsrf_UDLR_grp = groupTree(mouth_projsrf_prefix + '_UDLR_grp',
                                   [
                                       mouth_projsrf_loc_MU_A_grp,
                                       mouth_projsrf_loc_MU_B_grp,
                                       mouth_projsrf_loc_MU_C_grp,
                                       mouth_projsrf_loc_MU_D_grp,
                                       mouth_projsrf_loc_MU_E_grp,
                                       mouth_projsrf_loc_MD_A_grp,
                                       mouth_projsrf_loc_MD_B_grp,
                                       mouth_projsrf_loc_MD_C_grp,
                                       mouth_projsrf_loc_MD_D_grp,
                                       mouth_projsrf_loc_MD_E_grp,
                                       mouth_projsrf_loc_MD_F_grp
                                   ])

# Cheek Control Zone
cheek_projsrf_loc_L_A_grp = groupTree(cheek_projsrf_prefix + '_L_A_grp')
cheek_projsrf_loc_L_B_grp = groupTree(cheek_projsrf_prefix + '_L_B_grp')
cheek_projsrf_loc_L_C_grp = groupTree(cheek_projsrf_prefix + '_L_C_grp')
cheek_projsrf_loc_L_D_grp = groupTree(cheek_projsrf_prefix + '_L_D_grp')
cheek_projsrf_loc_L_E_grp = groupTree(cheek_projsrf_prefix + '_L_E_grp')
cheek_projsrf_loc_R_A_grp = groupTree(cheek_projsrf_prefix + '_R_A_grp')
cheek_projsrf_loc_R_B_grp = groupTree(cheek_projsrf_prefix + '_R_B_grp')
cheek_projsrf_loc_R_C_grp = groupTree(cheek_projsrf_prefix + '_R_C_grp')
cheek_projsrf_loc_R_D_grp = groupTree(cheek_projsrf_prefix + '_R_D_grp')
cheek_projsrf_loc_R_E_grp = groupTree(cheek_projsrf_prefix + '_R_E_grp')

# cheek_projsrf_UDLR_grp = groupTree(cheek_projsrf_prefix + '_' + )