#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# File Name: lc3chr_facial_custsys_demo.py
# Author: Sheng (Raymond) Liao
# Date: October 2021
#

"""
A module to procedurally rig LCA's level three characters' head model (demo).
"""

import maya.cmds as cmds

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

    # Create the controller translation planes
    eyelidctrl_transplane_RU = cmds.nurbsPlane(degree=1, patchesU=4, patchesV=6)
    cmds.xform(eyelidctrl_transplane_RU, translation=[4.0, 16.0, 0.0], rotation=[90.0, 0.0, 0.0], scale=[4.0, 1.0, 4.8])
    cmds.makeIdentity(eyelidctrl_transplane_RU, apply=True)
    cmds.xform(eyelidctrl_transplane_RU, scale=[-1, 0, 0])  # mirroring
    eyelidctrl_transplane_RU = cmds.rename(eyelidctrl_transplane_RU, 'fm_eyelidProjectPlane_RU_nbs')

    eyelidctrl_transplane_RD = cmds.nurbsPlane(degree=1, patchesU=4, patchesV=6)
    cmds.xform(eyelidctrl_transplane_RD, translation=[4.0, 16.0, 0.0], rotation=[90.0, 0.0, 0.0], scale=[4.0, 1.0, 4.8])
    cmds.makeIdentity(eyelidctrl_transplane_RU, apply=True)
    cmds.xform(eyelidctrl_transplane_RD, scale=[-1, 0, 0])
    eyelidctrl_transplane_RD = cmds.rename(eyelidctrl_transplane_RD, 'fm_eyelidProjectPlane_RD_nbs')

    eyelidctrl_transplane_LU = cmds.nurbsPlane(degree=1, patchesU=4, patchesV=6)
    cmds.xform(eyelidctrl_transplane_LU, translation=[9.0, 16.0, 0.0], rotation=[90.0, 0.0, 0.0], scale=[4.0, 1.0, 4.8])
    cmds.makeIdentity(eyelidctrl_transplane_LU, apply=True)
    eyelidctrl_transplane_LU = cmds.rename(eyelidctrl_transplane_LU, 'fm_eyelidProjectPlane_LU_nbs')

    eyelidctrl_transplane_LD = cmds.nurbsPlane(degree=1, patchesU=4, patchesV=6)
    cmds.xform(eyelidctrl_transplane_LD, translation=[9.0, 16.0, 0.0], rotation=[90.0, 0.0, 0.0], scale=[4.0, 1.0, 4.0])
    cmds.makeIdentity(eyelidctrl_transplane_LD, apply=True)
    eyelidctrl_transplane_LD = cmds.rename(eyelidctrl_transplane_LD, 'fm_eyelidProjectPlane_LD_nbs')

    # Create the controller projection planes
    eyelidctrl_projplane_RU = cmds.nurbsPlane()
    cmds.xform()
    eyelidctrl_projplane_RU = cmds.rename(eyelidctrl_projplane_RU, 'fm_eyelidFaceMask_RU_nbs')
    eyelidctrl_projplane_RD = cmds.nurbsPlane()
    eyelidctrl_projplane_RD = cmds.rename(eyelidctrl_projplane_RD, 'fm_eyelidFaceMask_RD_nbs')
    eyelidctrl_projplane_LU = cmds.nurbsPlane()
    eyelidctrl_projplane_LU = cmds.rename(eyelidctrl_projplane_LU, 'fm_eyelidFaceMask_LU_nbs')
    eyelidctrl_projplane_LD = cmds.nurbsPlane()
    eyelidctrl_projplane_LD = cmds.rename(eyelidctrl_projplane_LD, 'fm_eyelidFaceMask_LD_nbs')

def setup_ctrl_crvs():
    """ Create the facial controlling NURBS curves.
    :return: None
    """
    cmds.warning('[setup_ctrl_crvs] No Implementation')
    pass

    # Left Eyes

    # Right Eyes


def setup_ctrl_locs():
    """ Create the locators on the controlling curves and the projection planes.
    :return: None
    """
    cmds.warning('[setup_ctrl_locs] No Implementation')
    pass

def setup_ctrls():
    """ Create the NURBS primitives as the facial controllers.
    :return: None
    """
    cmds.warning('[setup_ctrls] No Implementation')
    pass

def setup_ctrl_data_transfer():
    """ Create the joints, bind-skin on the controlling curves; \
    establish the blend-shapes among curves and pointOnXXX nodes for the controller translation data transfer network.
    :return: None
    """
    cmds.warning('[setup_ctrl_data_transfer] No Implementation')
    pass



# Entry point ==========================================================================================================
lc3chr_facialsys_construct()