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
    setup_ctrl_locs()
    setup_ctrl_data_transfer()

def setup_proj_planes():
    """ Import or create the projection planes for the controllers and locators.
    :return: None
    """

    # Loading the curve projection planes' data from the json document.
    try:
        root_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../'))
        # print('lv3 character facial module root path: {}'.format(root_path))
        f_crv_proj_plane_data = open(root_path+'/template/crv_proj_plane.json', 'r')
        crv_proj_plane_data = json.load(f_crv_proj_plane_data)
    except:
        cmds.error('Error thrown while setting up the data curve projection plane: {}'.format(
            sys.exc_info()[0]
        ))

    # Create the controller translation planes
    crv_proj_transplane_data = crv_proj_plane_data['translation_plane']
    crv_proj_transplane_degree = crv_proj_transplane_data['degree']
    crv_proj_transplane_patchesU = crv_proj_transplane_data['patchesU']
    crv_proj_transplane_patchesV = crv_proj_transplane_data['patchesV']

    # translation plane right-up
    eyelidctrl_transplane_RU_data = crv_proj_transplane_data['right_up']

    eyelidctrl_transplane_RU = curveTransPlane(eyelidctrl_transplane_RU_data['name'],
                                               crv_proj_transplane_degree,
                                               crv_proj_transplane_patchesU,
                                               crv_proj_transplane_patchesV,
                                               eyelidctrl_transplane_RU_data['xform']['translation'],
                                               eyelidctrl_transplane_RU_data['xform']['rotation'],
                                               eyelidctrl_transplane_RU_data['xform']['scale'],
                                               [-1, 1, 1])

    # translation plane right-down
    eyelidctrl_transplane_RD_data = crv_proj_transplane_data['right_dn']

    eyelidctrl_transplane_RD = curveTransPlane(eyelidctrl_transplane_RD_data['name'],
                                               crv_proj_transplane_degree,
                                               crv_proj_transplane_patchesU,
                                               crv_proj_transplane_patchesV,
                                               eyelidctrl_transplane_RD_data['xform']['translation'],
                                               eyelidctrl_transplane_RD_data['xform']['rotation'],
                                               eyelidctrl_transplane_RD_data['xform']['scale'],
                                               [-1, 1, 1])

    # translation plane left-up
    eyelidctrl_transplane_LU_data = crv_proj_transplane_data['left_up']

    eyelidctrl_transplane_LU = curveTransPlane(eyelidctrl_transplane_LU_data['name'],
                                               crv_proj_transplane_degree,
                                               crv_proj_transplane_patchesU,
                                               crv_proj_transplane_patchesV,
                                               eyelidctrl_transplane_LU_data['xform']['translation'],
                                               eyelidctrl_transplane_LU_data['xform']['rotation'],
                                               eyelidctrl_transplane_LU_data['xform']['scale'])

    # translation plane left-down
    eyelidctrl_transplane_LD_data = crv_proj_transplane_data['left_dn']

    eyelidctrl_transplane_LD = curveTransPlane(eyelidctrl_transplane_LD_data['name'],
                                               crv_proj_transplane_degree,
                                               crv_proj_transplane_patchesU,
                                               crv_proj_transplane_patchesV,
                                               eyelidctrl_transplane_LD_data['xform']['translation'],
                                               eyelidctrl_transplane_LD_data['xform']['rotation'],
                                               eyelidctrl_transplane_LD_data['xform']['scale'])

    # # Create the controller projection planes
    # eyelidctrl_projplane_RU = cmds.nurbsPlane()
    #
    # eyelidctrl_projplane_RU = cmds.rename(eyelidctrl_projplane_RU, 'fm_eyelidFaceMask_RU_nbs')
    # eyelidctrl_projplane_RD = cmds.nurbsPlane()
    # eyelidctrl_projplane_RD = cmds.rename(eyelidctrl_projplane_RD, 'fm_eyelidFaceMask_RD_nbs')
    # eyelidctrl_projplane_LU = cmds.nurbsPlane()
    # eyelidctrl_projplane_LU = cmds.rename(eyelidctrl_projplane_LU, 'fm_eyelidFaceMask_LU_nbs')
    # eyelidctrl_projplane_LD = cmds.nurbsPlane()
    # eyelidctrl_projplane_LD = cmds.rename(eyelidctrl_projplane_LD, 'fm_eyelidFaceMask_LD_nbs')

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