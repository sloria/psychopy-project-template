# -*- coding: utf-8 -*-
"""Classes that make it easy to create and present a series of
Psychopy stimuli.

Author: Steven Loria
License: MIT
"""
import ctypes  # used for input/output

from psychopy import core, visual, sound, event

class Paradigm(object):
    """Represents a study paradigm.
    """
    def __init__(self, window_dimensions=(720, 480),
                        color='Black', escape_key=None, *args, **kwargs):
        '''Initialize a paradigm.

        Arguments:
        window_dimensions - The dimensions of the Psychopy window object.
                            Use 'full_screen' to make a full screen paradigm.
        escape_key - The keyboard button that exits the paradigm.
        '''
        if window_dimensions == 'full_screen':
            self.window = visual.Window(fullscr=True,
                                        color=color, units='norm', *args, **kwargs)
        else:
            self.window = visual.Window(window_dimensions,
                                        color=color, units='norm', *args, **kwargs)

        # List of stimuli for this study
        self.stimuli = []
        self.escape_key = escape_key

    def add_stimulus(self, stimulus):
        '''Adds a stimulus.

        A stimuli must be a tuple of the form:
            (StimulusType, (arguments))

        Example:
        >> paradigm = Paradigm()
        >> paradigm.add_stimulus( (Text, ('Hi!', 3.0)) )
        '''
        assert type(stimulus) in (tuple, list), 'Stimulus must be a tuple of the form (StimulusType, (arguments))'
        self.stimuli.append(stimulus)

    def add_stimuli(self, stimuli):
        '''Adds multiple stimuli.

        Args:
        stimuli - A list of stimuli, formatted as tuples
                    (see add_stimulus for how to format stimuli)
        '''
        for stimulus in stimuli:
            self.add_stimulus(stimulus)

    def play_all(self, verbose=False):
        '''Plays all the stimuli in sequence.
        This simply runs the show() method for each stimuli
        in self.stimuli, then quits.
        '''
        stim_idx = 0
        while self.escape_key not in event.getKeys():
            stim_idx += 1
            if verbose: "Playing stimulus {stim_idx}".format(stim_idx=stim_idx)
            self.play_next()
        core.quit()
        print "Finished."

    def play_next(self, verbose=False):
        '''Plays the next stimuli in the sequence.
        '''
        if len(self.stimuli) > 0:
            stim_data = self.stimuli.pop(0) # The next stimulus tuple
            # Instantiate the stimulus object
            stim = self._initialize_stimulus(stim_data)
            # Show the stimulus
            if verbose: print stim
            return stim.show()
        else:
            core.quit()

    def _initialize_stimulus(self, stim_data):
        '''Initialize a stimulus object from a tuple of the form:
            (StimulusType, (arguments)).

        Args:
        stim_data - The stimulus and its arguments as a tuple

        '''
        stim_class = stim_data[0] # The class of the stimulus
        # Get stim args if passed
        # If not, an empty tuple is passed to the stimulus constructor
        stim_args = stim_data[1] if type(stim_data[1])==tuple else tuple()
        # Get the kwargs if they are passed
        try:
            # the index of the kwargs in stim_data depends on whether
            # positional args were passed
            stim_kwargs = stim_data[2] if stim_args else stim_data[1]
        except IndexError:
            # If no kwargs were passed, just pass an empty dict
            stim_kwargs = {}
        return stim_class(self.window, *stim_args, **stim_kwargs)


class Stimulus(object):
    """An abstract stimulus class. All stimulus types will inherit
    from this class.
    """
    def show(self):
        '''Show the stimuli. This must be implemented by
        descendant classes.'''
        raise NotImplementedError

    def close(self):
        '''Close out.
        '''
        core.quit()


class Text(Stimulus):
    '''A text stimulus.
    '''
    def __init__(self, window, text, duration=2.0, keys=None):
        '''Initialize a text stimulus.

        Args:
        window - The window object
        text - text to display
        duration - the duration the text will appear
        keys - list of keys to press to continue to next stimulus. If None,
                will automatically go to the next stimulus.

        Additional args and kwargs are passed to the visual.TextStim
        constructor.
        '''
        self.window = window
        self.text = visual.TextStim(self.window, text=text, units='norm')
        self.duration = duration
        self.keys = keys

    def show(self):
        self.text.draw()
        self.window.flip()
        core.wait(self.duration)
        if self.keys:
            # Wait for keypress
            wait_for_key(self.keys)
        self.window.flip()
        return self


class Audio(Stimulus):
    '''A simple audio stimulus.'''
    def __init__(self, window,
                    value,
                    text=None,
                    *args, **kwargs):
        '''Constructor for the Audio stimulus.

        Arguments:
        value - A number (pitch in Hz), string for a note,
                or string for a filename.
                For more info, see:
                http://www.psychopy.org/api/sound.html
        text - Text to display on screen (Optional).

        Additional args and kwargs are passed to the
        sound.Sound constructor.
        '''
        self.window = window
        self.sound = sound.Sound(value, *args, **kwargs)
        self.text = visual.TextStim(self.window, text=text)

    def show(self):
        if self.text: self.text.draw()
        self.window.flip()
        self.sound.play()
        core.wait(self.sound.getDuration())
        return self


class Video(Stimulus):
    '''A basic video stimulus.
    '''
    def __init__(self, window, movie, movie_dimensions=None, *args, **kwargs):
        '''Constructor for the Video stimulus.

        Arguments:
            movie - A filename (string) for the video file.
            movie_dimensions - Movie dimensions. If not specified, defaults to
                        50\% of the window area.
        '''
        self.window = window
        movie_dims = None
        if movie_dimensions:
            movie_dims = movie_dimensions
        else:
            # Default movie to half of the window area
            movie_dims = (self.window.size[0] / 2, self.window.size[1] / 2)
        self.mov = visual.MovieStim(self.window, movie, size=movie_dims,
                                    flipVert=False, loop=False, *args, **kwargs)

    def show(self):
        '''Show the stimulus (movie).
        '''
        while self.mov.status != visual.FINISHED:
            self.mov.draw()
            self.window.update()
        self.window.flip()
        return self


class VideoRating(Video):
    '''A stimulus with simultaneous video playback and valence rating (Likert).
    Ratings are saved to a CSV file in where each row is of the format: Rating,Time
    '''
    # labels on either side of the scale.
    def __init__(self, window, movie, destination_path,
                movie_dimensions=(1, 1), units='norm',
                tick_marks=[1, 2, 3, 4, 5, 6, 7, 8, 9],
                rating_description='Very negative  . . .  Very positive',
                header_text = None,
                header_size=0.15,
                stretch_horizontal=2.7,
                marker_style='triangle', marker_color='White', marker_start=5,
                low=1, high=9, pos=None,
                button_box=None,
                *args, **kwargs):

        self.window = window
        # FIXME: video should mantain aspect ratio regardless of window dimensions
        self.mov = visual.MovieStim(self.window,
                                    movie,
                                    size=movie_dimensions,
                                    units=units,
                                    flipVert=False,
                                    loop=False)

        # Header text
        if header_text:
            self.header_text = visual.TextStim(self.window,
                                                text=header_text,
                                                pos=(0, 0.7),
                                                height=header_size,
                                                wrapWidth=2.0, # ??
                                                units=units)
        else:
            self.header_text = None

        self.rating_scale = visual.RatingScale(self.window, low=low, high=high,
                            tickMarks=tick_marks, precision=1,
                            pos=(0, -0.75), stretchHoriz=stretch_horizontal,
                            showAccept=False, acceptKeys=[None],
                            markerStyle=marker_style, markerColor=marker_color,
                            markerStart=marker_start,
                            *args, **kwargs)
        self.rating_scale.setDescription(rating_description)
        # The destination path to write the history to
        self.dest= destination_path
        self.button_box = button_box

    def show(self):
        # Reset the scale
        self.rating_scale.reset()
        # Start the rating at 5
        # Show and update until the movie is done
        while self.mov.status != visual.FINISHED:
            if self.button_box:
                keys = self.button_box.getEvents(returnRaw=True, asKeys=True)
                self.button_box.clearBuffer()
            self.mov.draw()
            self.rating_scale.draw()
            if self.header_text: self.header_text.draw()
            self.window.flip()
        # Write the history to a csv
        self.write_history()
        return self

    def write_history(self):
        '''Writes the rating history data to a CSV file
        at the specified destination path.
        '''
        rating_history = self.rating_scale.getHistory()
        if len(rating_history) > 0:
            print "Writing rating history..."
            with open(self.dest, 'w') as history_file:
                # Write header
                history_file.write('Rating,Time\n')
                for i, event in enumerate(rating_history):
                    # Skip the (None, 0.0) event
                    if i == 0:
                        continue
                    # Write data
                    rating, time = event
                    row = "{0},{1}\n".format(rating, round(time, 8))  # e.g. "3, 2.524"
                    history_file.write(row)
            print "Wrote to {0}".format(self.dest)
        else:
            print "Rating history is empty. Nothing written"


class Pause(Stimulus):
    '''A simple pause.
    '''
    def __init__(self, window, duration):
        self.window = window
        self.duration = float(duration)

    def show(self):
        core.wait(self.duration)
        return self


class WaitForTTL(Stimulus):
    """Wait for a TTL pulse before proceeding to next stimulus.
    """
    def __init__(self, window, address, par=None, event='continue'):
        """Initialize the stimulus.

        Args:
        address - Address of the TTL input device.
        event - The event to be triggered after the TTL pulse.
                Can be 'exit' or 'continue' (proceed to next stimulus).
                Defaults to 'continue'.
        """
        self.window = window
        self.event = event
        if not par:
            self.par = ctypes.windll.inpout32
        self.address = address

    def show(self):
        event.clearEvents()
        current = self.par.Inp32(self.address)
        initial = current
        # Wait for TTL pulse
        while initial == current:
            current = self.par.Inp32(self.address)
        # After the TTL pulse, run the event
        self.run_event()
        return self

    def run_event(self):
        """Execute the specified event (either exit or continue).
        """
        if self.event == 'exit':
            print "Exiting. . ."
            self.window.close()
            core.quit()
        if self.event in ['nothing', 'continue']:
            pass
        else:
            print "Warning: Event not recognized. Doing nothing."


class WaitForKey(Stimulus):
    '''Wait for a keypress.'''
    def __init__(self, window, keys, event='continue'):
        '''Initialize the stimulus.

        Args:
        keys - A list of keys to wait for.
        event - The event to be triggered when one of the
                keys is pressed. Can be 'exit' or 'continue'.
                Defaults to 'continue'.
        '''
        self.window = window
        self.keys = keys
        self.event = event

    def show(self):
        wait_for_key(self.keys)
        self.run_event()
        return self

    def run_event(self):
        if self.event == 'exit':
            print "Exiting. . ."
            self.window.close()
            core.quit()
        if self.event in ['nothing', 'continue']:
            pass
        else:
            print "Warning: Event not recognized. Doing nothing."

def wait_for_key(keys):
    '''Wait for a key that is in a set of keys
    to be pressed before proceeding.

    Args:
    keys - A list or tuple of keys.
    '''
    event.clearEvents()
    event.waitKeys(keyList=keys)
