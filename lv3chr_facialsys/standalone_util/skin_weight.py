import maya.cmds as cmds

jnt_list = cmds.ls(sl=True)[:-1]
nurbs_plane = cmds.ls(sl=True)[-1]

cmds.skinCluster(jnt_list, nurbs_plane, toSelectedBones=True, name=nurbs_plane+'_skinCluster')
for vtx_idx in range(8, -1):
    vtx_1 = '{}.vtx[0,{}]'.format(nurbs_plane, vtx_idx)
    vtx_2 = '{}.vtx[1,{}]'.format(nurbs_plane, vtx_idx)
    jnt = jnt_list[8-vtx_idx]
    cmds.skinPercent(nurbs_plane+'_skinCluster', vtx_1, transformValue=[(jnt, 1.0)], zeroRemainingInfluences=True)
    cmds.skinPercent(nurbs_plane+'_skinCluster', vtx_2, transformValue=[(jnt, 1.0)], zeroRemainingInfluences=True)