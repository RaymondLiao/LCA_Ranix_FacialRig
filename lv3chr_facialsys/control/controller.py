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

    _degree = 1
    _nurbs_crv = None
    _ofs_grp = None

    def __init__(self, name='controller',
                 degree=1, points=[],
                 color=COLOR_INDEX_YELLOW,
                 translation_ofs=[0, 0, 0],
                 translation=[0, 0, 0]):

        self._degree = degree
        assert len(points) > 0

        self._ofs_grp = cmds.group(name=name+'_ofs', empty=True)
        cmds.xform(self._ofs_grp, translation=translation_ofs)

        self._nurbs_crv = cmds.curve(degree=self._degree,
                                     point=points)
        cmds.parent(self._nurbs_crv, self._ofs_grp)
        cmds.xform(self._nurbs_crv, translation=translation)
        self._nurbs_crv = cmds.rename(self._nurbs_crv, name)

        cmds.setAttr(self._nurbs_crv+'.overrideEnabled', True)
        cmds.setAttr(self._nurbs_crv+'.overrideColor', color)

        cmds.select(deselect=True)

    def __repr__(self):
        return NotImplemented

    def get_name(self):
        return str(self._nurbs_crv)

    def get_offset_group(self):
        return str(self._ofs_grp)