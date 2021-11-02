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

from general import lv3chr_facialsys_config; reload(lv3chr_facialsys_config)

from control import crv_proj_plane; reload(crv_proj_plane)
from control.crv_proj_plane import curveTransPlane, curveProjPlane

from control import ctrl_curve; reload(ctrl_curve)
from control.ctrl_curve import controlCurve

def lc3chr_facialsys_construct():

    setup_proj_planes()
    setup_ctrl_crvs()
    # setup_ctrl_locs()
    # setup_ctrls()
    setup_ctrl_data_transfer()

def setup_proj_planes():
    """ Create the projection planes containing locators and joints.

    # controller translation planes' names:
    # -- fm_eyelidProjectPlane_RU_nbs
    # -- fm_eyelidProjectPlane_RD_nbs
    # -- fm_eyelidProjectPlane_LU_nbs
    # -- fm_eyelidProjectPlane_LD_nbs

    # controller (translation) projection planes' names:
    # -- fm_eyelidFaceMask_RU_nbs
    # -- fm_eyelidFaceMask_RD_nbs
    # -- fm_eyelidFaceMask_LU_nbs
    # -- fm_eyelidFaceMask_LD_nbs

    :return: None
    """

    proj_srf_shader = cmds.shadingNode('lambert', asShader=True, name=lv3chr_facialsys_config.PROJ_PLANE_SHADER)
    cmds.setAttr(proj_srf_shader + '.transparency', 0.25, 0.25, 0.25, type='double3')
    proj_srf_shader_SG = cmds.sets(name=proj_srf_shader+'_SG',
                                   renderable=True, noSurfaceShader=True, empty=True,)
    cmds.connectAttr(proj_srf_shader+'.outColor', proj_srf_shader_SG+'.surfaceShader', force=True)

    # Load the curve projection planes' data from the json document.
    try:
        root_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../'))
        # print('lv3 character facial module root path: {}'.format(root_path))
        f_crv_proj_plane_data = open(root_path+'/template/crv_proj_plane_data.json', 'r')
        crv_proj_plane_data = json.load(f_crv_proj_plane_data)
    except:
        cmds.error('Error thrown while loading the data curve projection planes data: {}'.format(
            sys.exc_info()[0]
        ))
    crv_proj_plane_dir_list = ['right_up', 'right_dn', 'left_up', 'left_dn']

    # Create the controller translation planes.
    eyelid_crvproj_transplane_data = crv_proj_plane_data['eyelid_translation_plane']
    eyelid_crvproj_transplane_degree = eyelid_crvproj_transplane_data['degree']
    eyelid_crvproj_transplane_patchesU = eyelid_crvproj_transplane_data['patchesU']
    eyelid_crvproj_transplane_patchesV = eyelid_crvproj_transplane_data['patchesV']

    for dir in crv_proj_plane_dir_list:
        eyelid_dir_transplane_data = eyelid_crvproj_transplane_data[dir]

        mirror = [1, 1, 1]
        if 'right' in dir:
            mirror = [-1, 1, 1]

        eyelid_crvproj_transplane = curveTransPlane(name = eyelid_dir_transplane_data['name'],
                                                    degree = eyelid_crvproj_transplane_degree,
                                                    patchesU = eyelid_crvproj_transplane_patchesU,
                                                    patchesV = eyelid_crvproj_transplane_patchesV,
                                                    translation = eyelid_dir_transplane_data['xform']['translation'],
                                                    rotation = eyelid_dir_transplane_data['xform']['rotation'],
                                                    scale = eyelid_dir_transplane_data['xform']['scale'],
                                                    mirror = mirror)

    # Create the controller projection planes
    eyelid_crvproj_projplane_data = crv_proj_plane_data['eyelid_projection_plane']
    eyelid_crvproj_projplane_degree = eyelid_crvproj_projplane_data['degree']
    eyelid_crvproj_projplane_patchesU = eyelid_crvproj_projplane_data['patchesU']
    eyelid_crvproj_projplane_patchesV = eyelid_crvproj_projplane_data['patchesV']

    for dir in crv_proj_plane_dir_list:
        eyelid_dir_projplane_data = eyelid_crvproj_projplane_data[dir]

        mirror = [1, 1, 1]
        if 'right' in dir:
            mirror = [-1, 1, 1]

        eyelid_crvproj_projplane = curveProjPlane(name = eyelid_dir_projplane_data['name'],
                                                  degree = eyelid_crvproj_projplane_degree,
                                                  patchesU = eyelid_crvproj_projplane_patchesU,
                                                  patchesV = eyelid_crvproj_projplane_patchesV,
                                                  translation = eyelid_dir_projplane_data['xform']['translation'],
                                                  rotation = eyelid_dir_projplane_data['xform']['rotation'],
                                                  scale = eyelid_dir_projplane_data['xform']['scale'],
                                                  cv_list = eyelid_dir_projplane_data['control_vtx'],
                                                  mirror = mirror)

    f_crv_proj_plane_data.close()

def setup_ctrl_crvs():
    """ Create the facial controlling NURBS curves.
    :return: None
    """

    # Control curves' names:
    # -- fm_eyelidProject_RU_A_curve
    # -- fm_eyelidProject_RU_B_curve
    # -- fm_eyelidProject_RU_C_curve
    # -- fm_eyelidProject_RU_D_curve

    # -- fm_eyelidProject_RD_A_curve
    # -- fm_eyelidProject_RD_B_curve
    # -- fm_eyelidProject_RD_C_curve
    # -- fm_eyelidProject_RD_D_curve

    # -- fm_eyelidProject_LU_A_curve
    # -- fm_eyelidProject_LU_B_curve
    # -- fm_eyelidProject_LU_D_curve
    # -- fm_eyelidProject_LU_D_curve

    # -- fm_eyelidProject_LD_A_curve
    # -- fm_eyelidProject_LD_B_curve
    # -- fm_eyelidProject_LD_C_curve
    # -- fm_eyelidProject_LD_D_curve

    # Load the control curves' data from the json document.
    try:
        root_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../'))

        f_ctrl_crv_data = open(root_path+'/template/control_crv_data.json', 'r')
        ctrl_crv_data = json.load(f_ctrl_crv_data)
    except:
        cmds.error('Error thrown while loading the control curves data: {}'.format(
            sys.exc_info()[0]
        ))

    ctrl_crv_dir_list = ['right_up', 'right_dn', 'left_up', 'left_dn']
    ctrl_crv_id_list = ['A', 'B', 'C', 'D']

    # Create the control curves.
    eyelid_ctrlcrv_data = ctrl_crv_data['eyelid_control_curve']
    eyelid_ctrlcrv_degree = eyelid_ctrlcrv_data['degree']

    for dir in ctrl_crv_dir_list:
        for id in ctrl_crv_id_list:
            eyelid_dir_ctrlcrv_data = eyelid_ctrlcrv_data[dir+'_'+id]
            eyelid_ctrl_crv = controlCurve(name = eyelid_dir_ctrlcrv_data['name'],
                                           degree = eyelid_ctrlcrv_degree,
                                           points = eyelid_dir_ctrlcrv_data['points'],
                                           translation = eyelid_dir_ctrlcrv_data['xform']['translation'])


# def setup_ctrl_locs():
#     """ Create the locators on the controlling curves and the projection planes.
#     :return: None
#     """
#     # cmds.warning('[setup_ctrl_locs] No Implementation')
#     pass
#
# def setup_ctrls():
#     """ Create the NURBS primitives as the facial controllers.
#     :return: None
#     """
#     # cmds.warning('[setup_ctrls] No Implementation')
#     pass

def setup_ctrl_data_transfer():
    """ Create the joints, bind-skin on the controlling curves; \
    establish the blend-shapes among curves and pointOnXXX nodes for the controller translation data transfer network.
    :return: None
    """
    # cmds.warning('[setup_ctrl_data_transfer] No Implementation')
    pass



# Entry point ==========================================================================================================
lc3chr_facialsys_construct()