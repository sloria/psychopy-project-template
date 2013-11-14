#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Runs the experiment.

This uses the stimulus.py classes to create a paradigm 
and display them.

This file is the responsibility of the experiment programmer.

Author: 
Editor: 
'''
from psychopy import logging
from stimulus import Paradigm, Text
from custom_stimuli import *

from settings import get_settings
import experiment as ex

settings = get_settings(env='dev', test=True)

def run_experiment():
    par = construct_paradigm()  # Construct paradigm
    if par: par.play_all()      # Blastoff!

def construct_paradigm():
    # Initialize a paradigm
    par = Paradigm(window_dimensions=settings['window_dimensions'],
                    escape_key='escape')
    # Create list of stimuli from variables in
    # experiment.py
    stimuli = [
        (Text, (ex.instructions01, ex.duration01)),
        (Text, (ex.text02, ex.duration02)),
        (Text, ('+', 1.0)), # A fixation cross
        (Text, (ex.text03, ex.duration03)),
        # and so on...
    ]

    # Add the stimuli to the paradigm
    par.add_stimuli(stimuli)
    return par

if __name__ == '__main__':
    logging.console.setLevel(settings['logging_level'])
    run_experiment()