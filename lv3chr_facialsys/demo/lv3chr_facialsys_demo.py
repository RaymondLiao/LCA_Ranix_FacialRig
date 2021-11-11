#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# File Name: lv3chr_facialsys_demo.py
# Author: Sheng (Raymond) Liao
# Date: October 2021
#

"""
A module to procedurally rig LCA's level three characters' head model (demo).
"""

import os
import sys
import json

import maya.cmds as cmds
import maya.mel as mel

from general import lv3chr_facialsys_config; reload(lv3chr_facialsys_config)
from general.lv3chr_facialsys_config import *

from general import lv3chr_facialsys_hierarchy; reload(lv3chr_facialsys_hierarchy)

from control import control_proj_surface; reload(control_proj_surface)
from control.control_proj_surface import controlTransPlane, controlProjSurface

from control import control_curve; reload(control_curve)
from control.control_curve import controlCurve

from control import controller; reload(controller)
from control.controller import controller

from control import control_zone; reload(control_zone)
from control.control_zone import controlZone

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

# function definitions -------------------------------------------------------------------------------------------------
def lc3chr_facialsys_construct():

    # We must establish the group hierarchy first,
    # in order to organize the rig elements that will be created later in the Outliner.
    setup_group_hierarchy()
    assert cmds.objExists(lv3chr_facialsys_hierarchy.eyelid_grp.get_group_name())

    setup_proj_surface()
    setup_ctrl_zones()
    setup_ctrl_data_transfer()

    # Do clean-up.
    cmds.select(deselect=True)
    mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes")')

def setup_proj_surface():
    """ Create the projection planes containing locator_data and joints.
    :return: None
    """

    proj_srf_shader = cmds.shadingNode('lambert', asShader=True, name=PROJ_SRF_SHADER)
    cmds.setAttr(proj_srf_shader+'.color', 0.0, 0.0, 0.0, type='double3')
    cmds.setAttr(proj_srf_shader+'.transparency', 0.85, 0.85, 0.85, type='double3')
    proj_srf_shader_SG = cmds.sets(name=proj_srf_shader+'_SG',
                                   renderable=True, empty=True,)
    cmds.connectAttr(proj_srf_shader+'.outColor', proj_srf_shader_SG+'.surfaceShader', force=True)

    # Load the curve projection planes' data from the JSON document.
    root_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../'))

    control_proj_surface_data = {}
    try:
        # print('lv3 character facial module root path: {}'.format(root_path))
        f_control_proj_surface_data = open(root_path+'/template/control_proj_surface_data.json', 'r')
        control_proj_surface_data = json.load(f_control_proj_surface_data)
    except:
        cmds.error('Error thrown while loading the data curve projection planes data: {}'.format(
            sys.exc_info()[0]
        ))

    # Create the controller translation planes.
    eyelid_crvproj_transplane_data = control_proj_surface_data['eyelid_translation_plane']
    eyelid_crvproj_transplane_degree = eyelid_crvproj_transplane_data['degree']
    eyelid_crvproj_transplane_patchesU = eyelid_crvproj_transplane_data['patchesU']
    eyelid_crvproj_transplane_patchesV = eyelid_crvproj_transplane_data['patchesV']

    for dir in control_zone_dir_list:
        eyelid_dir_transplane_data = eyelid_crvproj_transplane_data[dir]

        mirror = [1, 1, 1]
        if 'r' in dir:
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
        if controlZoneDirEnum.right_up == dir:
            cmds.parent(eyelid_crvproj_transplane.get_name(),
                        lv3chr_facialsys_hierarchy.eyelid_ctrlcrv_RU_grp.get_group_name())
            g_crv_projsrf_dict['eyelid_transplane_RU'] = eyelid_crvproj_transplane.get_name()
        elif controlZoneDirEnum.right_dn == dir:
            cmds.parent(eyelid_crvproj_transplane.get_name(),
                        lv3chr_facialsys_hierarchy.eyelid_ctrlcrv_RD_grp.get_group_name())
            g_crv_projsrf_dict['eyelid_transplane_RD'] = eyelid_crvproj_transplane.get_name()
        elif controlZoneDirEnum.left_up == dir:
            cmds.parent(eyelid_crvproj_transplane.get_name(),
                        lv3chr_facialsys_hierarchy.eyelid_ctrlcrv_LU_grp.get_group_name())
            g_crv_projsrf_dict['eyelid_transplane_LU'] = eyelid_crvproj_transplane.get_name()
        elif controlZoneDirEnum.left_dn == dir:
            cmds.parent(eyelid_crvproj_transplane.get_name(),
                        lv3chr_facialsys_hierarchy.eyelid_ctrlcrv_LD_grp.get_group_name())
            g_crv_projsrf_dict['eyelid_transplane_LD'] = eyelid_crvproj_transplane.get_name()

    # Create the controller projection surfaces
    eyelid_crvproj_projsrf_data = control_proj_surface_data['eyelid_projection_surface']
    eyelid_crvproj_projsrf_degree = eyelid_crvproj_projsrf_data['degree']
    eyelid_crvproj_projsrf_patchesU = eyelid_crvproj_projsrf_data['patchesU']
    eyelid_crvproj_projsrf_patchesV = eyelid_crvproj_projsrf_data['patchesV']

    for dir in control_zone_dir_list:
        eyelid_dir_projsrf_data = eyelid_crvproj_projsrf_data[dir]

        mirror = [1, 1, 1]
        if 'r' in dir:
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
                                                    locator_scale = eyelid_crvproj_projsrf_data['locator_scale'])

        if controlZoneDirEnum.right_up == dir:
            cmds.parent(eyelid_crvproj_projsrf.get_name(),
                        lv3chr_facialsys_hierarchy.eyelid_projsrf_RU_grp.get_group_name())
            g_crv_projsrf_dict['eyelid_projsrf_RU'] = eyelid_crvproj_projsrf.get_name()
        elif controlZoneDirEnum.right_dn == dir:
            cmds.parent(eyelid_crvproj_projsrf.get_name(),
                        lv3chr_facialsys_hierarchy.eyelid_projsrf_RD_grp.get_group_name())
            g_crv_projsrf_dict['eyelid_projsrf_RD'] = eyelid_crvproj_projsrf.get_name()
        elif controlZoneDirEnum.left_up == dir:
            cmds.parent(eyelid_crvproj_projsrf.get_name(),
                        lv3chr_facialsys_hierarchy.eyelid_projsrf_LU_grp.get_group_name())
            g_crv_projsrf_dict['eyelid_projsrf_LU'] = eyelid_crvproj_projsrf.get_name()
        elif controlZoneDirEnum.left_dn == dir:
            cmds.parent(eyelid_crvproj_projsrf.get_name(),
                        lv3chr_facialsys_hierarchy.eyelid_projsrf_LD_grp.get_group_name())
            g_crv_projsrf_dict['eyelid_projsrf_LD'] = eyelid_crvproj_projsrf.get_name()

    f_control_proj_surface_data.close()

def setup_ctrl_zones():
    """ Create the facial controlling NURBS curves.
    :return: None
    """

    # Load the control curves' and controllers' data from the JSON document.
    root_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../'))

    ctrl_crv_data = {}
    try:
        f_ctrl_crv_data = open(root_path+'/template/control_crv_data.json', 'r')
        ctrl_crv_data = json.load(f_ctrl_crv_data)
    except:
        cmds.error('Error thrown while loading the control curves data: {}'.format(
            sys.exc_info()[0]
        ))

    # Create the control zones.
    for dir in control_zone_dir_list:

        ctrlproj_transplane = None
        if 'r' in dir:
            if 'u' in dir:
                ctrlproj_transplane = g_crv_projsrf_dict['eyelid_transplane_RU']
            elif 'd' in dir:
                ctrlproj_transplane = g_crv_projsrf_dict['eyelid_transplane_RD']
        elif 'l' in dir:
            if 'u' in dir:
                ctrlproj_transplane = g_crv_projsrf_dict['eyelid_transplane_LU']
            elif 'd' in dir:
                ctrlproj_transplane = g_crv_projsrf_dict['eyelid_transplane_LD']
        assert None != ctrlproj_transplane

        ctrlproj_projsrf = None
        if 'r' in dir:
            if 'u' in dir:
                ctrlproj_projsrf = g_crv_projsrf_dict['eyelid_projsrf_RU']
            elif 'd' in dir:
                ctrlproj_projsrf = g_crv_projsrf_dict['eyelid_projsrf_RD']
        elif 'l' in dir:
            if 'u' in dir:
                ctrlproj_projsrf = g_crv_projsrf_dict['eyelid_projsrf_LU']
            elif 'd' in dir:
                ctrlproj_projsrf = g_crv_projsrf_dict['eyelid_projsrf_LD']
        assert None != ctrlproj_projsrf

        eyelid_ctrl_zone = controlZone(zone=controlZoneEnum.eyelid,
                                       direction=dir,
                                       ctrl_crv_data=ctrl_crv_data,
                                       ctrlproj_transplane=ctrlproj_transplane,
                                       ctrlproj_projsurface=ctrlproj_projsrf)


def setup_ctrl_locs():
    """ Create the locator_data on the controlling curves and the projection planes.
    :return: None
    """
    return NotImplemented

def setup_ctrls():
    """ Create the NURBS primitives as the facial controllers.
    :return: None
    """
    return NotImplemented

def setup_ctrl_data_transfer():
    """ Create the joints, bind-skin on the controlling curves; \
    establish the blend-shapes among curves and pointOnXXX nodes for the controller translation data transfer network.
    :return: None
    """
    return NotImplemented

def setup_group_hierarchy():
    """
    :return: None
    """

    eyelid_grp = lv3chr_facialsys_hierarchy.eyelid_grp
    eyelid_grp.setup_group_hierarchy()

# Entry point ==========================================================================================================
lc3chr_facialsys_construct()