#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# File Name: contrl_crv.py
# Author: Sheng (Raymond) Liao
# Date: October 2021
#

"""
A module containing the definitions of control curves.
"""

import warnings
import maya.cmds as cmds

class controlCurve(object):
    """ Control Curves are used to transit the translation of
    locators binding joints on the projected surface.
    """

