#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# File Name: config.py
# Author: Sheng (Raymond) Liao
# Date: October 2021
#

"""
A module containing global definitions for the LCA third level character facial system
"""

# from enum import Enum, unique # WARNING: enum wasn't added to Python until 3.4

from general import util; reload(util)

# control zones partitioned in directions ------------------------------------------------------------------------------
# @unique
# class controlZoneEnum(Enum):
class controlZoneEnum(object):
    eyelid = 'eyelid'
    eyebrow = 'eyebrow'
    mouth = 'mouth'
    # nasolabial = 'nasolabial'
    # cheek = 'cheek'
    nasocheek = 'nasoCheek'

# control_zone_list = [name for name, member in controlZoneEnum.__members__.items()]
control_zone_list = util.get_enum_value_list(controlZoneEnum)

# @unique
# class controlZoneDirEnum(Enum):
class controlZoneDirEnum(object):
    """ The control zone direction names should be same with those in the keys to
    retrieve the control elements data in the JSON database files of this system.

    Note that the left+right direction combination corresponds to the "middle" zone.
    """
    left = 'left'       # abbr: L
    right = 'right'     # abbr: R
    middle = 'middle'   # abbr: M; Note that "middle" = "left_right"

    up = 'up'           # abbr: U
    down = 'dn'         # abbr: D

    front = 'front'     # abbr: F
    back = 'back'       # abbr: B

# control_zone_dir_list = [name for name, member in controlZoneDirEnum.__members__.items()]
control_zone_dir_list = util.get_enum_value_list(controlZoneDirEnum)

# @unique
# class dirDictKeyEnum(Enum):
class dirDictKeyEnum(object):
    LR = 'LR'
    UD = 'UD'
    FB = 'FB'

# dir_dict_key_list = [name for name, member in dirDictKeyEnum.__members__.items()]
# dir_dict_key_list = util.get_enum_value_list(dirDictKeyEnum)
dir_dict_key_list = ['LR', 'UD', 'FB']

ctrl_crv_bs_dir_list = ['original',
                        'right_side_up', 'middle_side_up', 'left_side_up',
                        'right_side_left', 'middle_side_left', 'left_side_left',
                        'right_side_front', 'middle_side_front', 'left_side_front']
ctrl_crv_bs_drving_gain = 1.2

# Empty string means no motion of controllers in these direction for the control zone.
CONTROL_ZONE_DIRECTION_DICT = {
    controlZoneEnum.eyelid: [
                                {
                                    dirDictKeyEnum.LR: controlZoneDirEnum.right,
                                    dirDictKeyEnum.UD: controlZoneDirEnum.up,
                                    dirDictKeyEnum.FB: ''
                                },
                                {
                                    dirDictKeyEnum.LR: controlZoneDirEnum.right,
                                    dirDictKeyEnum.UD: controlZoneDirEnum.down,
                                    dirDictKeyEnum.FB: ''
                                },
                                {
                                    dirDictKeyEnum.LR: controlZoneDirEnum.left,
                                    dirDictKeyEnum.UD: controlZoneDirEnum.up,
                                    dirDictKeyEnum.FB: ''
                                },
                                {
                                    dirDictKeyEnum.LR: controlZoneDirEnum.left,
                                    dirDictKeyEnum.UD: controlZoneDirEnum.down,
                                    dirDictKeyEnum.FB: ''
                                }
                            ],
    controlZoneEnum.eyebrow: [
                                {
                                    dirDictKeyEnum.LR: controlZoneDirEnum.left + '_' + controlZoneDirEnum.right,
                                    dirDictKeyEnum.UD: controlZoneDirEnum.up + '_' + controlZoneDirEnum.down,
                                    dirDictKeyEnum.FB: ''
                                },
                                {
                                    dirDictKeyEnum.LR: controlZoneDirEnum.left + '_' + controlZoneDirEnum.right,
                                    dirDictKeyEnum.UD: '',
                                    dirDictKeyEnum.FB: controlZoneDirEnum.front
                                }
                             ],
    controlZoneEnum.mouth:  [
                                {
                                    dirDictKeyEnum.LR: controlZoneDirEnum.left + '_' + controlZoneDirEnum.right,
                                    dirDictKeyEnum.UD: controlZoneDirEnum.up,
                                    dirDictKeyEnum.FB: ''
                                },
                                {
                                    dirDictKeyEnum.LR: controlZoneDirEnum.left + '_' + controlZoneDirEnum.right,
                                    dirDictKeyEnum.UD: controlZoneDirEnum.down,
                                    dirDictKeyEnum.FB: ''
                                }
                            ],
    # controlZoneEnum.nasolabial: [
    #                                 {
    #                                     dirDictKeyEnum.LR: controlZoneDirEnum.right,
    #                                     dirDictKeyEnum.UD: controlZoneDirEnum.up + '_' + controlZoneDirEnum.down,
    #                                     dirDictKeyEnum.FB: ''
    #                                 },
    #                                 {
    #                                     dirDictKeyEnum.LR: controlZoneDirEnum.left,
    #                                     dirDictKeyEnum.UD: controlZoneDirEnum.up + '_' + controlZoneDirEnum.down,
    #                                     dirDictKeyEnum.FB: ''
    #                                 }
    #                             ],
    # controlZoneEnum.cheek: [
    #                             {
    #                                 dirDictKeyEnum.LR: controlZoneDirEnum.right,
    #                                 dirDictKeyEnum.UD: controlZoneDirEnum.up + '_' + controlZoneDirEnum.down,
    #                                 dirDictKeyEnum.FB: ''
    #                             },
    #                             {
    #                                 dirDictKeyEnum.LR: controlZoneDirEnum.left,
    #                                 dirDictKeyEnum.UD: controlZoneDirEnum.up + '_' + controlZoneDirEnum.down,
    #                                 dirDictKeyEnum.FB: ''
    #                             }
    #                        ]
    controlZoneEnum.nasocheek: [
                                    {
                                        dirDictKeyEnum.LR: controlZoneDirEnum.right,
                                        dirDictKeyEnum.UD: controlZoneDirEnum.up + '_' + controlZoneDirEnum.down,
                                        dirDictKeyEnum.FB: ''
                                    },
                                    {
                                        dirDictKeyEnum.LR: controlZoneDirEnum.left,
                                        dirDictKeyEnum.UD: controlZoneDirEnum.up + '_' + controlZoneDirEnum.down,
                                        dirDictKeyEnum.FB: ''
                                    }
                               ]
}

# facial control display settings --------------------------------------------------------------------------------------
PROJ_SRF_SET = 'proj_plane_set'
PROJ_SRF_SHADER = 'proj_srf_shader'

COLOR_INDEX_LIGHT_GRAY = 0
COLOR_INDEX_BLACK = 1
COLOR_INDEX_GRAY = 2
COLOR_INDEX_DARK_WHITE = 3
COLOR_INDEX_CARMINE = 4
COLOR_INDEX_DARK_BLUE = 5
COLOR_INDEX_LIGHT_BLUE = 6
COLOR_INDEX_DARK_GREEN = 7
COLOR_INDEX_DARK_PURPLE = 8
COLOR_INDEX_MAGENTA = 9
COLOR_INDEX_LIGHT_BROWN = 10
COLOR_INDEX_DARK_BROWN = 11
COLOR_INDEX_DARK_RED = 12
COLOR_INDEX_LIGHT_RED = 13
COLOR_INDEX_LIGHT_GREEN = 14
COLOR_INDEX_BLUE = 15
COLOR_INDEX_WHITE = 16
COLOR_INDEX_LIGHT_YELLOW = 17
COLOR_INDEX_CYAN = 18
COLOR_INDEX_TURQUOISE = 19
COLOR_INDEX_PINK = 20
COLOR_INDEX_SALMON = 21
COLOR_INDEX_YELLOW = 22
COLOR_INDEX_GREEN_1 = 23
COLOR_INDEX_BROWN = 24
COLOR_INDEX_OLIVE = 25
COLOR_INDEX_GRASS_GREEN = 26
COLOR_INDEX_GREEN_2 = 27
COLOR_INDEX_PEACOCK_BLUE = 28
COLOR_INDEX_INDIGO = 29
COLOR_INDEX_VIOLET = 30
COLOR_INDEX_RED_VIOLET = 31

PROJ_SURFACE_COLOR_INDEX = COLOR_INDEX_DARK_WHITE
PROJ_SURFACE_LOC_COLOR_INDEX = COLOR_INDEX_DARK_RED

CTRL_CURVE_COLOR_INDEX = COLOR_INDEX_BLACK
CTRL_CURVE_LOC_COLOR_INDEX = COLOR_INDEX_BLACK

CONTROL_R_COLOR = COLOR_INDEX_CYAN
CONTROLLER_RU_COLOR = COLOR_INDEX_CYAN
CONTROLLER_RD_COLOR = COLOR_INDEX_CYAN
CONTROL_M_COLOR = COLOR_INDEX_LIGHT_YELLOW
CONTROL_L_COLOR = COLOR_INDEX_LIGHT_RED
CONTROLLER_LU_COLOR = COLOR_INDEX_LIGHT_RED
CONTROLLER_LD_COLOR = COLOR_INDEX_LIGHT_RED

BIND_JOINT_COLOR_INDEX = COLOR_INDEX_DARK_WHITE