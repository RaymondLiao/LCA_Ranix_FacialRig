#
# Copyright (c) 2021 Light Chaser Animation Studios. All Rights Reserved.
#
# File Name: util.py
# Author: Sheng (Raymond) Liao
# Date: October 2021
#

"""
A module containing utility functions used by the LCA third level character facial system
"""

def get_class_name(obj_or_class):
    """
    :param obj_or_class: a class or a class's instance
    :return: a string of the class's name
    """

    cls = type(obj_or_class)
    if cls is type:
        cls = obj_or_class

    return cls.__name__.split('.')[-1]

def get_enum_value_list(enum_class):
    """ Because Python does not support enum types until version 3.4, we have to define enum classes
    with enumerated attributes by ourselves; and we use this function to retrieve the enumerated values as a list.

    :param enum_class: custom "enumeration" class who keeps enumerated values as class attributes
    :return: a list of values of the custom enumeration classes' attributes
    """

    # Make sure the incoming argument is a name of the "enumeration" classes we defined in this module.
    enum_class_name = get_class_name(enum_class)
    assert 'controlZoneEnum' == enum_class_name or \
            'controlZoneDirEnum' == enum_class_name

    res_list = [attr
                for attr in dir(enum_class)
                if not callable(getattr(enum_class, attr))
                and not attr.startswith('__')]

    return res_list