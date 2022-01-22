#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# File Name: standalone_util.controller.py
# Author: Sheng (Raymond) Liao
# Date: January 2022
#

"""
A module to manipulate NURBS curve controllers
"""

import maya.cmds as cmds

def ctrl_add_offset(ctrl_grp=None):
    if None == ctrl_grp:
        sel_list = cmds.ls(sl=True)
        if len(sel_list) > 0:
            ctrl_grp = sel_list[0]

    ctrl_list = cmds.listRelatives(ctrl_grp, children=True)
    for ctrl in ctrl_list:
        ctrl_pos = cmds.getAttr(ctrl+'.translate')[0]
        ctrl_ofs = cmds.group(ctrl, name=ctrl.replace('ctrl', 'ofs'))
        cmds.xform(ctrl_ofs, translation=list(ctrl_pos))
        cmds.xform(ctrl, translation=[0, 0, 0])