#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# File Name: standalone_util.geometry.py
# Author: Sheng (Raymond) Liao
# Date: January 2022
#

"""
A module to query geometry information
"""

import maya.cmds as cmds

def get_nurbs_srf_CVs():
    """
    :return: a string containing the control vertices' coordinates of a selected NURBS surface
    stored in a list of dictionary, formatted in [{"u, v": [x, y, z]}], which will be used by
    the Projection Surface data JSON document to re-construct the surface
    """
    nurbs_srf = cmds.ls(selection=True)[0]
    nurbs_srf_spanU = cmds.getAttr(nurbs_srf + '.spansU')
    nurbs_srf_spanV = cmds.getAttr(nurbs_srf + '.spansV')

    nurbs_srf_CVs = ''

    for idx_u in range(nurbs_srf_spanU + 1):
        for idx_v in range(nurbs_srf_spanV + 1):
            cv_coord = cmds.getAttr(nurbs_srf + '.cv[{0}][{1}]'.format(idx_u, idx_v))[0]
            cv_coord_x = round(float(cv_coord[0]), 3)
            cv_coord_y = round(float(cv_coord[1]), 3)
            cv_coord_z = round(float(cv_coord[2]), 3)
            nurbs_srf_CVs += '{{"{0},{1}": [{2:.3f}, {3}, {4}]}},\n'.format(idx_u, idx_v,
                                                                          cv_coord_x, cv_coord_y, cv_coord_z)
        nurbs_srf_CVs += '\n'

    nurbs_srf_CVs = nurbs_srf_CVs[:-3]  # Get rid of the trailing two '\n' and a ','
    # print(nurbs_srf_CVs)

    return nurbs_srf_CVs

def get_nurbs_crv_CVs():
    nurbs_crv = cmds.ls(selection=True)[0]
    nurbs_crv_span = cmds.getAttr(nurbs_crv + '.spans')

    nurbs_crv_CVs = ''

    for idx in range(nurbs_crv_span + 1):
        cv_coord = cmds.getAttr(nurbs_crv + '.cv[{}]'.format(idx))[0]
        cv_coord_x = round(float(cv_coord[0]), 3)
        cv_coord_y = round(float(cv_coord[1]), 3)
        cv_coord_z = round(float(cv_coord[2]), 3)
        nurbs_crv_CVs += '[{0}, {1}, {2}],\n'.format(cv_coord_x, cv_coord_y, cv_coord_z)

    return nurbs_crv_CVs

def get_translation():
    sel_trans = cmds.ls(sl=True)[0]

    sel_trans = cmds.getAttr(sel_trans + '.translate')[0]
    sel_trans_x = round(float(sel_trans[0]), 3)
    sel_trans_y = round(float(sel_trans[1]), 3)
    sel_trans_z = round(float(sel_trans[2]), 3)
    cmds.warning('[{0}, {1}, {2}],\n'.format(sel_trans_x, sel_trans_y, sel_trans_z))