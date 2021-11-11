#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# File Name: lv3chr_facialsys_config.py
# Author: Sheng (Raymond) Liao
# Date: October 2021
#

"""
A module containing global definitions for the LCA level three character facial system
"""

# from enum import Enum, unique # WARNING: enum wasn't added to Python until 3.4

# control zones partitioned in directions ------------------------------------------------------------------------------
# @unique
# class controlZoneEnum(Enum):
class controlZoneEnum(object):
    eyelid = 'eyelid'
# control_zone_list = [name for name, member in controlZoneEnum.__members__.items()]
control_zone_list = [attr
                     for attr in dir(controlZoneEnum)
                     if not callable(getattr(controlZoneEnum, attr))
                     and not attr.startswith('__')]

# @unique
# class controlZoneDirEnum(Enum):
class controlZoneDirEnum(object):
    right_up = 'right_up'
    right_dn = 'right_dn'
    left_up = 'left_up'
    left_dn = 'left_dn'
# control_zone_dir_list = [name for name, member in controlZoneDirEnum.__members__.items()]
control_zone_dir_list = [attr
                         for attr in dir(controlZoneDirEnum)
                         if not callable(getattr(controlZoneDirEnum, attr))
                         and not attr.startswith('__')]

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
CTRL_CURVE_LOC_COLOR_INDEX = COLOR_INDEX_DARK_RED
CONTROLLER_UP_COLOR = COLOR_INDEX_LIGHT_YELLOW
CONTROLLER_DN_COLOR = COLOR_INDEX_CYAN