# ----------------------------------------------------------------------------------------------------------------------
import math, sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import random

# ----------------------------------------------------------------------------------------------------------------------
kPluginNodeTypeName = "spRandomNode"
randomNodeId = OpenMaya.MTypeId( 0x87300 )

class randomNode( OpenMayaMPx.MPxNode ):
    GIRDI = OpenMaya.MObject()
    CIKTI = OpenMaya.MObject()

    def __init__( self ):
        OpenMayaMPx.MPxNode.__init__( self )

    def compute( self, plug, dataBlock ):
        if ( plug == randomNode.CIKTI ):
            dataHandle = dataBlock.inputValue( randomNode.GIRDI )
            inputFloat = dataHandle.asFloat()
            result = random.uniform( -1, -1 ) + inputFloat
            outputHandle = dataBlock.outputValue( randomNode.CIKTI )
            outputHandle.setFloat( result )
            dataBlock.setClean( plug )

        return OpenMaya.kUnknownParameter

def nodeCreator():
    return OpenMayaMPx.asMPxPtr( randomNode() )

def nodeInitializer():
    nAttr = OpenMaya.MFnNumericAttribute()
    randomNode.GIRDI = nAttr.create( "Girdi", "in", OpenMaya.MFnNumericData.kFloat, 0.0 )
    nAttr.setStorable( 1 )
    nAttr = OpenMaya.MFnNumericAttribute()
    randomNode.CIKTI = nAttr.create( "Cikti", "out", OpenMaya.MFnNumericData.kFloat, 0.0 )
    nAttr.setStorable( 1 )
    nAttr.setWritable( 1 )
    randomNode.addAttribute( randomNode.GIRDI )
    randomNode.addAttribute( randomNode.CIKTI )
    randomNode.attributeAffects( randomNode.GIRDI, randomNode.CIKTI )

def initializePlugin( mobject ):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode( kPluginNodeTypeName, randomNodeId, nodeCreator, nodeInitializer )
    except:
        sys.stderr.write( "Failed to register node: %s" % kPluginNodeTypeName )
        raise

def uninitializePlugin( mobject ):
    mplugin = OpenMayaMPx.MFnPlugin( mobject )
    try:
        mplugin.deregisterNode( randomNodeId )
    except:
        sys.stderr.write("Failed to deregister node: %s" % kPluginNodeTypeName )
        raise