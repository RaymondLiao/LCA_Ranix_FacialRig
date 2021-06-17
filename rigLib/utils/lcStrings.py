#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# Author: Sheng (Raymond) Liao
# Date: June 2021
#

'''
module for dealing with strings such as retrieving useful information in sub-strings.
'''

import maya.cmds as cmds

def GetSPluginFileName( pluginModuleInfo ):
    '''

    :param pluginModuleInfo: the module information printed in the Script Editor.
                             e.g. <module 'LCA_Ranix_FacialRig.rigLib.experiment.sineNodeTEST' from 'D:/liaosheng/Maya Projects\LCA_Ranix_FacialRig\rigLib\experiment\sineNodeTEST.pyc'>
    :return: the scripted plug-in name string, e.g. sineNodeTEST.pyc,
             or None if the sub-string does not contain .py or .pyc
    '''
    res = str( pluginModuleInfo ).split( "from" )[-1].lstrip( " \'" ).rstrip( "\'>" )
    if '.py' not in res:
        return None

    return res