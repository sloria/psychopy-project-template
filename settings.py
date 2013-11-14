# -*- coding: utf-8 -*-
'''settings.py
Define global and environment-specific settings here.
'''
import os
from psychopy import logging

# Base settings that apply to all environments.
# These settings can be overwritten by any of the 
# environment settings.
BASE = {
    'test': False,
    'mouse_visible': False,
    'logging_level': logging.INFO
}

# Testing settings
TEST = {
    'test': True,
    'logging_level': logging.DEBUG
}

# Production settings
PRODUCTION = {
    'test': False,
    'logging_level': logging.INFO
}

# Development environment settings. Used for testing,
# outside of the MR room.
DEV = {
    'env': 'dev',  # Enviroment name
    'window_dimensions': (800, 600),
    'button_box': None,  # No button box

    # Number of runs
    'n_runs': 1,

    # Rating scale descriptions
    'gaze_desc': "Left                   \
                                        Right",
    'self_desc': "Very Negative                   \
                                        Very Positive",
    'other_desc': "Very Negative                   \
                                        Very Positive",
}

MRI = {
    'env': 'mri',
    'window_dimensions': "full_screen",
    # ButtonBox settings
    'button_box_port': 1,
    'button_box_rate': 19200,
    # Button box key mappings
    'left_key': "2",
    'right_key': '1',
    # Address for Biopac output
    'biopac_out': 0x3010,
    # TTL input address
    'ttl_in': 0x3011,
}

SIM = {
    'env': 'sim',
    'window_dimensions': "full_screen",
    # ButtonBox settings
    'button_box_port': 1,
    'button_box_rate': 19200,
    # Button box key mappings
    'left_key': "2",
    'right_key': '1',
    # Address for Biopac output
    'biopac_out': 0x3010,
}

def get_settings(env, test=False):
    '''Return a dictionary of settings based on 
    the specified environment, given by the parameter 
    env. Can also specify whether or not to use testing settings.
    '''
    # Start with the base settings
    settings = BASE
    # Update it with either the test or production settings
    settings.update(TEST) if test else settings.update(PRODUCTION)
    if env == 'dev':
        settings.update(DEV)
    elif env == 'mri':
        settings.update(MRI)
    elif env == 'sim':
        settings.update(SIM)
    else:
        raise ValueError, 'Environment "{0}" not supported.'.format(env)
    return settings
