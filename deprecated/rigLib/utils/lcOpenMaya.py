#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# Author: Sheng (Raymond) Liao
# Date: June 2021
#

'''
module for facilitating exploiting the Maya Python API functionalities.
'''

import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

def getMObjectName( mobject ):
    '''
    Retrieve its MDagPath from an MObject
    :param mobject: The object to get the DAG path from.
    :type mobject: OpenMaya.MObject
    '''

#region ToBeImplemented
    # Put an assert here to guarantee that mobject is an OpenMaya.MObject
#endregion

    if not mobject.hasFn( OpenMaya.MFn.kDagNode ):
        raise Exception( "[lcOpenMaya] Object" + mobject + "is not a valid DAG node.")

    dagPath = OpenMaya.MDagPath()
    OpenMaya.MDagPath.getAPathTo( mobject, dagPath )
    fullName = dagPath.fullPathName().split('|')
    if len(fullName) > 0:
        name = fullName[-1]
    else:
        name = fullName[0]

    return name