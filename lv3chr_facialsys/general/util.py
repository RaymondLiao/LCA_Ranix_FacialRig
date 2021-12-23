#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# File Name: util.py
# Author: Sheng (Raymond) Liao
# Date: November 2021
#

"""
A module containing utility functions used by the LCA third level character facial system
"""

import maya.cmds as cmds

def get_class_name(obj_or_class):
    """
    :param obj_or_class: a class or a class's instance
    :return: a string of the class's name
    """

    cls = type(obj_or_class)
    if cls is type:
        cls = obj_or_class

    return cls.__name__.split('.')[-1]

def get_enum_value_list(enum_class):
    """ Because Python does not support enum types until version 3.4, we have to define enum classes
    with enumerated attributes by ourselves; and we use this function to retrieve the enumerated values as a list.

    :param enum_class: custom "enumeration" class who keeps enumerated values as class attributes
    :return: a list of values of the custom enumeration classes' attributes
    """

    # Make sure the incoming argument is a name of the "enumeration" classes we defined in this module.
    enum_class_name = get_class_name(enum_class)
    assert 'controlZoneEnum' == enum_class_name or \
            'controlZoneDirEnum' == enum_class_name or \
            'dirDictKeyEnum' == enum_class_name

    res_list = [attr
                for attr in dir(enum_class)
                if not callable(getattr(enum_class, attr))
                and not attr.startswith('__')]

    return res_list

def get_ctrl_zone_dir(zone_dir_dict):
    """ Retrieve the control zone direction components' values stored in the zone sub-dictionary of the
    "CONTROL_ZONE_DIRECTION_DICT" dictionary, then use "_" separators to concatenate them into this zone's direction.

    Note that this function convert the direction combination of "left_right" into "middle".

    :param dir_dict: a sub-dictionary of the "CONTROL_ZONE_DIRECTION_DICT" keyed by
    the name of the facial zone, e.g. {"LD":"left_right", "UD":"up_dn", "FB":""}
    :return: a tuple of strings of the facial control zone direction and its abbreviation, e.g. ("middle_up_dn", "LRUD")
    """

    dir_whole = ''
    dir_abbr = ''

    for dir_key in ['LR', 'UD', 'FB']:
        dir_whole += ('_' + zone_dir_dict[dir_key])

    # Remove the leading and trailing '_'s, and those extra adjacent ones.
    dir_whole = dir_whole.strip('_').replace('__', '_')

    if 'l' in dir_whole:
        dir_abbr += 'L'
    if 'r' in dir_whole:
        dir_abbr += 'R'
    if 'u' in dir_whole:
        dir_abbr += 'U'
    if 'd' in dir_whole:
        dir_abbr += 'D'
    if 'fr' in dir_whole:
        dir_abbr += 'F'
    if 'b' in dir_whole:
        dir_abbr += 'B'

    # Replace the "left_right" or "right_left" with "middle".
    dir_whole = dir_whole.replace('left_right', 'middle').replace('right_left', 'middle')

    return (dir_whole, dir_abbr)

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

def ctrl_add_offset(ctrl_grp=None):
    if None == ctrl_grp:
        sel_list = cmds.ls(sl=True)
        if len(sel_list) > 0:
            ctrl_grp = sel_list[0]

    ctrl_list = cmds.listRelatives(ctrl_grp, children=True)
    for ctrl in ctrl_list:
        ctrl_pos = cmds.getAttr(ctrl + '.translate')[0]
        ctrl_ofs = cmds.group(ctrl, name=ctrl.replace('ctrl', 'ofs'))
        cmds.xform(ctrl_ofs, translation=list(ctrl_pos))
        cmds.xform(ctrl, translation=[0, 0, 0])