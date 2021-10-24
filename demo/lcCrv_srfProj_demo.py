# ----------------------------------------------------------------------------------------------------------------------
import maya.cmds as cmds

lca_ranixFacial_dir = "D:/liaosheng/Maya Projects"
if lca_ranixFacial_dir not in sys.path:
    sys.path.append(lca_ranixFacial_dir)

import LCA_Ranix_FacialRig; reload( LCA_Ranix_FacialRig )
from LCA_Ranix_FacialRig.rigLib.utils import lcTransform;  reload( lcTransform )
from LCA_Ranix_FacialRig.rigLib.utils import lcString;     reload( lcString )
from LCA_Ranix_FacialRig.rigLib.utils import lcSurface;    reload( lcSurface )
from LCA_Ranix_FacialRig.rigLib.dependencyNodes import lcCrv_ProjectToUVPlane; reload( lcCrv_ProjectToUVPlane )

# ----------------------------------------------------------------------------------------------------------------------
# Create a new scene.
cmds.file( new=True, force=True )
# Load the curve projection scirpted plug-in.
lcProjCrvPlugin = lcString.GetSPluginFilePath( lcCrv_ProjectToUVPlane )
if not cmds.pluginInfo( lcProjCrvPlugin, query=True, loaded=True ):
    cmds.loadPlugin( lcProjCrvPlugin )

# Create the original NURBS curve.
crv_ori = cmds.curve( degree=3, point=[
    (-7.0, -1.0,  0.0), (-6.0,  3.0,  0.0), (-5.0, -4.0,  0.0), (-4.0,  4.0,  0.0), (-3.0, -3.0,  0.0),
    (-2.0,  3.0,  0.0), (-1.0, -3.0,  0.0), ( 0.0,  3.0 , 0.0), ( 1.0, -3.0,  0.0), ( 2.0,  3.0,  0.0),
    ( 3.0, -3.0,  0.0), ( 4.0,  4.0,  0.0), ( 5.0, -4.0,  0.0), ( 6.0,  3.0,  0.0), ( 7.0, -1.0,  0.0)] )
crv_ori = cmds.rename( crv_ori, "crv_ori" )
cmds.displaySmoothness( crv_ori, pointsWire=16 )
cmds.setAttr( crv_ori + ".overrideEnabled", True )
cmds.setAttr( crv_ori + ".overrideColor", 16 )   # 16 == white

# Create a NURBS plane as the first projection target.
srf_planeProjTarget = cmds.nurbsPlane( name="srf_planeProjTarget", width=13.5, lengthRatio=0.4, patchesU=10, patchesV=5 )[0]
cmds.xform( srf_planeProjTarget, translation=[0.0, 16.5, 2.5], rotation=[-90.0, -75.0, 90.0] )
cmds.select( srf_planeProjTarget )
srf_planeProj_bendDeform = cmds.nonLinear( name="srf_planeProj_bendDeform", type="bend", curvature="-70.0", autoParent=True )
cmds.xform( srf_planeProj_bendDeform, rotation=[90.0, 0.0, 0.0] )
cmds.delete( srf_planeProjTarget, constructionHistory=True )
cmds.makeIdentity( srf_planeProjTarget, apply=True )
cmds.setAttr( srf_planeProjTarget + ".overrideEnabled", True )
cmds.setAttr( srf_planeProjTarget + ".overrideDisplayType", 1 ) # 1 == template

# Create a NURBS sphere as the second projection target.
srf_sphereProjTarget = cmds.sphere( radius=7, spans=8 )[0]    # [u'nurbsSphere1', u'makeNurbSphere1']
srf_sphereProjTarget = cmds.rename( srf_sphereProjTarget, "srf_sphereProjTarget" )
cmds.xform( srf_sphereProjTarget, translation=[0.0, 9.0, 0.0], rotation=[0.0, 90.0, 157.5] )
cmds.makeIdentity( srf_sphereProjTarget, apply=True )
cmds.setAttr( srf_sphereProjTarget + ".overrideEnabled", True )
cmds.setAttr( srf_sphereProjTarget + ".overrideDisplayType", 1 ) # 1 == template

# Project the original curve onto the NURBS plane.
crv_uvProj_toPlane = cmds.curve(degree=3, point=[(-1.0, 0.0, 0.0), (1.0, 0.0, 0.0)])
crv_uvProj_toPlane = cmds.rename(crv_uvProj_toPlane, "crv_uvProj_toPlane")
cmds.setAttr( crv_uvProj_toPlane + ".overrideEnabled", True )
cmds.setAttr( crv_uvProj_toPlane + ".overrideDisplayType", 1 )
cmds.hide( crv_uvProj_toPlane )

crv_planeSrfProj = cmds.curveOnSurface( srf_planeProjTarget, degree=3, uv=[(0.0, 0.0), (1.0, 1.0)] )
crv_planeSrfProj = cmds.rename( crv_planeSrfProj, "crv_planeSrfProj" )
cmds.setAttr( crv_planeSrfProj + ".overrideEnabled", True )
cmds.setAttr( crv_planeSrfProj + ".overrideColor", 14 )  # 14 == light green

cmds.connectAttr( crv_uvProj_toPlane + ".local", crv_planeSrfProj + ".create" )

assert( cmds.pluginInfo(lcString.GetSPluginName(lcProjCrvPlugin), query=True, loaded=True) )
projCrvNode_toPlane = cmds.createNode( lcCrv_ProjectToUVPlane.lcCrv_ProjectToUVPlaneNode.pluginNodeTypeName,
                                      name="lcCrv_ProjectToUVPlane_toPlane" )
cmds.setAttr( projCrvNode_toPlane + ".uBoundary", -8.0, 8.0 )
cmds.setAttr( projCrvNode_toPlane + ".vBoundary", -3.0, 3.0 )

cmds.connectAttr( crv_ori + ".worldSpace[0]", projCrvNode_toPlane + ".inputCurves[0]" )
cmds.connectAttr( projCrvNode_toPlane + ".outputCurves[0]", crv_uvProj_toPlane + ".create" )

# Project the original curve onto the NURBS sphere.
crv_uvProj_toSphere = cmds.curve( degree=3, point=[(-1.0, 0.0, 0.0), (1.0, 0.0, 0.0)] )
crv_uvProj_toSphere = cmds.rename( crv_uvProj_toSphere, "crv_uvProj_toSphere" )
cmds.setAttr( crv_uvProj_toSphere + ".overrideEnabled", True )
cmds.setAttr( crv_uvProj_toSphere + ".overrideDisplayType", 1 )
cmds.hide( crv_uvProj_toSphere )

crv_sphereSrfProj = cmds.curveOnSurface( srf_sphereProjTarget, degree=3, uv=[(0.0, 0.0), (1.0, 1.0)] )
crv_sphereSrfProj = cmds.rename( crv_sphereSrfProj, "crv_sphereSrfProj" )
cmds.xform( crv_sphereSrfProj, translation=[-0.5, 0.0, 0.0] )
cmds.setAttr( crv_sphereSrfProj + ".overrideEnabled", True )
cmds.setAttr( crv_sphereSrfProj + ".overrideColor", 14 )

cmds.connectAttr( crv_uvProj_toSphere + ".local", crv_sphereSrfProj + ".create" )

projCrvNode_toSphere = cmds.createNode( lcCrv_ProjectToUVPlane.lcCrv_ProjectToUVPlaneNode.pluginNodeTypeName,
                                       name="lcCrv_ProjectToUVPlane_toSphere" )
cmds.setAttr( projCrvNode_toSphere + ".uBoundary", -1.5, 1.5 )
cmds.setAttr( projCrvNode_toSphere + ".vBoundary", -1.0, 1.0 )

cmds.connectAttr( crv_ori + ".worldSpace[0]", projCrvNode_toSphere + ".inputCurves[0]" )
cmds.connectAttr( projCrvNode_toSphere + ".outputCurves[0]", crv_uvProj_toSphere + ".create" )

# Finish demonstrating the functionality of the projection custom node.
cmds.select( clear=True )

