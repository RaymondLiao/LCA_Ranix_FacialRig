#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# File Name: contrl_crv.py
# Author: Sheng (Raymond) Liao
# Date: October 2021
#

"""
A module containing the definitions of NURBS curve controller
"""

import warnings
import maya.cmds as cmds

from general import lv3chr_facialsys_config; reload(lv3chr_facialsys_config)
from general.lv3chr_facialsys_config import *

class controller(object):
    """ Controllers are NURBS curves used by animators to key the rig.
    """

    # _bind_jnt = None
    def get_bind_joint(self):
        assert None != self._bind_jnt
        return self._bind_jnt

    def __init__(self,
                 name = 'controller',
                 degree = 1,
                 points = [],
                 color = COLOR_INDEX_YELLOW,
                 translation_ofs = [0, 0, 0],
                 translation = [0, 0, 0],
                 lock_trans_axes = [],
                 lock_rot_axes = [],
                 bind_joint_data = {},
                 bind_joint_color = COLOR_INDEX_DARK_WHITE):

        # Member Variable Definitions ----------------------------------------------------------------------------------
        # Create a NURBS curve object as the controller UI.
        self._degree = degree
        self._nurbs_crv = None
        self._ofs_grp = None
        # ---------------------------------------------------------------------------------- Member Variable Definitions

        assert len(points) > 0

        self._ofs_grp = cmds.group(name=name+'_ofs', empty=True)
        cmds.xform(self._ofs_grp, translation=translation_ofs)

        nurbs_crv = cmds.curve(degree=self._degree,
                               point=points)
        cmds.parent(nurbs_crv, self._ofs_grp)
        cmds.xform(nurbs_crv, translation=translation)

        for axis in lock_trans_axes:
            assert axis in ['x', 'y', 'z']
            cmds.setAttr(nurbs_crv+'.t'+axis, lock=True)
        for axis in lock_rot_axes:
            assert axis in ['x', 'y', 'z']
            cmds.setAttr(nurbs_crv+'.r'+axis, lock=True)

        nurbs_crv = cmds.rename(nurbs_crv, name)

        cmds.setAttr(nurbs_crv+'.overrideEnabled', True)
        cmds.setAttr(nurbs_crv+'.overrideColor', color)

        self._nurbs_crv = nurbs_crv
        cmds.select(deselect=True)

        # Create a joint to bind this controller.
        bind_jnt_data_keys = bind_joint_data.keys()
        assert 'suffix' in bind_jnt_data_keys
        assert 'radius' in bind_jnt_data_keys

        bind_jnt_name = name.rsplit('_', 1)[0] + '_' + bind_joint_data['suffix']
        bind_jnt = cmds.joint(name=bind_jnt_name, radius=bind_joint_data['radius'])

        cmds.setAttr(bind_jnt+'.overrideEnabled', True)
        cmds.setAttr(bind_jnt+'.overrideColor', bind_joint_color)

        cmds.parent(bind_jnt, self._nurbs_crv)
        cmds.xform(bind_jnt, translation=[0, 0, 0])

        self._bind_jnt = bind_jnt

    def __repr__(self):
        return NotImplemented

    def get_name(self):
        return str(self._nurbs_crv)

    def get_offset_group(self):
        return str(self._ofs_grp)