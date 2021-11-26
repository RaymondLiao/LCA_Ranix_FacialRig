#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# File Name: lv3chr_facialsys_demo.py
# Author: Sheng (Raymond) Liao
# Date: October 2021
#

"""
A module to procedurally rig LCA third level characters' head model (demo).
"""

import os
import sys
import json

import maya.cmds as cmds
import maya.mel as mel

from general import util; reload(util)

from general import config; reload(config)
from general.config import *

from general import hierarchy; reload(hierarchy)

from control import control_proj_surface; reload(control_proj_surface)
from control.control_proj_surface import controlTransPlane, controlProjSurface

from control import control_curve; reload(control_curve)
from control.control_curve import controlCurve

from control import controller; reload(controller)
from control.controller import controller

# from control import control_zone; reload(control_zone)
# from control.control_zone import controlZone
from control import control_zone_eyelid; reload(control_zone_eyelid)
from control.control_zone_eyelid import eyelidControlZone

# global variables -----------------------------------------------------------------------------------------------------
g_crv_projsrf_dict = {
    'eyelid_transplane_RU' : None,
    'eyelid_transplane_RD' : None,
    'eyelid_transplane_LU' : None,
    'eyelid_transplane_LD' : None,
    'eyelid_projsrf_RU'    : None,
    'eyelid_projsrf_RD'    : None,
    'eyelid_projsrf_LU'    : None,
    'eyelid_projsrf_LD'    : None,
}

# g_lv3chr_facialsys_demo_run = False

# function definitions -------------------------------------------------------------------------------------------------

def lc3chr_facialsys_construct():

    # global g_lv3chr_facialsys_demo_run
    # if g_lv3chr_facialsys_demo_run:
    #     return
    # g_lv3chr_facialsys_demo_run = True

    # We must establish the group hierarchy first,
    # in order to organize the rig elements that will be created later in the Outliner.
    setup_group_hierarchy()
    assert cmds.objExists(hierarchy.eyelid_grp.get_group_name())

    setup_proj_surfaces()
    setup_ctrl_zones()

    # Do clean-up.
    cmds.select(deselect=True)
    mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes")')

def setup_proj_surfaces():
    """ Create the projection planes containing locator_data and joints.
    :return: None
    """

    global g_crv_projsrf_dict

    proj_srf_shader = cmds.shadingNode('lambert', asShader=True, name=PROJ_SRF_SHADER)
    cmds.setAttr(proj_srf_shader+'.color', 0.0, 0.0, 0.0, type='double3')
    cmds.setAttr(proj_srf_shader+'.transparency', 0.85, 0.85, 0.85, type='double3')
    proj_srf_shader_SG = cmds.sets(name=proj_srf_shader+'_SG',
                                   renderable=True, empty=True,)
    cmds.connectAttr(proj_srf_shader+'.outColor', proj_srf_shader_SG+'.surfaceShader', force=True)

    # Load the curve projection planes' data from the JSON document.
    root_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../'))

    f_control_proj_surface_data = None
    control_proj_surface_data = {}
    try:
        # print('lv3 character facial module root path: {}'.format(root_path))
        f_control_proj_surface_data = open(root_path+'/data/control_proj_surface_data.json', 'r')
        control_proj_surface_data = json.load(f_control_proj_surface_data)
    except:
        f_control_proj_surface_data.close()
        cmds.error('Error thrown while loading the data curve projection planes data: {}'.format(
            sys.exc_info()[0]
        ))

    # Create the controller Translation Planes and Projection Surfaces.
    # ------------------------------------------------------------------------------------------------------------------
    # Eyelid Facial Zone - Translation Planes
    eyelid_crvproj_transplane_data = control_proj_surface_data['eyelid_translation_plane']
    eyelid_crvproj_transplane_degree = eyelid_crvproj_transplane_data['degree']
    eyelid_crvproj_transplane_patchesU = eyelid_crvproj_transplane_data['patchesU']
    eyelid_crvproj_transplane_patchesV = eyelid_crvproj_transplane_data['patchesV']

    for dir_dict in CONTROL_ZONE_DIRECTION_DICT[controlZoneEnum.eyelid]:
        zone_dir = util.get_ctrl_zone_dir(dir_dict)
        eyelid_dir_transplane_data = eyelid_crvproj_transplane_data[zone_dir]

        mirror = [1, 1, 1]
        if controlZoneDirEnum.right in zone_dir:
            mirror = [-1, 1, 1]

        eyelid_crvproj_transplane = controlTransPlane(name_prefix = eyelid_crvproj_transplane_data['name_prefix'],
                                                      name = eyelid_dir_transplane_data['name'],
                                                      degree = eyelid_crvproj_transplane_degree,
                                                      patchesU = eyelid_crvproj_transplane_patchesU,
                                                      patchesV = eyelid_crvproj_transplane_patchesV,
                                                      translation = eyelid_dir_transplane_data['xform']['translation'],
                                                      rotation = eyelid_dir_transplane_data['xform']['rotation'],
                                                      scale = eyelid_dir_transplane_data['xform']['scale'],
                                                      mirror = mirror)
        if controlZoneDirEnum.right in zone_dir and controlZoneDirEnum.up in zone_dir:
            g_crv_projsrf_dict['eyelid_transplane_RU'] = eyelid_crvproj_transplane
            cmds.parent(eyelid_crvproj_transplane.get_name(),
                        hierarchy.eyelid_ctrlzone_RU_grp.get_group_name())
        elif controlZoneDirEnum.right in zone_dir and controlZoneDirEnum.down in zone_dir:
            g_crv_projsrf_dict['eyelid_transplane_RD'] = eyelid_crvproj_transplane
            cmds.parent(eyelid_crvproj_transplane.get_name(),
                        hierarchy.eyelid_ctrlzone_RD_grp.get_group_name())
        elif controlZoneDirEnum.left in zone_dir and controlZoneDirEnum.up in zone_dir:
            g_crv_projsrf_dict['eyelid_transplane_LU'] = eyelid_crvproj_transplane
            cmds.parent(eyelid_crvproj_transplane.get_name(),
                        hierarchy.eyelid_ctrlzone_LU_grp.get_group_name())
        elif controlZoneDirEnum.left in zone_dir and controlZoneDirEnum.down in zone_dir:
            g_crv_projsrf_dict['eyelid_transplane_LD'] = eyelid_crvproj_transplane
            cmds.parent(eyelid_crvproj_transplane.get_name(),
                        hierarchy.eyelid_ctrlzone_LD_grp.get_group_name())

    # Eyelid Facial Zone - Projection Surfaces
    eyelid_crvproj_projsrf_data = control_proj_surface_data['eyelid_projection_surface']
    eyelid_crvproj_projsrf_degree = eyelid_crvproj_projsrf_data['degree']
    eyelid_crvproj_projsrf_patchesU = eyelid_crvproj_projsrf_data['patchesU']
    eyelid_crvproj_projsrf_patchesV = eyelid_crvproj_projsrf_data['patchesV']

    for dir_dict in CONTROL_ZONE_DIRECTION_DICT[controlZoneEnum.eyelid]:
        zone_dir = util.get_ctrl_zone_dir(dir_dict)
        eyelid_dir_projsrf_data = eyelid_crvproj_projsrf_data[zone_dir]

        mirror = [1, 1, 1]
        if controlZoneDirEnum.right in zone_dir:
            mirror = [-1, 1, 1]

        eyelid_crvproj_projsrf = controlProjSurface(name_prefix = eyelid_crvproj_projsrf_data['name_prefix'],
                                                    name = eyelid_dir_projsrf_data['name'],
                                                    degree = eyelid_crvproj_projsrf_degree,
                                                    patchesU = eyelid_crvproj_projsrf_patchesU,
                                                    patchesV = eyelid_crvproj_projsrf_patchesV,
                                                    translation = eyelid_dir_projsrf_data['xform']['translation'],
                                                    rotation = eyelid_dir_projsrf_data['xform']['rotation'],
                                                    scale = eyelid_dir_projsrf_data['xform']['scale'],
                                                    mirror = mirror,
                                                    cv_list = eyelid_dir_projsrf_data['control_vtx'],
                                                    locator_data = eyelid_dir_projsrf_data['locators'],
                                                    locator_scale = eyelid_crvproj_projsrf_data['locator_scale'],
                                                    bind_joint_data = eyelid_crvproj_projsrf_data['bind_joint'],
                                                    bind_joint_color=BIND_JOINT_COLOR_INDEX)

        loc_row_id_list = eyelid_crvproj_projsrf.get_locator_row_ids()

        if controlZoneDirEnum.right in zone_dir and controlZoneDirEnum.up in zone_dir:
            g_crv_projsrf_dict['eyelid_projsrf_RU'] = eyelid_crvproj_projsrf
            cmds.parent(eyelid_crvproj_projsrf.get_name(),
                        hierarchy.eyelid_projsrf_RU_grp.get_group_name())

            for loc_row_id in loc_row_id_list:
                if 'A' == loc_row_id:
                    for loc_col_id in eyelid_crvproj_projsrf.get_locator_col_ids(loc_row_id):
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_RU_A_grp.get_group_name())
                elif 'B' == loc_row_id:
                    for loc_col_id in eyelid_crvproj_projsrf.get_locator_col_ids(loc_row_id):
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_RU_B_grp.get_group_name())
                elif 'C' == loc_row_id:
                    for loc_col_id in eyelid_crvproj_projsrf.get_locator_col_ids(loc_row_id):
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_RU_C_grp.get_group_name())
                elif 'D' == loc_row_id:
                    for loc_col_id in eyelid_crvproj_projsrf.get_locator_col_ids(loc_row_id):
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_RU_D_grp.get_group_name())

        elif controlZoneDirEnum.right in zone_dir and controlZoneDirEnum.down in zone_dir:
            g_crv_projsrf_dict['eyelid_projsrf_RD'] = eyelid_crvproj_projsrf
            cmds.parent(eyelid_crvproj_projsrf.get_name(),
                        hierarchy.eyelid_projsrf_RD_grp.get_group_name())

            for loc_row_id in loc_row_id_list:
                if 'A' == loc_row_id:
                    for loc_col_id in eyelid_crvproj_projsrf.get_locator_col_ids(loc_row_id):
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_RD_A_grp.get_group_name())
                elif 'B' == loc_row_id:
                    for loc_col_id in eyelid_crvproj_projsrf.get_locator_col_ids(loc_row_id):
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_RD_B_grp.get_group_name())
                elif 'C' == loc_row_id:
                    for loc_col_id in eyelid_crvproj_projsrf.get_locator_col_ids(loc_row_id):
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_RD_C_grp.get_group_name())
                elif 'D' == loc_row_id:
                    for loc_col_id in eyelid_crvproj_projsrf.get_locator_col_ids(loc_row_id):
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_RD_D_grp.get_group_name())

        elif controlZoneDirEnum.left in zone_dir and controlZoneDirEnum.up in zone_dir:
            g_crv_projsrf_dict['eyelid_projsrf_LU'] = eyelid_crvproj_projsrf
            cmds.parent(eyelid_crvproj_projsrf.get_name(),
                        hierarchy.eyelid_projsrf_LU_grp.get_group_name())

            for loc_row_id in loc_row_id_list:
                if 'A' == loc_row_id:
                    for loc_col_id in eyelid_crvproj_projsrf.get_locator_col_ids(loc_row_id):
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_LU_A_grp.get_group_name())
                elif 'B' == loc_row_id:
                    for loc_col_id in eyelid_crvproj_projsrf.get_locator_col_ids(loc_row_id):
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_LU_B_grp.get_group_name())
                elif 'C' == loc_row_id:
                    for loc_col_id in eyelid_crvproj_projsrf.get_locator_col_ids(loc_row_id):
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_LU_C_grp.get_group_name())
                elif 'D' == loc_row_id:
                    for loc_col_id in eyelid_crvproj_projsrf.get_locator_col_ids(loc_row_id):
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_LU_D_grp.get_group_name())

        elif controlZoneDirEnum.left in zone_dir and controlZoneDirEnum.down in zone_dir:
            g_crv_projsrf_dict['eyelid_projsrf_LD'] = eyelid_crvproj_projsrf
            cmds.parent(eyelid_crvproj_projsrf.get_name(),
                        hierarchy.eyelid_projsrf_LD_grp.get_group_name())

            for loc_row_id in loc_row_id_list:
                if 'A' == loc_row_id:
                    for loc_col_id in eyelid_crvproj_projsrf.get_locator_col_ids(loc_row_id):
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_LD_A_grp.get_group_name())
                elif 'B' == loc_row_id:
                    for loc_col_id in eyelid_crvproj_projsrf.get_locator_col_ids(loc_row_id):
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_LD_B_grp.get_group_name())
                elif 'C' == loc_row_id:
                    for loc_col_id in eyelid_crvproj_projsrf.get_locator_col_ids(loc_row_id):
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_LD_C_grp.get_group_name())
                elif 'D' == loc_row_id:
                    for loc_col_id in eyelid_crvproj_projsrf.get_locator_col_ids(loc_row_id):
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_LD_D_grp.get_group_name())

    # ------------------------------------------------------------------------------------------------------------------
    # Eyebrow Facial Zone - Translation Planes
    eyebrow_crvproj_transplane_data = control_proj_surface_data['eyebrow_translation_plane']
    eyebrow_crvproj_transplane_degree = eyebrow_crvproj_transplane_data['degree']
    eyebrow_crvproj_transplane_patchesU = eyebrow_crvproj_transplane_data['patchesU']
    eyebrow_crvproj_transplane_patchesV = eyebrow_crvproj_transplane_data['patchesV']



    # Eyebrow Facial Zone - Projection Surfaces

    f_control_proj_surface_data.close()

def setup_ctrl_zones():
    """ Create the facial controlling NURBS curves.
    :return: None
    """

    # Load the control curves' and controllers' data from the JSON document.
    root_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../'))

    f_ctrl_crv_data = None
    ctrl_crv_data = {}
    try:
        f_ctrl_crv_data = open(root_path+'/data/control_crv_data.json', 'r')
        ctrl_crv_data = json.load(f_ctrl_crv_data)
    except:
        f_ctrl_crv_data.close()
        cmds.error('Error thrown while loading the control curves data: {}'.format(
            sys.exc_info()[0]
        ))

    # Create the control zones.
    for dir_dict in CONTROL_ZONE_DIRECTION_DICT[controlZoneEnum.eyelid]:
        zone_dir = util.get_ctrl_zone_dir(dir_dict)

        ctrlproj_transplane = None
        if controlZoneDirEnum.right in zone_dir:
            if controlZoneDirEnum.up in zone_dir:
                ctrlproj_transplane = g_crv_projsrf_dict['eyelid_transplane_RU']
            elif controlZoneDirEnum.down in zone_dir:
                ctrlproj_transplane = g_crv_projsrf_dict['eyelid_transplane_RD']
        elif controlZoneDirEnum.left in zone_dir:
            if controlZoneDirEnum.up in zone_dir:
                ctrlproj_transplane = g_crv_projsrf_dict['eyelid_transplane_LU']
            elif controlZoneDirEnum.down in zone_dir:
                ctrlproj_transplane = g_crv_projsrf_dict['eyelid_transplane_LD']
        assert None != ctrlproj_transplane

        ctrlproj_projsrf = None
        if controlZoneDirEnum.right in zone_dir:
            if controlZoneDirEnum.up in zone_dir:
                ctrlproj_projsrf = g_crv_projsrf_dict['eyelid_projsrf_RU']
            elif controlZoneDirEnum.down in zone_dir:
                ctrlproj_projsrf = g_crv_projsrf_dict['eyelid_projsrf_RD']
        elif controlZoneDirEnum.left in zone_dir:
            if controlZoneDirEnum.up in zone_dir:
                ctrlproj_projsrf = g_crv_projsrf_dict['eyelid_projsrf_LU']
            elif controlZoneDirEnum.down in zone_dir:
                ctrlproj_projsrf = g_crv_projsrf_dict['eyelid_projsrf_LD']
        assert None != ctrlproj_projsrf

        eyelid_ctrl_zone = eyelidControlZone(direction=zone_dir,
                                             ctrl_crv_data=ctrl_crv_data,
                                             ctrlproj_transplane=ctrlproj_transplane,
                                             ctrlproj_projsurface=ctrlproj_projsrf)

    f_ctrl_crv_data.close()

def setup_group_hierarchy():
    """
    :return: None
    """

    eyelid_grp = hierarchy.eyelid_grp
    eyelid_grp.setup_group_hierarchy()

    eyebrow_grp = hierarchy.eyebrow_grp
    eyebrow_grp.setup_group_hierarchy()

# Entry point ==========================================================================================================
# lc3chr_facialsys_construct()