#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# Author: Sheng (Raymond) Liao
# Date: August 2021
#

'''
module for transforming objects from one space to another.
'''

# ----------------------------------------------------------------------------------------------------------------------
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

# ----------------------------------------------------------------------------------------------------------------------
def ParentTo( objs, newParent ):
    '''
    Reparent objects.
    :param objs: objects to be reparented
    :param newParent: objects to be reparented to
    :return: none
    '''

    if None == objs:
        cmds.warning( "[lcTransform.ParentTo] Please pass in valid object nodes to be re-parented." )
        return
    if None == newParent:
        cmds.warning( "[lcTransform.ParentTo] Please pass in a valid new parent node." )

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

def TransformCurve(curve, transformNode, newCurveName="transformedCrv"):
    '''
    Transform a curve from one space to another.
    :param curve: the NURBS curve to be transformed
    :param transformNode: A functional node to transform the curve
    :param name: the name of the curve after being transformed
    :return: the transformed curve
    '''

    if None == curve:
        cmds.warning( "[lcTransform.TransformCrv] Please pass in a valid NURBS curve." )
        return
    if None == transformNode:
        cmds.warning( "[lcTransform.TransformCrv] Please pass in a valid transform node." )

    lastIdx = cmds.getAttr( transformNode + ".inputCurves", size=True )
    cmds.connectAttr( curve + ".worldSpace[0]", transformNode + ".inputCurves[" + str(lastIdx) + "]" )
    transformedCrvShape = cmds.createNode( "nurbsCurve" )
    cmds.connectAttr( transformNode + ".outputCurves[" + str(lastIdx) + "]", transformedCrvShape + ".create")
    transformedCrv = cmds.listRelatives( transformedCrvShape, p=1 )[0]
    transformedCrv = cmds.rename( transformedCrv, newCurveName )

    return transformedCrv