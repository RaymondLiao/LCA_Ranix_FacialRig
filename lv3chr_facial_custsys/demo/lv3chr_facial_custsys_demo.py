#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# File Name: lv3chr_facial_custsys_demo.py
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

from control import crv_proj_plane; reload(crv_proj_plane)
from control.crv_proj_plane import curveTransPlane, curveProjPlane

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

def lc3chr_facialsys_construct():

    setup_proj_planes()
    setup_ctrl_crvs()
    setup_ctrl_locs()
    setup_ctrls()
    setup_ctrl_data_transfer()

def setup_proj_planes():
    """ Import or create the projection planes for the controllers and locators.
    :return: None
    """

    # Loading the curve projection planes' data from the json document.
    try:
        root_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../'))
        # print('lv3 character facial module root path: {}'.format(root_path))
        f_crv_proj_plane_data = open(root_path+'/template/crv_proj_plane_data.json', 'r')
        crv_proj_plane_data = json.load(f_crv_proj_plane_data)
    except:
        cmds.error('Error thrown while setting up the data curve projection plane: {}'.format(
            sys.exc_info()[0]
        ))
    crv_proj_plane_dir_list = ['right_up', 'right_dn', 'left_up', 'left_dn']

    # Create the controller translation planes
    crv_proj_transplane_data = crv_proj_plane_data['translation_plane']
    crv_proj_transplane_degree = crv_proj_transplane_data['degree']
    crv_proj_transplane_patchesU = crv_proj_transplane_data['patchesU']
    crv_proj_transplane_patchesV = crv_proj_transplane_data['patchesV']

    for dir in crv_proj_plane_dir_list:
        eyelidctrl_transplane_data = crv_proj_transplane_data[dir]

        mirror = [1, 1, 1]
        if 'right' in dir:
            mirror = [-1, 1, 1]

        eyelidctrl_transplane = curveTransPlane(name = eyelidctrl_transplane_data['name'],
                                                degree = crv_proj_transplane_degree,
                                                patchesU = crv_proj_transplane_patchesU,
                                                patchesV = crv_proj_transplane_patchesV,
                                                translation = eyelidctrl_transplane_data['xform']['translation'],
                                                rotation = eyelidctrl_transplane_data['xform']['rotation'],
                                                scale = eyelidctrl_transplane_data['xform']['scale'],
                                                mirror = mirror)

    # Create the controller projection planes
    crv_proj_projplane_data = crv_proj_plane_data['projection_plane']
    crv_proj_projplane_degree = crv_proj_projplane_data['degree']
    crv_proj_projplane_patchesU = crv_proj_projplane_data['patchesU']
    crv_proj_projplane_patchesV = crv_proj_projplane_data['patchesV']

    for dir in crv_proj_plane_dir_list:
        eyelidctrl_projplane_data = crv_proj_projplane_data[dir]

        mirror = [1, 1, 1]
        if 'right' in dir:
            mirror = [-1, 1, 1]

        eyelidctrl_projplane = curveProjPlane(name = eyelidctrl_projplane_data['name'],
                                              degree = crv_proj_projplane_degree,
                                              patchesU = crv_proj_projplane_patchesU,
                                              patchesV = crv_proj_projplane_patchesV,
                                              translation = eyelidctrl_projplane_data['xform']['translation'],
                                              rotation = eyelidctrl_projplane_data['xform']['rotation'],
                                              scale = eyelidctrl_projplane_data['xform']['scale'],
                                              cv_list = eyelidctrl_projplane_data['control_vtx'],
                                              mirror = mirror)

    f_crv_proj_plane_data.close()

def setup_ctrl_crvs():
    """ Create the facial controlling NURBS curves.
    :return: None
    """
    # cmds.warning('[setup_ctrl_crvs] No Implementation')
    pass

    # Left Eyes

    # Right Eyes


def setup_ctrl_locs():
    """ Create the locators on the controlling curves and the projection planes.
    :return: None
    """
    # cmds.warning('[setup_ctrl_locs] No Implementation')
    pass

def setup_ctrls():
    """ Create the NURBS primitives as the facial controllers.
    :return: None
    """
    # cmds.warning('[setup_ctrls] No Implementation')
    pass

def setup_ctrl_data_transfer():
    """ Create the joints, bind-skin on the controlling curves; \
    establish the blend-shapes among curves and pointOnXXX nodes for the controller translation data transfer network.
    :return: None
    """
    # cmds.warning('[setup_ctrl_data_transfer] No Implementation')
    pass



# Entry point ==========================================================================================================
lc3chr_facialsys_construct()