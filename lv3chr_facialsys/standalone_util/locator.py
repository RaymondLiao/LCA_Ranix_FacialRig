#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# File Name: standalone_util.locator.py
# Author: Sheng (Raymond) Liao
# Date: January 2022
#

"""
A module to generate and manipulate locators
"""

import string

import maya.cmds as cmds
import maya.api.OpenMaya as OpenMaya2

def get_type_and_id(sel_list, single_indexed=True):
    '''
    :param sel_list: an instance of MSelectionList class
    :param single_indexed: if the component ID is a single integer
    :return: selected MObjects' MFN function set type ID (integer) and component ID list
    '''

    compo_dag_path, component = sel_list.getComponent(0)
    compo_fn_type_id = component.apiType()
    id_compo_fn = None
    if single_indexed:
        id_compo_fn = OpenMaya2.MFnSingleIndexedComponent(component)
    else:
        id_compo_fn = OpenMaya2.MFnDoubleIndexedComponent(component)
    compo_id_list = id_compo_fn.getElements()

    return compo_fn_type_id, compo_id_list

def create_locator(name_prefix, id, local_scale, color_id, modifier):
    '''
    :param name_prefix: the prefix of the locator, e.g. fm_eyelidMask_LU
    :param id: the identifier of the locator, e.g. A1
    :param modifier: instance of the MDagModifier class
    :return: a MObjectHandle to the locator created
    '''

    assert isinstance(local_scale, list)
    assert len(local_scale) == 3

    loc_obj = modifier.createNode('locator')
    loc_handle = OpenMaya2.MObjectHandle(loc_obj)
    loc_name = '{}_{}_loc'.format(name_prefix, id)
    modifier.renameNode(loc_obj, loc_name)
    modifier.doIt()

    dag_path = OpenMaya2.MDagPath()
    loc_dag_path = dag_path.getAPathTo(loc_obj)
    loc_shape_dag_path = loc_dag_path.extendToShape()
    loc_shape_obj = loc_shape_dag_path.node()
    modifier.renameNode(loc_shape_obj, loc_name+'Shape')
    modifier.doIt()

    loc_shape_fn = OpenMaya2.MFnDependencyNode(loc_shape_obj)
    loc_shape_local_sclx = loc_shape_fn.findPlug('localScaleX', False)
    loc_shape_local_scly = loc_shape_fn.findPlug('localScaleY', False)
    loc_shape_local_sclz = loc_shape_fn.findPlug('localScaleZ', False)
    loc_shape_local_sclx.setFloat(local_scale[0])
    loc_shape_local_scly.setFloat(local_scale[1])
    loc_shape_local_sclz.setFloat(local_scale[2])

    cmds.setAttr(loc_name+'Shape.overrideEnabled', True)
    cmds.setAttr(loc_name+'Shape.overrideColor', color_id)

    return loc_handle

def create_locator_at_vertex(sel_list, compo_fn_type_id, vtx_id_list, loc_scale, modifier):
    '''
    Create locators each on a selected mesh's vertex or a NURBS object's control vertex
    :param sel_list: an instance of the MSelectionList class
    :param compo_fn_type: the selected components' MFn function set type
    :param vtx_id_list: the indices of the selected CVs
    :param modifier: an instance of the MDagModifier class
    :return: None
    '''

    vtx_pos = [0, 0, 0]
    loc_id = ''

    loc_trans = [0, 0, 0]
    loc_handle = None

    for vtx_id in vtx_id_list:

        if OpenMaya2.MFn.kMeshVertComponent == compo_fn_type_id:
            # Get vertex's position
            mesh_dag_path = sel_list.getDagPath(0)
            mesh_fn = OpenMaya2.MFnMesh(mesh_dag_path)
            vtx_pt = mesh_fn.getPoint(vtx_id, OpenMaya2.MSpace.kObject)

            vtx_pos = vtx_pt
            loc_id = str(vtx_id + 1)

        elif OpenMaya2.MFn.kSurfaceCVComponent == compo_fn_type_id:
            # Get control vertex's position
            nbs_srf_dag_path = sel_list.getDagPath(0)
            nbs_srf_fn = OpenMaya2.MFnNurbsSurface(nbs_srf_dag_path)
            cv_pos = nbs_srf_fn.cvPosition(vtx_id[0], vtx_id[1], OpenMaya2.MSpace.kObject)

            # Compose the locator's ID
            loc_id_row_list = list(string.ascii_uppercase)
            loc_id_row = loc_id_row_list[vtx_id[0]]
            loc_id_col = str(vtx_id[1] + 1)

            vtx_pos = cv_pos
            loc_id = loc_id_row + loc_id_col

        elif OpenMaya2.MFn.kCurveCVComponent == compo_fn_type_id:
            # Get control vertex's position
            nbs_crv_dag_path = sel_list.getDagPath(0)
            nbs_crv_fn = OpenMaya2.MFnNurbsCurve(nbs_crv_dag_path)
            cv_pos = nbs_crv_fn.cvPosition(vtx_id, OpenMaya2.MSpace.kObject)

            vtx_pos = cv_pos
            loc_id = str(vtx_id + 1)

        geo_node = sel_list.getDependNode(0)
        geo_node_fn = OpenMaya2.MFnDependencyNode(geo_node)

        geo_wmat_plug_arr = geo_node_fn.findPlug('worldMatrix', False)
        geo_wmat_plug = geo_wmat_plug_arr.elementByLogicalIndex(0)
        geo_wmat_obj = geo_wmat_plug.asMObject()

        geo_wmat_data_fn = OpenMaya2.MFnMatrixData(geo_wmat_obj)
        geo_wmat = geo_wmat_data_fn.matrix()

        # Construct the transformation matrix for the locator
        loc_mat_data = [
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            vtx_pos.x, vtx_pos.y, vtx_pos.z, vtx_pos.w
        ]

        loc_mat = OpenMaya2.MMatrix(loc_mat_data) * geo_wmat
        loc_trans_mat = OpenMaya2.MTransformationMatrix(loc_mat)
        loc_trans = loc_trans_mat.translation(OpenMaya2.MSpace.kWorld)

        loc_handle = create_locator('fm_mask', loc_id, loc_scale, 1, modifier)

        if loc_handle.isValid():
            loc_node = loc_handle.object()
            loc_node_fn = OpenMaya2.MFnDependencyNode(loc_node)

            loc_transx_plug = loc_node_fn.findPlug('translateX', False)
            loc_transy_plug = loc_node_fn.findPlug('translateY', False)
            loc_transz_plug = loc_node_fn.findPlug('translateZ', False)
            loc_transx_plug.setFloat(loc_trans.x)
            loc_transy_plug.setFloat(loc_trans.y)
            loc_transz_plug.setFloat(loc_trans.z)

# Test codes for creating locators at mesh's vertices
sel_list = OpenMaya2.MGlobal.getActiveSelectionList()
compo_fn_type_id, compo_id_list = get_type_and_id(sel_list, single_indexed=True)
modifier = OpenMaya2.MDagModifier()

if compo_fn_type_id == OpenMaya2.MFn.kMeshVertComponent:
    create_locator_at_vertex(sel_list, compo_fn_type_id, compo_id_list, [0.1, 0.1, 0.1], modifier)
    print("Done! Vertex locator/s created and placed!")
else:
    print("Please select a vertex")

# Test codes for creating locators at NURBS surface's CVs
sel_list = OpenMaya2.MGlobal.getActiveSelectionList()
compo_fn_type_id, compo_id_list = get_type_and_id(sel_list, single_indexed=False)
modifier = OpenMaya2.MDagModifier()

if compo_fn_type_id == OpenMaya2.MFn.kSurfaceCVComponent:
    create_locator_at_vertex(sel_list, compo_fn_type_id, compo_id_list, [0.1, 0.1, 0.1], modifier)
    print("Done! CV locator/s created and placed!")
else:
    print("Please select a control vertex")

# Test codes for creating locators at NURBS curve's CVs
sel_list = OpenMaya2.MGlobal.getActiveSelectionList()
compo_fn_type_id, compo_id_list = get_type_and_id(sel_list, single_indexed=True)
modifier = OpenMaya2.MDagModifier()

if compo_fn_type_id == OpenMaya2.MFn.kCurveCVComponent:
    create_locator_at_vertex(sel_list, compo_fn_type_id, compo_id_list, [0.1, 0.1, 0.1], modifier)
    print("Done! CV locator/s created and placed!")
else:
    print("Please select a control vertex")

# ----------------------------------------------------------------------------------------------------------------------
def create_joint_at_locator():
    loc_grp = cmds.ls(sl=True)[0]
    loc_list = cmds.listRelatives(loc_grp, children=True, fullPath=True)
    for loc_trans in loc_list:
        loc_shape = cmds.listRelatives(loc_trans, shapes=True, fullPath=True)
        assert 'locator' == cmds.objectType(loc_shape)

        loc_name = loc_trans.split('|')[-1]
        bind_jnt = cmds.joint(name=loc_name.replace('loc', 'bind'), radius=0.5)

        cmds.setAttr(bind_jnt + '.overrideEnabled', True)
        cmds.setAttr(bind_jnt + '.overrideColor', 3)
        cmds.parent(bind_jnt, loc_trans)
        cmds.xform(bind_jnt, translation=[0, 0, 0])

def connect_locators():
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