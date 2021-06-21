import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import sys

lca_ranixFacial_dir = "D:/Maya Projects"
if lca_ranixFacial_dir not in sys.path:
    sys.path.append(lca_ranixFacial_dir)

for path in sys.path:
    print path

import LCA_Ranix_FacialRig; reload( LCA_Ranix_FacialRig )

from LCA_Ranix_FacialRig.rigLib.utils import lcTransform;  reload( lcTransform )
from LCA_Ranix_FacialRig.rigLib.utils import lcString;     reload( lcString )
from LCA_Ranix_FacialRig.rigLib.utils import lcSurface;    reload( lcSurface )

from LCA_Ranix_FacialRig.rigLib.experiment import randomNodeTEST;   reload( randomNodeTEST )
from LCA_Ranix_FacialRig.rigLib.experiment import sineNodeTEST;     reload( sineNodeTEST )
from LCA_Ranix_FacialRig.rigLib.experiment import helixCmdTEST;     reload( helixCmdTEST )

from LCA_Ranix_FacialRig.rigLib.dependencyNodes import lcProjectCurvesToSurface; reload( lcProjectCurvesToSurface )

# ======================================================================================
lcTransform.ParentTo( "nurbsCircle1", "nurbsCircleGroup1" )
lcTransform.ParentTo( "nurbsCircleGroup1", "nurbsPlane1" )

cmds.projectCurve( "nurbsCircle1", "nurbsPlane1" )

# --------------------------------------------------------------------------------------
# spRandomNode
randomNodePlugin = cmds.loadPlugin( lcString.GetSPluginFileName(randomNodeTEST) )[0]
cmds.unloadPlugin( randomNodePlugin )
sel = cmds.ls( sl=True )
node = cmds.createNode( "spRandomNode", n="spRandom_TEST" )
cmds.connectAttr( node + ".Cikti", sel[0] + ".ty" )
cmds.connectAttr( sel[1] + ".tx", node + ".Girdi" )
cmds.connectAttr( sel[1] + ".ty", node + ".Cikti" )

# --------------------------------------------------------------------------------------
# spSineNode
sineNodePlugin = cmds.loadPlugin( lcString.GetSPluginFileName(sineNodeTEST) )[0]
cmds.unloadPlugin( sineNodePlugin )
sel = cmds.ls( sl=True )
node = cmds.createNode( "spSpineNode", n="spSpine_TEST" )
cmds.connectAttr( sel[0] + ".ty", node + ".input"  )
cmds.connectAttr( node + ".output", sel[1] + ".ty" )

# --------------------------------------------------------------------------------------
# spHelixCommand
helixCmdPlugin = cmds.loadPlugin( lcString.GetSPluginFileName(helixCmdTEST) )[0]
cmds.unloadPlugin( helixCmdPlugin )
OpenMaya.MGlobal.executeCommand( "spHelix -pitch 1 -radius 2" )

# ======================================================================================
# lcProjCrvsNode
lcProjCrvPlugin = cmds.loadPlugin( lcString.GetSPluginFileName(lcProjectCurvesToSurface) )[0]
cmds.unloadPlugin( lcProjCrvPlugin )
projCrvsNode = cmds.createNode( "lcProjCurvesToSurface", n="lcProjCrvs_TEST" )
del projCrvsNode
cmds.connectAttr( "dataProjSrf.worldSpace[0]", projCrvsNode + ".inputSurface" )
lcTransform.TransformCurve( "nurbsCircle_original", projCrvsNode, "nurbsCircle_projed" )

# ======================================================================================
# DAG relevant tests
selection = OpenMaya.MSelectionList()
OpenMaya.MGlobal.getSelectionListByName( "nurbsCircle_originalShape", selection )

crvObj = OpenMaya.MObject()
selection.getDependNode( 0, crvObj )

crvPath = OpenMaya.MDagPath()
selection.getDagPath( 0, crvPath )

crvFn = OpenMaya.MFnNurbsCurve()
crvFn.setObject( crvPath )
crvCVs = OpenMaya.MPointArray()
crvKnots = OpenMaya.MDoubleArray()
crvFn.getCVs( crvCVs, OpenMaya.MSpace.kWorld )
crvFn.getKnots( crvKnots )

print "curve's api Type: %s" % crvObj.apiTypeStr()
for i in range(0, crvCVs.length()):
    print "curve point: (%s, %s, %s)" % (crvCVs[i][0], crvCVs[i][1], crvCVs[i][2])
for i in range(0, crvKnots.length()):
    print "curve knot: %s" % crvKnots[i]
print "curve degree: %s" % crvFn.degree()
