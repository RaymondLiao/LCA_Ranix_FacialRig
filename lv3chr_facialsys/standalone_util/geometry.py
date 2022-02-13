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
    nurbs_srf_spanU = cmds.getAttr(nurbs_srf+'.spansU')
    nurbs_srf_spanV = cmds.getAttr(nurbs_srf+'.spansV')

    nurbs_srf_CVs = ''

    for idx_u in range(nurbs_srf_spanU+1):
        for idx_v in range(nurbs_srf_spanV+1):
            cv_coord = cmds.getAttr(nurbs_srf+'.cv[{0}][{1}]'.format(idx_u, idx_v))[0]
            cv_coord_x = round(float(cv_coord[0]), 3)
            cv_coord_y = round(float(cv_coord[1]), 3)
            cv_coord_z = round(float(cv_coord[2]), 3)
            nurbs_srf_CVs += '{{"{0},{1}": [{2:.3f}, {3}, {4}]}},\n'.format(idx_u, idx_v,
                                                                          cv_coord_x, cv_coord_y, cv_coord_z)
        nurbs_srf_CVs += '\n'

    nurbs_srf_CVs = nurbs_srf_CVs[:-3]  # Get rid of the trailing two '\n' and a ','
    # cmds.warning(nurbs_srf_CVs)

    return nurbs_srf_CVs

def get_nurbs_crv_CVs():
    nurbs_crv = cmds.ls(selection=True)[0]
    nurbs_crv_span = cmds.getAttr(nurbs_crv+'.spans')

    nurbs_crv_CVs = ''

    for idx in range(nurbs_crv_span+1):
        cv_coord = cmds.getAttr(nurbs_crv+'.cv[{}]'.format(idx))[0]
        cv_coord_x = round(float(cv_coord[0]), 3)
        cv_coord_y = round(float(cv_coord[1]), 3)
        cv_coord_z = round(float(cv_coord[2]), 3)
        nurbs_crv_CVs += '[{0}, {1}, {2}],\n'.format(cv_coord_x, cv_coord_y, cv_coord_z)

    cmds.warning(nurbs_crv_CVs)
    return nurbs_crv_CVs

def get_translation_string():
    sel_transform = cmds.ls(sl=True)[0]

    sel_translation = cmds.getAttr(sel_transform+'.translate')[0]
    sel_translation_x = round(float(sel_translation[0]), 3)
    sel_translation_y = round(float(sel_translation[1]), 3)
    sel_translation_z = round(float(sel_translation[2]), 3)

    sel_translation_str = '[{0}, {1}, {2}], \n'.format(sel_translation_x, sel_translation_y, sel_translation_z)
    cmds.warning(sel_translation_str)
    return sel_translation_str

def copy_transform(translation=True, rotation=True, scale=False, delete_source=False):
    '''
    Copy the firstly selected transform node's data to the secondly selected one.
    :param translation: Copy the translation data
    :param rotation: Copy the rotation data
    :param scale: Copy the scale data
    :param delete_source: If delete the source transform node after copy its information
    :return: None
    '''
    sel_transforms = cmds.ls(sl=True)

    if len(sel_transforms) < 2:
        cmds.error('Must select a target transform node to copy the transform to.')
        return

    src_transform = sel_transforms[0]

    src_translation = cmds.getAttr(src_transform+'.translate')[0]
    src_translation_x = src_translation[0]
    src_translation_y = src_translation[1]
    src_translation_z = src_translation[2]

    src_rotation = cmds.getAttr(src_transform+'.rotate')[0]
    src_rotation_x = src_rotation[0]
    src_rotation_y = src_rotation[1]
    src_rotation_z = src_rotation[2]

    src_scale = cmds.getAttr(src_transform+'.scale')[0]
    src_scale_x = src_scale[0]
    src_scale_y = src_scale[1]
    src_scale_z = src_scale[2]

    tar_transform_list = sel_transforms[1:]
    for tar_transform in tar_transform_list:
        if translation:
            cmds.setAttr(tar_transform+'.translate', src_translation_x, src_translation_y, src_translation_z)
        if rotation:
            cmds.setAttr(tar_transform+'.rotate', src_rotation_x, src_rotation_y, src_rotation_z)
        if scale:
            cmds.setAttr(tar_transform+'.scale', src_scale_x, src_scale_y, src_scale_z)

    if delete_source:
        cmds.delete(src_transform)