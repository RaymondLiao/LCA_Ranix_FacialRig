#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# Author: Sheng (Raymond) Liao
# Date: August 2021
#

'''
custom node to map curves' CVs coordinates to a plane within U & V boundaries.
'''

import maya.cmds as cmds
import math, sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

from LCA_Ranix_FacialRig.rigLib.utils import lcOpenMaya; reload( lcOpenMaya )

class lcCrv_ProjectToUVPlaneNode(OpenMayaMPx.MPxNode):
    # member variables
    pluginNodeTypeName = "lcCrv_ProjectToUVPlane"
    pluginNodeId = OpenMaya.MTypeId(0x1ca00000)

    attr_uStartBoundary = OpenMaya.MObject()
    attr_uEndBoundary = OpenMaya.MObject()
    attr_UBoundary = OpenMaya.MObject()
    attr_vStartBoundary = OpenMaya.MObject()
    attr_vEndBoundary = OpenMaya.MObject()
    attr_vBoundary = OpenMaya.MObject()

    attr_reverseU = OpenMaya.MObject()
    attr_reverseV = OpenMaya.MObject()
    attr_planeDirection = OpenMaya.MObject()

    attr_inputCurves = OpenMaya.MObject()
    attr_outputCurves = OpenMaya.MObject()

    # member functions
    def __init__( self ):
        OpenMayaMPx.MPxNode.__init__( self )

    def compute( self, plug, dataBlock ):
        print "Called lcCrv_ProjectToUVPlaneNode.compute(). The plug is %s" % plug.name()
        if plug != lcCrv_ProjectToUVPlaneNode.attr_outputCurves and plug.array() != lcCrv_ProjectToUVPlaneNode.attr_outputCurves:
            return

        # Retrieve the attributes' values from the dataBlock.
        reverseU = dataBlock.inputValue( lcCrv_ProjectToUVPlaneNode.attr_reverseU ).asBool()
        reverseV = dataBlock.inputValue( lcCrv_ProjectToUVPlaneNode.attr_reverseV ).asBool()
        uStartBoundary = dataBlock.inputValue( lcCrv_ProjectToUVPlaneNode.attr_uStartBoundary ).asDouble()
        uEndBoundary = dataBlock.inputValue( lcCrv_ProjectToUVPlaneNode.attr_uEndBoundary ).asDouble()
        vStartBoundary = dataBlock.inputValue( lcCrv_ProjectToUVPlaneNode.attr_vStartBoundary ).asDouble()
        vEndBoundary = dataBlock.inputValue( lcCrv_ProjectToUVPlaneNode.attr_vEndBoundary ).asDouble()
        planeDirection = dataBlock.inputValue( lcCrv_ProjectToUVPlaneNode.attr_planeDirection ).asShort()

        inputArrayPlug = OpenMaya.MPlug( self.thisMObject(), lcCrv_ProjectToUVPlaneNode.attr_inputCurves )
        outputArrayPlug = OpenMaya.MPlug( self.thisMObject(), lcCrv_ProjectToUVPlaneNode.attr_outputCurves )
        relativeInputPlugs = []
        if plug.isElement():
            inputPlug = inputArrayPlug.elementByLogicalIndex( plug.logicalIndex() )
            relativeInputPlugs.append( inputPlug )
        else:
            i, n = inputArrayPlug.numElements()
            for i in range( 0, n ):
                inputPlug = inputArrayPlug.elementByPhysicalIndex( i )
                relativeInputPlugs.append( inputPlug )

        uLength = abs( uEndBoundary - uStartBoundary )
        vLength = abs( vEndBoundary - vStartBoundary )
        uDirection = 0; vDirection = 0
        if 0 == planeDirection: # xy
            uDirection = 0
            vDirection = 1
        else:                   # yz
            uDirection = 2
            vDirection = 1

        for i in range( 0, len(relativeInputPlugs) ):
            inputPlug = relativeInputPlugs[i]
            outputPlug = outputArrayPlug.elementByLogicalIndex( inputPlug.logicalIndex() )

            inputData = inputPlug.asMDataHandle()
            outputData = dataBlock.outputValue( outputPlug )

            crvObj = inputData.asNurbsCurve()
            inCvArray = OpenMaya.MPointArray()
            outCvArray = OpenMaya.MPointArray()

            crvFn = OpenMaya.MFnNurbsCurve( crvObj )
            cvNum = crvFn.numCVs()
            crvFn.getCVs( inCvArray )
            # outCvArray.setLength( cvNum )

            for j in range( 0, cvNum ):
                crvCV = inCvArray[j]

                uPos = crvCV[uDirection]    # "xy" == 0 --- x, "zy" == 2 --- z
                vPos = crvCV[vDirection]    # "xy" == 1 --- y, "zy" == 1 --- y

                uParam = ( uPos - uStartBoundary ) / uLength
                vParam = ( vPos - vStartBoundary ) / vLength
                if reverseU:
                    uParam *= -1
                if reverseV:
                    vParam *= -1

                uvPoint = OpenMaya.MPoint()
                uvPoint.x = uParam
                uvPoint.y = vParam
                uvPoint.z = 0

                # outCvArray[j] = uvPoint # Error: 'MPointArray' object does not support item assignment
                outCvArray.append( uvPoint )

            knots = OpenMaya.MDoubleArray()
            crvFn.getKnots( knots )
            degree = crvFn.degree()

            MFnCrvData = OpenMaya.MFnNurbsCurveData()
            outCurveData = MFnCrvData.create()
            mfnCrv = OpenMaya.MFnNurbsCurve( outCurveData )

            mfnCrv.create( outCvArray, knots, degree, OpenMaya.MFnNurbsCurve.kOpen, True, True, outCurveData )
            outputData.setMObject( outCurveData )

        dataBlock.setClean(plug)
        return

    def setDependentsDirty( self, plugBeingDirted, affectedPlugs ):
        # print "Called lcCrv_ProjectToUVPlaneNode.setDependentsDirty(). The plug is %s" % plugBeingDirted.name()
        if plugBeingDirted.attribute() != lcCrv_ProjectToUVPlaneNode.attr_inputCurves:
            return

        outArrayPlug = OpenMaya.MPlug( self.thisMObject(), lcCrv_ProjectToUVPlaneNode.attr_outputCurves )

        if plugBeingDirted.isElement():
            outElemPlug = outArrayPlug.elementByLogicalIndex( plugBeingDirted.logicalIndex() )
            affectedPlugs.append( outElemPlug )
            affectedPlugs.append( outArrayPlug )
        else:
            i, n = outArrayPlug.numElements()
            for i in range( 0, n ):
                outElemPlug = outArrayPlug.elementByPhysicalIndex( i )
                affectedPlugs.append( outElemPlug )
            affectedPlugs.append( outArrayPlug )

        return

# creator
def nodeCreator():
    return OpenMayaMPx.asMPxPtr(lcCrv_ProjectToUVPlaneNode())

# initializer
def nodeInitializer():
    print "Initializing custom node: %s" % lcCrv_ProjectToUVPlaneNode.pluginNodeTypeName

    nAttr = OpenMaya.MFnNumericAttribute()
    eAttr = OpenMaya.MFnEnumAttribute()
    gAttr = OpenMaya.MFnGenericAttribute()

    lcCrv_ProjectToUVPlaneNode.attr_uStartBoundary = nAttr.create( "uStartBoundary", "usb", OpenMaya.MFnNumericData.kDouble, -1.0 )
    lcOpenMaya.makeNodeInput( nAttr )
    lcCrv_ProjectToUVPlaneNode.attr_uEndBoundary = nAttr.create( "uEndBoundary", "ueb", OpenMaya.MFnNumericData.kDouble, 1.0 )
    lcOpenMaya.makeNodeInput( nAttr )
    lcCrv_ProjectToUVPlaneNode.attr_uBoundary = nAttr.create( "uBoundary", "ub",
                                                                lcCrv_ProjectToUVPlaneNode.attr_uStartBoundary,
                                                                lcCrv_ProjectToUVPlaneNode.attr_uEndBoundary )
    lcOpenMaya.makeNodeInput( nAttr )

    lcCrv_ProjectToUVPlaneNode.attr_vStartBoundary = nAttr.create( "vStartBoundary", "vsb", OpenMaya.MFnNumericData.kDouble, -1.0 )
    lcOpenMaya.makeNodeInput( nAttr )
    lcCrv_ProjectToUVPlaneNode.attr_vEndBoundary = nAttr.create( "vEndBoundary", "veb", OpenMaya.MFnNumericData.kDouble, 1.0 )
    lcOpenMaya.makeNodeInput( nAttr )
    lcCrv_ProjectToUVPlaneNode.attr_vBoundary = nAttr.create( "vBoundary", "vb",
                                                              lcCrv_ProjectToUVPlaneNode.attr_vStartBoundary,
                                                              lcCrv_ProjectToUVPlaneNode.attr_vEndBoundary )
    lcOpenMaya.makeNodeInput( nAttr )

    lcCrv_ProjectToUVPlaneNode.attr_reverseU = nAttr.create( "reverseU", "ru", OpenMaya.MFnNumericData.kBoolean, False )
    lcOpenMaya.makeNodeInput( nAttr )
    lcCrv_ProjectToUVPlaneNode.attr_reverseV = nAttr.create( "reverseV", "rv", OpenMaya.MFnNumericData.kBoolean, False )
    lcOpenMaya.makeNodeInput( nAttr )


    lcCrv_ProjectToUVPlaneNode.attr_planeDirection = eAttr.create( "planeDirection", "pld", 0 )
    eAttr.addField( "xy", 0 )
    eAttr.addField( "yz", 1 )
    lcOpenMaya.makeNodeInput( eAttr )

    lcCrv_ProjectToUVPlaneNode.attr_inputCurves = gAttr.create( "inputCurves", "icrvs" )
    gAttr.addDataAccept( OpenMaya.MFnData.kNurbsCurve )
    lcOpenMaya.makeNodeInput( gAttr )
    gAttr.setArray( True )
    gAttr.setHidden( False )

    lcCrv_ProjectToUVPlaneNode.attr_outputCurves = gAttr.create( "outputCurves", "ocrvs" )
    gAttr.addDataAccept( OpenMaya.MFnData.kNurbsCurve )
    lcOpenMaya.makeNodeOutput( gAttr )
    gAttr.setArray( True )
    gAttr.setHidden( False )

    lcCrv_ProjectToUVPlaneNode.addAttribute( lcCrv_ProjectToUVPlaneNode.attr_uBoundary )
    lcCrv_ProjectToUVPlaneNode.addAttribute( lcCrv_ProjectToUVPlaneNode.attr_vBoundary )
    lcCrv_ProjectToUVPlaneNode.addAttribute( lcCrv_ProjectToUVPlaneNode.attr_reverseU )
    lcCrv_ProjectToUVPlaneNode.addAttribute( lcCrv_ProjectToUVPlaneNode.attr_reverseV )
    lcCrv_ProjectToUVPlaneNode.addAttribute( lcCrv_ProjectToUVPlaneNode.attr_planeDirection )
    lcCrv_ProjectToUVPlaneNode.addAttribute( lcCrv_ProjectToUVPlaneNode.attr_inputCurves )
    lcCrv_ProjectToUVPlaneNode.addAttribute( lcCrv_ProjectToUVPlaneNode.attr_outputCurves )

    lcCrv_ProjectToUVPlaneNode.attributeAffects( lcCrv_ProjectToUVPlaneNode.attr_uBoundary, lcCrv_ProjectToUVPlaneNode.attr_outputCurves )
    lcCrv_ProjectToUVPlaneNode.attributeAffects( lcCrv_ProjectToUVPlaneNode.attr_vBoundary, lcCrv_ProjectToUVPlaneNode.attr_outputCurves )
    lcCrv_ProjectToUVPlaneNode.attributeAffects( lcCrv_ProjectToUVPlaneNode.attr_reverseU, lcCrv_ProjectToUVPlaneNode.attr_outputCurves )
    lcCrv_ProjectToUVPlaneNode.attributeAffects( lcCrv_ProjectToUVPlaneNode.attr_reverseV, lcCrv_ProjectToUVPlaneNode.attr_outputCurves )
    lcCrv_ProjectToUVPlaneNode.attributeAffects( lcCrv_ProjectToUVPlaneNode.attr_planeDirection, lcCrv_ProjectToUVPlaneNode.attr_outputCurves )

    return

# Initialize the script plug-in.
def initializePlugin( mobject ):
    mplugin = OpenMayaMPx.MFnPlugin( mobject )
    try:
        mplugin.registerNode( lcCrv_ProjectToUVPlaneNode.pluginNodeTypeName,
                              lcCrv_ProjectToUVPlaneNode.pluginNodeId,
                              nodeCreator, nodeInitializer )
    except:
        sys.stderr.write( "Failed to register node: %s" % lcCrv_ProjectToUVPlaneNode.pluginNodeTypeName )
        raise

# Uninitialize the script plug-in.
def uninitializePlugin( mobject ):
    mplugin = OpenMayaMPx.MFnPlugin( mobject )
    try:
        mplugin.deregisterNode( lcCrv_ProjectToUVPlaneNode.pluginNodeId )
    except:
        sys.stderr.write( "Failed to deregister node: %s" % lcCrv_ProjectToUVPlaneNode.pluginNodeTypeName )
        raise