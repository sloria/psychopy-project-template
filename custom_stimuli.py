# -*- coding: utf-8 -*-
'''Define custom, experiment-specific stimuli here.'''

from stimulus import Stimulus

class CustomAnimated3DFractalImageWithExplosionsAndRatingScale(Stimulus):

    def __init__(self, window, duration=5.0):
        self.window = window
        self.duration = duration

    def show(self):
        pass  # IMPLEMENT ME
