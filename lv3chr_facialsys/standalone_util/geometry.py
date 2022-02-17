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

g_float_precision = 8

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
            cv_coord_x = round(float(cv_coord[0]), g_float_precision)
            cv_coord_y = round(float(cv_coord[1]), g_float_precision)
            cv_coord_z = round(float(cv_coord[2]), g_float_precision)
            nurbs_srf_CVs += '{{"{0},{1}": [{2:.8f}, {3}, {4}]}},\n'.format(idx_u, idx_v,
                                                                          cv_coord_x, cv_coord_y, cv_coord_z)
        nurbs_srf_CVs += '\n'

    nurbs_srf_CVs = nurbs_srf_CVs[:-3]  # Get rid of the trailing two '\n' and a ','
    cmds.warning(nurbs_srf_CVs)

    return nurbs_srf_CVs

def get_nurbs_crv_CVs():
    nurbs_crv = cmds.ls(selection=True)[0]
    nurbs_crv_span = cmds.getAttr(nurbs_crv+'.spans')

    nurbs_crv_CVs = ''

    for idx in range(nurbs_crv_span+1):
        cv_coord = cmds.getAttr(nurbs_crv+'.cv[{}]'.format(idx))[0]
        cv_coord_x = round(float(cv_coord[0]), g_float_precision)
        cv_coord_y = round(float(cv_coord[1]), g_float_precision)
        cv_coord_z = round(float(cv_coord[2]), g_float_precision)
        nurbs_crv_CVs += '[{0}, {1}, {2}],\n'.format(cv_coord_x, cv_coord_y, cv_coord_z)

    cmds.warning(nurbs_crv_CVs)
    return nurbs_crv_CVs

def get_transform_string():
    sel_transform = cmds.ls(sl=True)[0]

    sel_translation = cmds.getAttr(sel_transform+'.translate')[0]
    sel_translation_x = round(float(sel_translation[0]), g_float_precision)
    sel_translation_y = round(float(sel_translation[1]), g_float_precision)
    sel_translation_z = round(float(sel_translation[2]), g_float_precision)

    sel_translation_str = '"translation": [{0}, {1}, {2}],\n'.format(
        sel_translation_x, sel_translation_y, sel_translation_z
    )

    sel_rotation = cmds.getAttr(sel_transform+'.rotate')[0]
    sel_rotation_x = round(float(sel_rotation[0]), g_float_precision)
    sel_rotation_y = round(float(sel_rotation[1]), g_float_precision)
    sel_rotation_z = round(float(sel_rotation[2]), g_float_precision)

    sel_rotation_str = '"rotation": [{0}, {1}, {2}],\n'.format(
        sel_rotation_x,sel_rotation_y, sel_rotation_z
    )

    sel_scale = cmds.getAttr(sel_transform+'.scale')[0]
    sel_scale_x = round(float(sel_scale[0]), g_float_precision)
    sel_scale_y = round(float(sel_scale[1]), g_float_precision)
    sel_scale_z = round(float(sel_scale[2]), g_float_precision)

    sel_scale_str = '"scale": [{0}, {1}, {2}]\n'.format(
        sel_scale_x, sel_scale_y, sel_scale_z
    )

    sel_transform_str = sel_translation_str + sel_rotation_str + sel_scale_str
    cmds.warning(sel_transform_str)

    return sel_transform_str

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


def copy_curve_CVs(transform_offset=(0.0, 0.0, 0.0), axis_x=True, axis_y=True, axis_z=True):
    sel_transform_list = cmds.ls(sl=True)
    sel_curve_shape_list = []
    for sel_transform in sel_transform_list:
        sel_curve_shape = cmds.listRelatives(sel_transform, shapes=True)[0]
        if 'nurbsCurve' != cmds.objectType(sel_curve_shape):
            cmds.error('Must select NURBS curves to copy control vertices coordinates.')
            return
        sel_curve_shape_list.append(sel_curve_shape)

    src_curve_shape = sel_curve_shape_list[0]
    src_cv_count = cmds.getAttr(src_curve_shape+'.spans') + 1

    tar_curve_shape_list = sel_curve_shape_list[1:]
    for tar_curve_shape in tar_curve_shape_list:
        tar_cv_count = cmds.getAttr(tar_curve_shape+'.spans') + 1
        if tar_cv_count != src_cv_count:
            cmds.error('The target NURBS curves must have the same number of CVs with the source NURBS curve')
            return

        for cv_id in range(src_cv_count):
            src_cv = [sum(item) for item in zip(cmds.getAttr(src_curve_shape+'.cv[{}]'.format(cv_id))[0], transform_offset)]
            #cmds.warning('source_cv[{}]: {}'.format(cv_id, src_cv))
            #cmds.warning('target_cv[{}]: {}'.format(cv_id, cmds.getAttr(tar_curve_shape+'.cv[{}]'.format(cv_id))))
            tar_cv = list(cmds.getAttr(tar_curve_shape+'.cv[{}]'.format(cv_id))[0])
            if axis_x:
                tar_cv[0] = src_cv[0]
            if axis_y:
                tar_cv[1] = src_cv[1]
            if axis_z:
                tar_cv[2] = src_cv[2]

            cmds.setAttr(tar_curve_shape+'.cv[{}]'.format(cv_id), tar_cv[0], tar_cv[1], tar_cv[2])

def flatten_NURBS_surface(axis='y', make_plane=False):
    srf_transform = cmds.ls(sl=True)[0]
    srf_shape = cmds.listRelatives(srf_transform, shapes=True)[0]
    srf_span_U = cmds.getAttr(srf_shape+'.spansU')
    srf_span_V = cmds.getAttr(srf_shape+'.spansV')
    base_coord = cmds.getAttr(srf_shape + '.cv[0][0]')
    for cv_U_id in range(0, srf_span_U+1):
        row_base_coord = list(cmds.getAttr(srf_shape+'.cv[{}][0]'.format(cv_U_id))[0])
        for cv_V_id in range(1, srf_span_V+1):
            ori_coord = list(cmds.getAttr(srf_shape + '.cv[{}][{}]'.format(cv_U_id, cv_V_id))[0])

            if make_plane:
                if 'x' == axis:
                    cmds.setAttr(srf_shape + '.cv[{}][{}]'.format(
                        cv_U_id, cv_V_id), base_coord[0], ori_coord[1], ori_coord[2])
                elif 'y' == axis:
                    cmds.setAttr(srf_shape + '.cv[{}][{}]'.format(
                        cv_U_id, cv_V_id), ori_coord[0], base_coord[0], ori_coord[2])
                elif 'z' == axis:
                    cmds.setAttr(srf_shape + '.cv[{}][{}]'.format(
                        cv_U_id, cv_V_id), ori_coord[0], ori_coord[1], base_coord[0])
            else:
                flat_coord = ori_coord
                if 'x' == axis:
                    flat_coord[0] = row_base_coord[0]
                elif 'y' == axis:
                    flat_coord[1] = row_base_coord[1]
                elif 'z' == axis:
                    flat_coord[2] = row_base_coord[2]

                cmds.setAttr(srf_shape+'.cv[{}][{}]'.format(
                    cv_U_id, cv_V_id), flat_coord[0], flat_coord[1], flat_coord[2])