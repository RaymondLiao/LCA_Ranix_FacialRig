#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# Author: Sheng (Raymond) Liao
# Date: June 2021
#

'''
module for transforming objects from one space to another.
'''

import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

def ParentTo( objs, newParent ):
    '''
    Reparent objects.
    :param objs: objects to be reparented
    :param newParent: objects to be reparented to
    :return: none
    '''

    if (objs == None):
        cmds.warning( "[lca_transform.ParentTo] Please pass valid object nodes to be re-parented." )
        return
    if (newParent == None):
        cmds.warning( "[lca_transform.ParentTo] Please pass a valid new parent node." )

    sels = OpenMaya.MSelectionList()
    cmds.select( objs, newParent )
    OpenMaya.MGlobal.getActiveSelectionList(sels)
    selCount = sels.length()

    parent = OpenMaya.MObject()
    sels.getDependNode( selCount - 1, parent )

    for i in range( selCount - 1 ):
        dagFn = OpenMaya.MDagModifier()
        child = OpenMaya.MObject()
        sels.getDependNode(i, child)
        dagFn.reparentNode(child, parent)
        dagFn.doIt()

def TransformCrv(curve, transformNode, name="transformedCrv"):
    '''
    Transform a curve from one space to another.
    :param curve: the NURBS curve to be transformed
    :param transformNode: A functional node to transform the curve
    :param name: the name of the curve after being transformed
    :return: the transformed curve
    '''

    if (curve == None):
        cmds.warning( "[lca_transform.TransformCrv] Please pass a valid NURBS curve " )

    lastIdx = cmds.getAttr( transformNode + ".inputGeom", size=True )
    cmds.connectAttr( curve + ".worldSpace[0]", transformNode + ".inputGeom[" + str(lastIdx) + "]" )