#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# Author: Sheng (Raymond) Liao
# Date: June 2021
#

'''
custom node to project curves onto a NURBS surface
'''

import math, sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

from LCA_Ranix_FacialRig.rigLib.utils import lcOpenMaya
from LCA_Ranix_FacialRig.rigLib.utils import lcSurface

kPluginNodeTypeName = "lcProjCurvesToSurface"
projCrvNodeId = OpenMaya.MTypeId( 0x1ca00028 )

class lcProjCrvsNode( OpenMayaMPx.MPxNode ):
    # member variables
    inputSurfacePlug        = OpenMaya.MObject()
    inputSurface            = OpenMaya.MObject()
    inputSrfDirty           = False

    inputCurvesPlug         = OpenMaya.MObject()
    inputCrvsCount          = 0
    inputCrvsDegrees        = OpenMaya.MIntArray()
    inputCrvsCVs            = []
    inputCrvsKnots          = []
    inputCrvsLocalIndices   = OpenMaya.MIntArray()
    inputCrvsDirty          = False

    outputCurvesPlug        = OpenMaya.MObject()
    outputCrvsPts           = []

    #projMethodsPlug         = OpenMaya.MObject()
    projMethods             = OpenMaya.MObject()
    #projMethodDirty         = False

    #spacePlug               = OpenMaya.MObject()
    space                    = 0    # = OpenMaya.MSpace.kLocal
    #spaceValDirty           = False

    # member functions
    def __init__( self ):
        OpenMayaMPx.MPxNode.__init__( self )

    def compute( self, plug, dataBlock ):
        if plug == lcProjCrvsNode.outputCurvesPlug:
            if ( self.inputSrfDirty ):
                self.inputSurface = dataBlock.inputValue( self.inputSurfacePlug ).asNurbsSurface()
                self.inputSrfDirty = False

            if self.inputCrvsDirty:
                self.getAllCVs( dataBlock )

            # del self.outputCrvsPts[:]
            # for i in range( 0, self.inputCrvsCount ):
            #     self.outputCrvsPts.append( OpenMaya.MPointArray() ) # May be inefficient? Could we create the point arrays during the initialization?

                # iCVsLen = self.inputCrvsPts[i].length()
                # self.outputCrvsPts[i].setLength( iCVsLen )
                # for j in range(0, iCVsLen):
                #     self.outputCrvsPts[i][j] = self.inputCrvsPts[i][j]
                #     self.outputCrvsPts[i][j].z = 0.0

            # # if self.projMethodDirty:
            # projMethod = dataBlock.inputValue( self.projMethods ).asShort()
            #      # self.projMethodDirty = False

            # # if self.spaceValDirty:
            # spaceVal = dataBlock.inputValue( self.space ).asShort()
            #     # self.spaceValDirty = False
            #
            # dataTypeStr = self.inputSurface.apiTypeStr()
            # # assert dataTypeStr == "kNurbsSurfaceData"
            # if "kNurbsSurfaceData" == dataTypeStr:
            #
            #     srfPath = OpenMaya.MDagPath()
            #     OpenMaya.MDagPath.getAPathTo( self.inputSurface, srfPath )
            #     srfFn = OpenMaya.MFnNurbsSurface()
            #     srfFn.setObject( srfPath )
            #
            #     for i in range( 0, self.inputCrvsCount ):
            #         iCVsLen = self.inputCrvsPts[i].length()
            #         for j in range( 0, self.iCVsLen ):
            #             pt = self.inputCrvsPts[i][j]
            #             u, v = 0.0
            #
            #             # Project Method (1) - closestPoint
            #             if 0 == projMethod:
            #                 u, v = srfFn.getParamAtPoint( pt, False, 0.0, spaceVal )


            dataBlock.setClean( plug )
            return

    def setDependentsDirty( self, plug, plugArray ):
        if plug == self.inputSurfacePlug:
            self.inputSrfDirty = True
            return

        if plug == self.inputCurvesPlug:
            self.inputCrvsDirty = True
            return

        if plug == self.projMethodsPlug:
            self.projMethodsDirty = True
            return

        if plug == self.spacePlug:
            self.inputCrvsDirty = True
            self.spaceValDirty = True
            return

        return

    def getAllCVs( self, dataBlock ):
        inputCrvsHdl = dataBlock.inputArrayValue( self.inputCurvesPlug )
        self.inputCrvsCount = inputCrvsHdl.elementCount()
        self.inputCrvsDegrees.setLength( self.inputCrvsCount )
        del self.inputCrvsCVs[:]
        del self.inputCrvsKnots[:]
        self.inputCrvsLocalIndices.setLength( self.inputCrvsCount )

        curSpace = OpenMaya.MSpace.kObject
        spaceValue = dataBlock.inputValue( self.space ).asShort()
        if 1 == spaceValue:
            curSpace = OpenMaya.MSpace.kWorld

        crvObjs = OpenMaya.MObjectArray()
        for i in range( 0, self.inputCrvsCount ):
            inputCrvHdl = inputCrvsHdl.inputValue()
            # self.inputCrvsLocalIndices[i] = inputCrvsHdl.elementLogicalIndex() # or should be elementIndex()?
            self.inputCrvsLocalIndices[i] = inputCrvsHdl.elementIndex()
            crvObj = inputCrvHdl.asNurbsCurve()
            geoTypeStr = crvObj.apiTypeStr()
            if "kNurbsCurveData" != geoTypeStr:
                raise Exception( "[lcProjectCurvesToSurface] Input Geometries are not NURBS curves; Its api Type: %s" % geoTypeStr)
            crvObjs.append( crvObj )

            crvPath = OpenMaya.MDagPath()
            OpenMaya.MDagPath.getAPathTo( crvObj, crvPath )
            crvFn = OpenMaya.MFnNurbsCurve()
            crvFn.setObject( crvPath )

            crvCVs = OpenMaya.MPointArray()
            crvKnots = OpenMaya.MDoubleArray()

            self.inputCrvsDegrees[i] = crvFn.degree()
            crvFn.getCVs( crvCVs, curSpace )
            crvFn.getKnots( crvKnots )

            self.inputCrvsCVs.append( crvCVs )
            self.inputCrvsKnots.append( crvKnots )

            inputCrvsHdl.next()

# creator
def nodeCreator():
    return OpenMayaMPx.asMPxPtr( lcProjCrvsNode() )

# initializer
def nodeInitializer():

    gAttr = OpenMaya.MFnGenericAttribute()
    eAttr = OpenMaya.MFnEnumAttribute()

    # input
    lcProjCrvsNode.inputSurfacePlug = gAttr.create("inputSurface", "isrf")
    gAttr.addDataAccept( OpenMaya.MFnData.kNurbsSurface )
    gAttr.setStorable( True )

    lcProjCrvsNode.inputCurvesPlug = gAttr.create("inputCurves", "icrvs")
    gAttr.addDataAccept( OpenMaya.MFnData.kNurbsCurve )
    gAttr.setStorable( True )
    gAttr.setArray( True )

    # output
    lcProjCrvsNode.outputCurvesPlug = gAttr.create("outputCurves", "ocrvs")
    gAttr.addDataAccept( OpenMaya.MFnData.kNurbsCurve )
    gAttr.setStorable( True )
    gAttr.setArray( True )

    # other attributes
    lcProjCrvsNode.projMethods = eAttr.create("projectMethod", "projMthd", 0)
    eAttr.addField( "closestPoint", 0 )
    eAttr.addField( "projectRay", 1 )
    eAttr.setStorable( True )
    eAttr.setKeyable( False )
    eAttr.setChannelBox( True )

    lcProjCrvsNode.space = eAttr.create("space", "spc", 0)
    eAttr.addField( "local", 0 )
    eAttr.addField( "world", 1 )
    eAttr.setStorable( True )
    eAttr.setKeyable( False )
    eAttr.setChannelBox( True )

    # Add attributes
    lcProjCrvsNode.addAttribute(lcProjCrvsNode.inputSurfacePlug)
    lcProjCrvsNode.addAttribute(lcProjCrvsNode.inputCurvesPlug)
    lcProjCrvsNode.addAttribute(lcProjCrvsNode.outputCurvesPlug)
    lcProjCrvsNode.attributeAffects(lcProjCrvsNode.inputSurfacePlug, lcProjCrvsNode.outputCurvesPlug)
    lcProjCrvsNode.attributeAffects(lcProjCrvsNode.inputCurvesPlug, lcProjCrvsNode.outputCurvesPlug)

    lcProjCrvsNode.addAttribute(lcProjCrvsNode.projMethods)
    lcProjCrvsNode.attributeAffects(lcProjCrvsNode.projMethods, lcProjCrvsNode.outputCurvesPlug)
    lcProjCrvsNode.addAttribute(lcProjCrvsNode.space)
    lcProjCrvsNode.attributeAffects(lcProjCrvsNode.space, lcProjCrvsNode.outputCurvesPlug)

# Initialize the script plug-in.
def initializePlugin( mobject ):
    mplugin = OpenMayaMPx.MFnPlugin( mobject )
    try:
        mplugin.registerNode( kPluginNodeTypeName, projCrvNodeId, nodeCreator, nodeInitializer )
    except:
        sys.stderr.write( "Failed to register node: %s" % kPluginNodeTypeName )
        raise

# Uninitialize the script plug-in.
def uninitializePlugin( mobject ):
    mplugin = OpenMayaMPx.MFnPlugin( mobject )
    try:
        mplugin.deregisterNode( projCrvNodeId )
    except:
        sys.stderr.write( "Failed to deregister node: %s" % kPluginNodeTypeName )
        raise