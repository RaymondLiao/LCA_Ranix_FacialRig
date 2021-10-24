#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# Author: Sheng (Raymond) Liao
# Date: August 2021
#

'''
module for facilitating querying, calculating or manipulating NURBS surfaces' relevant data.
Notate that some of the functions were copied or written through taking modules from the github repository "bungnoid/glTools" as references.
'''

# ----------------------------------------------------------------------------------------------------------------------
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

import math

# ----------------------------------------------------------------------------------------------------------------------
def isSurface( surface ):
    '''
    Check if the specified object is a nurbs surface or transform parent of a surface.
    :param surface: The object to query
    :type surface: str
    '''

    # Check if the object exists
    if not cmds.objExists( surface ):
        return False
    # Check the corresponding shape node if 'surface' is a transform node.
    if cmds.objectType( surface ) == 'transform':
        surface = cmds.listRelatives( surface, shapes=True, noIntermediate=True, path=True )
    if cmds.objectType( surface ) != "nurbsSurface":
        return False

    return True

def getSurfaceFn( surface ):
    '''
    Create an MFnNurbsSurface class object from the specified nurbs surface.
    :param surface: The NURBS surface to create the function class for
    :type surface: str
    '''

    # Checks
    if not isSurface( surface ):
        raise Exception( "[lcSurface] Object " + surface + " is not a valid NURBS surface!" )
    if cmds.objectType( surface ) == "transform":
        surface = cmds.listRelatives( surface, shapes=True, noIntermediate=True, path=True )[0]

    # Get the MFnNurbsSurface object.
    selection = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getSelectionListByName( surface, selection )
    surfacePath = OpenMaya.MDagPath()
    selection.getDagPath( 0, surfacePath )
    surfaceFn = OpenMaya.MFnNurbsSurface()
    surfaceFn.setObject( surfacePath )

    return surfaceFn