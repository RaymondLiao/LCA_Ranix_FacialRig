import maya.cmds as cmds
import sys

lca_ranixFacial_dir = "D:/Maya Projects"
if lca_ranixFacial_dir not in sys.path:
    sys.path.append(lca_ranixFacial_dir)

for path in sys.path:
    print path

import LCA_Ranix_FacialRig; reload( LCA_Ranix_FacialRig )

from LCA_Ranix_FacialRig.rigLib.utils import lcTransform; reload( lcTransform )
from LCA_Ranix_FacialRig.rigLib.utils import lcStrings;reload( lcStrings )

from LCA_Ranix_FacialRig.rigLib.experiment import randomNodeTEST; reload( randomNodeTEST )
from LCA_Ranix_FacialRig.rigLib.experiment import sineNodeTEST; reload( sineNodeTEST )

# ======================================================================================
lcTransform.ParentTo( "nurbsCircle1", "nurbsCircleGroup1" )
lcTransform.ParentTo( "nurbsCircleGroup1", "nurbsPlane1" )

cmds.projectCurve( "nurbsCircle1", "nurbsPlane1" )

# --------------------------------------------------------------------------------------
# spRandomNode
randomNodePlugin = cmds.loadPlugin( lcStrings.GetSPluginFileName(randomNodeTEST) )[0]
cmds.unloadPlugin( randomNodePlugin )
sel = cmds.ls( sl=True )
node = cmds.createNode( "spRandomNode", n="spRandom_TEST" )
cmds.connectAttr( node + ".Cikti", sel[0] + ".ty" )
cmds.connectAttr( sel[1] + ".tx", node + ".Girdi" )
cmds.connectAttr( sel[1] + ".ty", node + ".Cikti" )

# --------------------------------------------------------------------------------------
# spSineNode
sineNodePlugin = cmds.loadPlugin( lcStrings.GetSPluginFileName(sineNodeTEST) )[0]
cmds.unloadPlugin( sineNodePlugin )
sel = cmds.ls( sl=True )
node = cmds.createNode( "spSpineNode", n="spSpine_TEST" )
cmds.connectAttr( sel[0] + ".ty", node + ".input"  )
cmds.connectAttr( node + ".output", sel[1] + ".ty" )