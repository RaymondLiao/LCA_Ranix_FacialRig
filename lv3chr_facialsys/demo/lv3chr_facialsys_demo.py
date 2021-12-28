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
from control.zone import eyelid; reload(eyelid)
from control.zone.eyelid import eyelidControlZone
from control.zone import eyebrow; reload(eyebrow)
from control.zone.eyebrow import eyebrowControlZone
from control.zone import mouth; reload(mouth)
from control.zone.mouth import mouthControlZone

# global variables -----------------------------------------------------------------------------------------------------
g_displayer_transplane = 'translation_plane'
g_displayer_projsrf = 'projection_surface'
g_displayer_ctrlcrv = 'control_curve'

g_crv_projsrf_dict = {
    'eyelid_transplane_RU' : None,
    'eyelid_transplane_RD' : None,
    'eyelid_transplane_LU' : None,
    'eyelid_transplane_LD' : None,
    'eyelid_projsrf_RU'    : None,
    'eyelid_projsrf_RD'    : None,
    'eyelid_projsrf_LU'    : None,
    'eyelid_projsrf_LD'    : None,

    'eyebrow_transplane_LRUD' : None,
    'eyebrow_transplane_LRF'  : None,
    'eyebrow_projsrf_LRUD'    : None,
    'eyebrow_projsrf_LRF'     : None,

    'mouth_transplane_LRU': None,
    'mouth_transplane_LRD': None,
    'mouth_projsrf_LRU': None,
    'mouth_projsrf_LRD': None,

    'nasolabial_transplane_RUD' : None,
    'nasolabial_transplane_LUD' : None,
    'nasolabial_projsrf_RUD' : None,
    'nasolabial_projsrf_LUD' : None
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

    # Create Display Layers for the translation planes, the projection surfaces and the control curves, if there are not.
    display_layer_list = cmds.ls(type='displayLayer')
    if g_displayer_transplane not in display_layer_list:
        cmds.createDisplayLayer(name=g_displayer_transplane, empty=True, noRecurse=True)
    if g_displayer_projsrf not in display_layer_list:
        cmds.createDisplayLayer(name=g_displayer_projsrf, empty=True, noRecurse=True)
    if g_displayer_ctrlcrv not in display_layer_list:
        cmds.createDisplayLayer(name=g_displayer_ctrlcrv, empty=True, noRecurse=True)

    cmds.editDisplayLayerMembers(g_displayer_transplane,
                                 g_crv_projsrf_dict['eyelid_transplane_RU'].get_name(),
                                 g_crv_projsrf_dict['eyelid_transplane_RD'].get_name(),
                                 g_crv_projsrf_dict['eyelid_transplane_LU'].get_name(),
                                 g_crv_projsrf_dict['eyelid_transplane_LD'].get_name(),
                                 g_crv_projsrf_dict['eyebrow_transplane_LRUD'].get_name(),
                                 g_crv_projsrf_dict['eyebrow_transplane_LRF'].get_name(),
                                 g_crv_projsrf_dict['mouth_transplane_LRU'].get_name(),
                                 g_crv_projsrf_dict['mouth_transplane_LRD'].get_name())
    cmds.editDisplayLayerMembers(g_displayer_projsrf,
                                 g_crv_projsrf_dict['eyelid_projsrf_RU'].get_name(),
                                 g_crv_projsrf_dict['eyelid_projsrf_RD'].get_name(),
                                 g_crv_projsrf_dict['eyelid_projsrf_LU'].get_name(),
                                 g_crv_projsrf_dict['eyelid_projsrf_LD'].get_name(),
                                 g_crv_projsrf_dict['eyebrow_projsrf_LRUD'].get_name(),
                                 g_crv_projsrf_dict['eyebrow_projsrf_LRF'].get_name(),
                                 g_crv_projsrf_dict['mouth_projsrf_LRU'].get_name(),
                                 g_crv_projsrf_dict['mouth_projsrf_LRD'].get_name())

    # Toggle on the "Wireframe on Shaded" for the current model panel.
    visible_panel_list = cmds.getPanel(visiblePanels=True)
    active_viewport_list = [visible_panel for visible_panel in visible_panel_list if 'modelPanel' in visible_panel]
    cmds.modelEditor(active_viewport_list[0], edit=True, wireframeOnShaded=True)
    cmds.warning('Turned on the "Wireframe on Shaded" shading mode in the "{}" viewport.'.format(active_viewport_list[0]))

    # Toggle on the "Viewport 2.0" renderer
    mel.eval('setRendererInModelPanel ogsRenderer {}'.format(active_viewport_list[0]))
    cmds.warning('Turned on the "Viewport 2.0" renderer in the "{}" viewport.'.format(active_viewport_list[0]))

    # Do clean-up.
    cmds.select(deselect=True)
    mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes")')

def setup_proj_surfaces():
    """ Create the projection planes containing locator_data and joints.
    :return: None
    """

    global g_crv_projsrf_dict

    proj_srf_shader = cmds.shadingNode('lambert', asShader=True, name=PROJ_SRF_SHADER)
    cmds.setAttr(proj_srf_shader+'.color', 1.0, 1.0, 0.5, type='double3')
    # cmds.setAttr(proj_srf_shader+'.transparency', 0.85, 0.85, 0.85, type='double3')
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

    for dir_dict in CONTROL_ZONE_DIRECTION_DICT[controlZoneEnum.eyelid]:
        zone_dir = util.get_ctrl_zone_dir(dir_dict)[0]
        eyelid_dir_transplane_data = eyelid_crvproj_transplane_data[zone_dir]
        eyelid_dir_transplane_degree = eyelid_dir_transplane_data['degree']
        eyelid_dir_transplane_patchesU = eyelid_dir_transplane_data['patchesU']
        eyelid_dir_transplane_patchesV = eyelid_dir_transplane_data['patchesV']

        mirror = [1, 1, 1]
        if controlZoneDirEnum.right in zone_dir:
            mirror = [-1, 1, 1]

        eyelid_crvproj_transplane = controlTransPlane(name_prefix = eyelid_crvproj_transplane_data['name_prefix'],
                                                      name = eyelid_dir_transplane_data['name'],
                                                      degree = eyelid_dir_transplane_degree,
                                                      patchesU = eyelid_dir_transplane_patchesU,
                                                      patchesV = eyelid_dir_transplane_patchesV,
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

    for dir_dict in CONTROL_ZONE_DIRECTION_DICT[controlZoneEnum.eyelid]:
        zone_dir = util.get_ctrl_zone_dir(dir_dict)[0]
        eyelid_dir_projsrf_data = eyelid_crvproj_projsrf_data[zone_dir]
        eyelid_dir_projsrf_degree = eyelid_dir_projsrf_data['degree']
        eyelid_dir_projsrf_patchesU = eyelid_dir_projsrf_data['patchesU']
        eyelid_dir_projsrf_patchesV = eyelid_dir_projsrf_data['patchesV']

        mirror = [1, 1, 1]
        if controlZoneDirEnum.right in zone_dir:
            mirror = [-1, 1, 1]

        eyelid_crvproj_projsrf = controlProjSurface(name_prefix = eyelid_crvproj_projsrf_data['name_prefix'],
                                                    name = eyelid_dir_projsrf_data['name'],
                                                    degree = eyelid_dir_projsrf_degree,
                                                    patchesU = eyelid_dir_projsrf_patchesU,
                                                    patchesV = eyelid_dir_projsrf_patchesV,
                                                    translation = eyelid_dir_projsrf_data['xform']['translation'],
                                                    rotation = eyelid_dir_projsrf_data['xform']['rotation'],
                                                    scale = eyelid_dir_projsrf_data['xform']['scale'],
                                                    mirror = mirror,
                                                    cv_list = eyelid_dir_projsrf_data['control_vtx'],
                                                    locator_data = eyelid_dir_projsrf_data['locators'],
                                                    locator_scale = eyelid_crvproj_projsrf_data['locator_scale'],
                                                    bind_joint_data = eyelid_crvproj_projsrf_data['bind_joint'],
                                                    bind_joint_color = BIND_JOINT_COLOR_INDEX)

        loc_row_id_list = eyelid_crvproj_projsrf.get_locator_row_ids()

        if controlZoneDirEnum.right in zone_dir and controlZoneDirEnum.up in zone_dir:
            g_crv_projsrf_dict['eyelid_projsrf_RU'] = eyelid_crvproj_projsrf
            cmds.parent(eyelid_crvproj_projsrf.get_name(),
                        hierarchy.eyelid_projsrf_RU_grp.get_group_name())

            for loc_row_id in loc_row_id_list:
                for loc_col_id in eyelid_crvproj_projsrf.get_locator_col_ids(loc_row_id):
                    if 'A' == loc_row_id:
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_RU_A_grp.get_group_name())
                    elif 'B' == loc_row_id:
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_RU_B_grp.get_group_name())
                    elif 'C' == loc_row_id:
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_RU_C_grp.get_group_name())
                    elif 'D' == loc_row_id:
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_RU_D_grp.get_group_name())
                    elif 'E' == loc_row_id:
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_RU_E_grp.get_group_name())
                    elif 'F' == loc_row_id:
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_RU_F_grp.get_group_name())

        elif controlZoneDirEnum.right in zone_dir and controlZoneDirEnum.down in zone_dir:
            g_crv_projsrf_dict['eyelid_projsrf_RD'] = eyelid_crvproj_projsrf
            cmds.parent(eyelid_crvproj_projsrf.get_name(),
                        hierarchy.eyelid_projsrf_RD_grp.get_group_name())

            for loc_row_id in loc_row_id_list:
                for loc_col_id in eyelid_crvproj_projsrf.get_locator_col_ids(loc_row_id):
                    if 'A' == loc_row_id:
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_RD_A_grp.get_group_name())
                    elif 'B' == loc_row_id:
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_RD_B_grp.get_group_name())
                    elif 'C' == loc_row_id:
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_RD_C_grp.get_group_name())
                    elif 'D' == loc_row_id:
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_RD_D_grp.get_group_name())
                    elif 'E' == loc_row_id:
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_RD_E_grp.get_group_name())
                    elif 'F' == loc_row_id:
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_RD_F_grp.get_group_name())

        elif controlZoneDirEnum.left in zone_dir and controlZoneDirEnum.up in zone_dir:
            g_crv_projsrf_dict['eyelid_projsrf_LU'] = eyelid_crvproj_projsrf
            cmds.parent(eyelid_crvproj_projsrf.get_name(),
                        hierarchy.eyelid_projsrf_LU_grp.get_group_name())

            for loc_row_id in loc_row_id_list:
                for loc_col_id in eyelid_crvproj_projsrf.get_locator_col_ids(loc_row_id):
                    if 'A' == loc_row_id:
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_LU_A_grp.get_group_name())
                    elif 'B' == loc_row_id:
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_LU_B_grp.get_group_name())
                    elif 'C' == loc_row_id:
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_LU_C_grp.get_group_name())
                    elif 'D' == loc_row_id:
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_LU_D_grp.get_group_name())
                    elif 'E' == loc_row_id:
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_LU_E_grp.get_group_name())
                    elif 'F' == loc_row_id:
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_LU_F_grp.get_group_name())

        elif controlZoneDirEnum.left in zone_dir and controlZoneDirEnum.down in zone_dir:
            g_crv_projsrf_dict['eyelid_projsrf_LD'] = eyelid_crvproj_projsrf
            cmds.parent(eyelid_crvproj_projsrf.get_name(),
                        hierarchy.eyelid_projsrf_LD_grp.get_group_name())

            for loc_row_id in loc_row_id_list:
                for loc_col_id in eyelid_crvproj_projsrf.get_locator_col_ids(loc_row_id):
                    if 'A' == loc_row_id:
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_LD_A_grp.get_group_name())
                    elif 'B' == loc_row_id:
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_LD_B_grp.get_group_name())
                    elif 'C' == loc_row_id:
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_LD_C_grp.get_group_name())
                    elif 'D' == loc_row_id:
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_LD_D_grp.get_group_name())
                    elif 'E' == loc_row_id:
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_LD_E_grp.get_group_name())
                    elif 'F' == loc_row_id:
                        cmds.parent(eyelid_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyelid_projsrf_loc_LD_F_grp.get_group_name())

    # ------------------------------------------------------------------------------------------------------------------
    # Eyebrow Facial Zone - Translation Planes
    eyebrow_crvproj_transplane_data = control_proj_surface_data['eyebrow_translation_plane']

    for dir_dict in CONTROL_ZONE_DIRECTION_DICT[controlZoneEnum.eyebrow]:
        zone_dir = util.get_ctrl_zone_dir(dir_dict)[0]
        eyebrow_dir_transplane_data = eyebrow_crvproj_transplane_data[zone_dir]
        eyebrow_dir_transplane_degree = eyebrow_dir_transplane_data['degree']
        eyebrow_dir_transplane_patchesU = eyebrow_dir_transplane_data['patchesU']
        eyebrow_dir_transplane_patchesV = eyebrow_dir_transplane_data['patchesV']

        eyebrow_crvproj_transplane = controlTransPlane(name_prefix = eyebrow_crvproj_transplane_data['name_prefix'],
                                                       name = eyebrow_dir_transplane_data['name'],
                                                       degree = eyebrow_dir_transplane_degree,
                                                       patchesU = eyebrow_dir_transplane_patchesU,
                                                       patchesV = eyebrow_dir_transplane_patchesV,
                                                       translation = eyebrow_dir_transplane_data['xform']['translation'],
                                                       rotation = eyebrow_dir_transplane_data['xform']['rotation'],
                                                       scale = eyebrow_dir_transplane_data['xform']['scale'],
                                                       cv_list = eyebrow_dir_transplane_data['control_vtx'])

        if controlZoneDirEnum.up in zone_dir and controlZoneDirEnum.down in zone_dir:
            g_crv_projsrf_dict['eyebrow_transplane_LRUD'] = eyebrow_crvproj_transplane
        elif controlZoneDirEnum.front in zone_dir:
            g_crv_projsrf_dict['eyebrow_transplane_LRF'] = eyebrow_crvproj_transplane

        cmds.parent(eyebrow_crvproj_transplane.get_name(),
                    hierarchy.eyebrow_ctrlzone_M_grp.get_group_name())

    # Eyebrow Facial Zone - Projection Surfaces
    eyebrow_crvproj_projsrf_data = control_proj_surface_data['eyebrow_projection_surface']

    for dir_dict in CONTROL_ZONE_DIRECTION_DICT[controlZoneEnum.eyebrow]:
        zone_dir = util.get_ctrl_zone_dir(dir_dict)[0]
        eyebrow_dir_projsrf_data = eyebrow_crvproj_projsrf_data[zone_dir]
        eyebrow_dir_projsrf_degree = eyebrow_dir_projsrf_data['degree']
        eyebrow_dir_projsrf_patchesU = eyebrow_dir_projsrf_data['patchesU']
        eyebrow_dir_projsrf_pathcesV = eyebrow_dir_projsrf_data['patchesV']

        eyebrow_crvproj_projsrf = controlProjSurface(name_prefix = eyebrow_crvproj_projsrf_data['name_prefix'],
                                                     name = eyebrow_dir_projsrf_data['name'],
                                                     degree = eyebrow_dir_projsrf_degree,
                                                     patchesU = eyebrow_dir_projsrf_patchesU,
                                                     patchesV = eyebrow_dir_projsrf_pathcesV,
                                                     translation = eyebrow_dir_projsrf_data['xform']['translation'],
                                                     rotation = eyebrow_dir_projsrf_data['xform']['rotation'],
                                                     scale = eyebrow_dir_projsrf_data['xform']['scale'],
                                                     cv_list = eyebrow_dir_projsrf_data['control_vtx'],
                                                     locator_data = eyebrow_dir_projsrf_data['locators'],
                                                     locator_scale = eyebrow_crvproj_projsrf_data['locator_scale'],
                                                     bind_joint_data = eyebrow_crvproj_projsrf_data['bind_joint'],
                                                     bind_joint_color = BIND_JOINT_COLOR_INDEX)

        loc_row_id_list = eyebrow_crvproj_projsrf.get_locator_row_ids()

        if controlZoneDirEnum.up in zone_dir and controlZoneDirEnum.down in zone_dir:
            g_crv_projsrf_dict['eyebrow_projsrf_LRUD'] = eyebrow_crvproj_projsrf

            for loc_row_id in loc_row_id_list:
                for loc_col_id in eyebrow_crvproj_projsrf.get_locator_col_ids(loc_row_id):
                    if 'A' == loc_row_id:
                        cmds.parent(eyebrow_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyebrow_projsrf_loc_M_UD_A_grp.get_group_name())
                    elif 'B' == loc_row_id:
                        cmds.parent(eyebrow_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyebrow_projsrf_loc_M_UD_B_grp.get_group_name())
                    elif 'C' == loc_row_id:
                        cmds.parent(eyebrow_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyebrow_projsrf_loc_M_UD_C_grp.get_group_name())
                    elif 'D' == loc_row_id:
                        cmds.parent(eyebrow_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyebrow_projsrf_loc_M_UD_D_grp.get_group_name())

        elif controlZoneDirEnum.front in zone_dir:
            g_crv_projsrf_dict['eyebrow_projsrf_LRF'] = eyebrow_crvproj_projsrf

            for loc_row_id in loc_row_id_list:
                for loc_col_id in eyebrow_crvproj_projsrf.get_locator_col_ids(loc_row_id):
                    if 'A' == loc_row_id:
                        cmds.parent(eyebrow_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                    hierarchy.eyebrow_projsrf_loc_M_FB_grp.get_group_name())

        cmds.parent(eyebrow_crvproj_projsrf.get_name(),
                    hierarchy.eyebrow_projsrf_M_grp.get_group_name())

    # ------------------------------------------------------------------------------------------------------------------
    # Mouth Facial Zone - Translation Planes
    mouth_crvproj_transplane_data = control_proj_surface_data['mouth_translation_plane']

    for dir_dict in CONTROL_ZONE_DIRECTION_DICT[controlZoneEnum.mouth]:
        zone_dir = util.get_ctrl_zone_dir(dir_dict)[0]
        mouth_dir_transplane_data = mouth_crvproj_transplane_data[zone_dir]
        mouth_dir_transplane_degree = mouth_dir_transplane_data['degree']
        mouth_dir_transplane_patchesU = mouth_dir_transplane_data['patchesU']
        mouth_dir_transplane_patchesV = mouth_dir_transplane_data['patchesV']

        mouth_crvproj_transplane = controlTransPlane(name_prefix = mouth_crvproj_transplane_data['name_prefix'],
                                                     name = mouth_dir_transplane_data['name'],
                                                     degree = mouth_dir_transplane_degree,
                                                     patchesU = mouth_dir_transplane_patchesU,
                                                     patchesV = mouth_dir_transplane_patchesV,
                                                     translation = mouth_dir_transplane_data['xform']['translation'],
                                                     rotation = mouth_dir_transplane_data['xform']['rotation'],
                                                     scale = mouth_dir_transplane_data['xform']['scale'],
                                                     cv_list = mouth_dir_transplane_data['control_vtx'])

        if controlZoneDirEnum.up in zone_dir:
            g_crv_projsrf_dict['mouth_transplane_LRU'] = mouth_crvproj_transplane
            cmds.parent(mouth_crvproj_transplane.get_name(),
                        hierarchy.mouth_ctrlzone_MU_grp.get_group_name())
        elif controlZoneDirEnum.down in zone_dir:
            g_crv_projsrf_dict['mouth_transplane_LRD'] = mouth_crvproj_transplane
            cmds.parent(mouth_crvproj_transplane.get_name(),
                        hierarchy.mouth_ctrlzone_MD_grp.get_group_name())

    # Mouth Facial Zone - Projection Surfaces
    mouth_crvproj_projsrf_data = control_proj_surface_data['mouth_projection_surface']

    for dir_dict in CONTROL_ZONE_DIRECTION_DICT[controlZoneEnum.mouth]:
        zone_dir = util.get_ctrl_zone_dir(dir_dict)[0]
        mouth_dir_projsrf_data = mouth_crvproj_projsrf_data[zone_dir]
        mouth_dir_projsrf_degree = mouth_dir_projsrf_data['degree']
        mouth_dir_projsrf_patchesU = mouth_dir_projsrf_data['patchesU']
        mouth_dir_projsrf_pathcesV = mouth_dir_projsrf_data['patchesV']

        mouth_crvproj_projsrf = controlProjSurface(name_prefix = mouth_crvproj_projsrf_data['name_prefix'],
                                                   name = mouth_dir_projsrf_data['name'],
                                                   degree = mouth_dir_projsrf_degree,
                                                   patchesU = mouth_dir_projsrf_patchesU,
                                                   patchesV = mouth_dir_projsrf_pathcesV,
                                                   translation = mouth_dir_projsrf_data['xform']['translation'],
                                                   rotation = mouth_dir_projsrf_data['xform']['rotation'],
                                                   scale = mouth_dir_projsrf_data['xform']['scale'],
                                                   cv_list = mouth_dir_projsrf_data['control_vtx'],
                                                   locator_data = mouth_dir_projsrf_data['locators'],
                                                   locator_scale = mouth_crvproj_projsrf_data['locator_scale'],
                                                   bind_joint_data = mouth_crvproj_projsrf_data['bind_joint'],
                                                   bind_joint_color = BIND_JOINT_COLOR_INDEX)

        loc_row_id_list = mouth_crvproj_projsrf.get_locator_row_ids()

        if controlZoneDirEnum.up in zone_dir:
            g_crv_projsrf_dict['mouth_projsrf_LRU'] = mouth_crvproj_projsrf

            for loc_row_id in loc_row_id_list:
                for loc_col_id in mouth_crvproj_projsrf.get_locator_col_ids(loc_row_id):
                    cmds.parent(mouth_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                hierarchy.mouth_projsrf_loc_MU_A_grp.get_group_name())

        elif controlZoneDirEnum.down in zone_dir:
            g_crv_projsrf_dict['mouth_projsrf_LRD'] = mouth_crvproj_projsrf

            for loc_row_id in loc_row_id_list:
                for loc_col_id in mouth_crvproj_projsrf.get_locator_col_ids(loc_row_id):
                    cmds.parent(mouth_crvproj_projsrf.get_locator_info(loc_row_id, loc_col_id)[0],
                                hierarchy.mouth_projsrf_loc_MD_A_grp.get_group_name())

        cmds.parent(mouth_crvproj_projsrf.get_name(), hierarchy.mouth_projsrf_M_grp.get_group_name())

    # ------------------------------------------------------------------------------------------------------------------
    # Nasolabial Facial Zone - Translation Planes
    nasolabial_projcrv_transplane_data = control_proj_surface_data['nasolabial_translation_plane']

    for dir_dict in CONTROL_ZONE_DIRECTION_DICT[controlZoneEnum.nasolabial]:
        zone_dir = util.get_ctrl_zone_dir(dir_dict)[0]
        nasolabial_dir_transplane_data = nasolabial_projcrv_transplane_data[zone_dir]
        nasolabial_dir_transplane_degree = nasolabial_dir_transplane_data['degree']
        nasolabial_dir_transplane_patchesU = nasolabial_dir_transplane_data['patchesU']
        nasolabial_dir_transplane_patchesV = nasolabial_dir_transplane_data['patchesV']

        mirror = [1, 1, 1]
        if controlZoneDirEnum.right in zone_dir:
            mirror = [-1, 1, 1]

        nasolabial_crvproj_transplane = controlTransPlane(name_prefix = nasolabial_projcrv_transplane_data['name_prefix'],
                                                          name = nasolabial_dir_transplane_data['name'],
                                                          degree = nasolabial_dir_transplane_degree,
                                                          patchesU = nasolabial_dir_transplane_patchesU,
                                                          patchesV = nasolabial_dir_transplane_patchesV,
                                                          translation = nasolabial_dir_transplane_data['xform']['translation'],
                                                          rotation = nasolabial_dir_transplane_data['xform']['rotation'],
                                                          scale = nasolabial_dir_transplane_data['xform']['scale'],
                                                          mirror = mirror,
                                                          cv_list = nasolabial_dir_transplane_data['control_vtx'])

        if controlZoneDirEnum.right in zone_dir:
            g_crv_projsrf_dict['nasolabial_transplane_RUD'] = nasolabial_crvproj_transplane
            cmds.parent(nasolabial_crvproj_transplane.get_name(),
                        hierarchy.nasolabial_ctrlzone_R_grp.get_group_name())
        elif controlZoneDirEnum.left in zone_dir:
            g_crv_projsrf_dict['nasolabial_transplane_LUD'] = nasolabial_crvproj_transplane
            cmds.parent(nasolabial_crvproj_transplane.get_name(),
                        hierarchy.nasolabial_ctrlzone_L_grp.get_group_name())

    # Nasolabial Facial Zone - Projection Surfaces


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

    # ------------------------------------------------------------------------------------------------------------------
    # Eyelid Control Zone

    for dir_dict in CONTROL_ZONE_DIRECTION_DICT[controlZoneEnum.eyelid]:
        zone_dir = util.get_ctrl_zone_dir(dir_dict)[0]

        ctrlproj_transplane_LRUD = None
        ctrlproj_projsrf_LRUD = None

        if controlZoneDirEnum.right in zone_dir:
            if controlZoneDirEnum.up in zone_dir:
                ctrlproj_transplane_LRUD = g_crv_projsrf_dict['eyelid_transplane_RU']
                ctrlproj_projsrf_LRUD = g_crv_projsrf_dict['eyelid_projsrf_RU']
            elif controlZoneDirEnum.down in zone_dir:
                ctrlproj_transplane_LRUD = g_crv_projsrf_dict['eyelid_transplane_RD']
                ctrlproj_projsrf_LRUD = g_crv_projsrf_dict['eyelid_projsrf_RD']
        elif controlZoneDirEnum.left in zone_dir:
            if controlZoneDirEnum.up in zone_dir:
                ctrlproj_transplane_LRUD = g_crv_projsrf_dict['eyelid_transplane_LU']
                ctrlproj_projsrf_LRUD = g_crv_projsrf_dict['eyelid_projsrf_LU']
            elif controlZoneDirEnum.down in zone_dir:
                ctrlproj_transplane_LRUD = g_crv_projsrf_dict['eyelid_transplane_LD']
                ctrlproj_projsrf_LRUD = g_crv_projsrf_dict['eyelid_projsrf_LD']

        assert None != ctrlproj_transplane_LRUD
        assert None != ctrlproj_projsrf_LRUD

        eyelid_ctrl_zone = eyelidControlZone(direction = zone_dir,
                                             ctrl_crv_data = ctrl_crv_data,
                                             ctrlproj_transplane_LRUD = ctrlproj_transplane_LRUD,
                                             ctrlproj_projsurface_LRUD = ctrlproj_projsrf_LRUD)

    # ------------------------------------------------------------------------------------------------------------------
    # Eyebrow Control Zone

    ctrlproj_transplane_LRUD = None
    ctrlproj_transplane_LRFB = None
    ctrlproj_projsrf_LRUD = None
    ctrlproj_projsrf_LRFB = None

    for dir_dict in CONTROL_ZONE_DIRECTION_DICT[controlZoneEnum.eyebrow]:
        zone_dir = util.get_ctrl_zone_dir(dir_dict)[0]

        if controlZoneDirEnum.up in zone_dir and controlZoneDirEnum.down in zone_dir:
            ctrlproj_transplane_LRUD = g_crv_projsrf_dict['eyebrow_transplane_LRUD']
            ctrlproj_projsrf_LRUD = g_crv_projsrf_dict['eyebrow_projsrf_LRUD']
            assert None != ctrlproj_transplane_LRUD
            assert None != ctrlproj_projsrf_LRUD
        elif controlZoneDirEnum.front in zone_dir:
            ctrlproj_transplane_LRFB = g_crv_projsrf_dict['eyebrow_transplane_LRF']
            ctrlproj_projsrf_LRFB = g_crv_projsrf_dict['eyebrow_projsrf_LRF']
            assert None != ctrlproj_transplane_LRFB
            assert None != ctrlproj_projsrf_LRFB

    # Note that the eyebrow facial zone only have one Control Zone, combining the up-down and front directions.
    eyebrow_ctrl_zone = eyebrowControlZone(ctrl_crv_data = ctrl_crv_data,
                                           ctrlproj_transplane_LRUD = ctrlproj_transplane_LRUD,
                                           ctrlproj_transplane_LRFB = ctrlproj_transplane_LRFB,
                                           ctrlproj_projsurface_LRUD = ctrlproj_projsrf_LRUD,
                                           ctrlproj_projsurface_LRFB = ctrlproj_projsrf_LRFB)

    # ------------------------------------------------------------------------------------------------------------------
    # Mouth Control Zone

    ctrlproj_transplane_LRUD = None
    ctrlproj_projsrf_LRUD = None

    for dir_dict in CONTROL_ZONE_DIRECTION_DICT[controlZoneEnum.mouth]:
        zone_dir = util.get_ctrl_zone_dir(dir_dict)[0]

        if controlZoneDirEnum.up in zone_dir:
            ctrlproj_transplane_LRUD = g_crv_projsrf_dict['mouth_transplane_LRU']
            ctrlproj_projsrf_LRUD = g_crv_projsrf_dict['mouth_projsrf_LRU']
        elif controlZoneDirEnum.down in zone_dir:
            ctrlproj_transplane_LRUD = g_crv_projsrf_dict['mouth_transplane_LRD']
            ctrlproj_projsrf_LRUD = g_crv_projsrf_dict['mouth_projsrf_LRD']

        assert None != ctrlproj_transplane_LRUD
        assert None != ctrlproj_projsrf_LRUD

        # Note that the eyebrow facial zone only have one Control Zone, combining the up-down and front directions.
        eyebrow_ctrl_zone = mouthControlZone(direction = zone_dir,
                                             ctrl_crv_data = ctrl_crv_data,
                                             ctrlproj_transplane_LRUD = ctrlproj_transplane_LRUD,
                                             ctrlproj_projsurface_LRUD = ctrlproj_projsrf_LRUD)

    f_ctrl_crv_data.close()

def setup_group_hierarchy():
    """
    :return: None
    """

    eyelid_grp = hierarchy.eyelid_grp
    eyelid_grp.setup_group_hierarchy()

    eyebrow_grp = hierarchy.eyebrow_grp
    eyebrow_grp.setup_group_hierarchy()

    mouth_grp = hierarchy.mouth_grp
    mouth_grp.setup_group_hierarchy()

    nasolabial_grp = hierarchy.nasolabial_grp
    nasolabial_grp.setup_group_hierarchy()

# Entry point ==========================================================================================================
# lc3chr_facialsys_construct()