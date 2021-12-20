"""
A module to connect the locators on the control curve to the locators on the projection surface
"""

import maya.cmds as cmds

prefix = 'fm'
zone = 'mouth'
crv_loc_prefix = 'Project'
srf_loc_prefix = 'Mask'

UD_dir_list = ['U', 'D']
LR_dir_list = ['R', 'M', 'L']

alphabet_idx = 'B'
idx_count = 4

UD_dir = 'U'
LR_dir = 'L'

control_crv = prefix + '_' + zone + crv_loc_prefix + \
              '_M' + UD_dir + '_' + alphabet_idx + '_curveShape'
assert cmds.objExists(control_crv)
trans_plane = 'facial_mouthCheekProjectPlane_UDLR_nbs_V2'
proj_srf = 'fm_mouthCheekMask_UDLR_nbs_V2'

loc_on_crv_list = []
# loc_on_srf_list = []

for LR_dir in LR_dir_list:
    for idx in range(idx_count):
        idx = idx + 1
        if 'R' == LR_dir:
            idx = idx_count - idx + 1
        if 'M' == LR_dir and idx > 1:
            continue

        loc_on_crv = prefix + '_' + zone + crv_loc_prefix + \
                     '_' + LR_dir + UD_dir + '_' + alphabet_idx + str(idx) + '_loc'
        cmds.warning(loc_on_crv)
        assert cmds.objExists(loc_on_crv)
        loc_on_crv_list.append(loc_on_crv)

        # loc_on_srf = loc_on_crv.replace(crv_loc_prefix, srf_loc_prefix)
        # assert cmds.objExists(loc_on_srf)
        # loc_on_srf_list.append(loc_on_srf)

loc_param = -1
for loc_on_crv in loc_on_crv_list:
    loc_on_srf = loc_on_crv.replace(crv_loc_prefix, srf_loc_prefix)
    if not cmds.objExists(loc_on_srf):
        cmds.warning('locator on the projection surface "{}" does not exist.'.format(loc_on_srf))
        continue

    loc_param += 1
    pt_on_crv_info_node = cmds.createNode('pointOnCurveInfo', name=loc_on_crv + '_ptOnCrv')
    cmds.setAttr(pt_on_crv_info_node + '.parameter', loc_param)
    cmds.connectAttr(control_crv + '.worldSpace[0]', pt_on_crv_info_node + '.inputCurve')
    cmds.connectAttr(pt_on_crv_info_node + '.position', loc_on_crv + '.translate')

    loc_on_crv_shape = loc_on_crv + 'Shape'
    assert cmds.objExists(loc_on_crv_shape)

    cls_pt_on_transplane_node = cmds.createNode('closestPointOnSurface')
    cls_pt_on_transplane_node = cmds.rename(cls_pt_on_transplane_node, loc_on_crv + '_clsPtOnSrf')

    cmds.connectAttr(trans_plane + '.worldSpace[0]',
                     cls_pt_on_transplane_node + '.inputSurface')
    cmds.connectAttr(loc_on_crv_shape + '.worldPosition[0]',
                     cls_pt_on_transplane_node + '.inPosition')


    pt_on_projsrf_node = cmds.createNode('pointOnSurfaceInfo', name=loc_on_srf+'_ptOnSrf')
    cmds.connectAttr(cls_pt_on_transplane_node + '.parameterU', pt_on_projsrf_node + '.parameterU')
    cmds.connectAttr(cls_pt_on_transplane_node + '.parameterV', pt_on_projsrf_node + '.parameterV')
    cmds.connectAttr(proj_srf + '.worldSpace[0]', pt_on_projsrf_node + '.inputSurface')
    cmds.connectAttr(pt_on_projsrf_node + '.position', loc_on_srf + '.translate')