import logging

import numpy as np
import pyaudio

from config import CONFIGS
from patterns.default import Default
from utils.modifier import Modifier
from visualization import Visualizer

_gamma = np.load(CONFIGS['gamma_table_path'])
"""Gamma lookup table used for nonlinear brightness correction"""

music_logger = logging.getLogger("music_logger")
music_logger.setLevel(logging.INFO)


class Music(Default):
    """
    Music reactive leds
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pattern_name = "Music"

        CONFIGS['n_pixels'] = self.strip_length

        # init visualizer
        self.vis = Visualizer(CONFIGS)

        # dict used to set the visualizer effect
        self.effect_dict = dict(
            spectrum=self.vis.visualize_spectrum,
            energy=self.vis.visualize_energy,
            scroll=self.vis.visualize_scroll,
        )

        # name of the effect to be used
        self.effect = Modifier('visualizer', "spectrum", options=list(self.effect_dict.keys()),
                               on_change=self.on_change)
        self._rate = Modifier('Delay', 0, minimum=0, maximum=0)

        self.modifiers = dict(
            effect=self.effect,
        )

        # attributes for the mic
        self.p = None
        self.stream = None
        self.frames_per_buffer = int(CONFIGS['mic_rate'] / CONFIGS['fps'])

        try:
            # do not initialize if the pattern is temp
            if kwargs['handler'] is not None:
                self.setup()
        except OSError:
            music_logger.warning(f"Could not initialize the audio stream")

    def setup(self):
        """
        Setup stream
        """
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=CONFIGS['mic_rate'],
                                  input=True,
                                  frames_per_buffer=self.frames_per_buffer)

        music_logger.info(f"Audio stream initialized with {CONFIGS['fps']} fps")

    def on_change(self, value):
        """
        Set the effect to a certain value and change the visualization effect in the vis calss
        """
        try:
            ef = self.effect_dict[value]
            self.vis.visualization_effect = ef

        except KeyError as e:
            music_logger.warning(f"Error for key {value}\n{e}")

    @property
    def rate(self):
        """
        Rate should always be zero here
        """
        return self._rate

    @rate.setter
    def rate(self, value):
        """
        Cannot change the value of rate since music must be real time
        :param value:
        :return:
        """
        pass

    def read_audio(self):
        """
        Read audio and return it
        """
        try:
            y = np.fromstring(self.stream.read(self.frames_per_buffer, exception_on_overflow=False),
                              dtype=np.int16)
            y = y.astype(np.float32)
            return y
        except IOError:
            music_logger.warning('Audio buffer has overflowed')
        except AttributeError:
            music_logger.error("Could not read from audio buffer, do you have a microphone?")
            self.close()

    def fill(self):
        """
        Read from audio stream and set pixels
        """
        # read audio input, can also be none when the mic has not started yet
        output = self.read_audio()

        try:
            # use visualization
            pixels, _ = self.vis.audio_to_rgb(output)
            # Truncate values and cast to integer
            pixels = np.clip(pixels, 0, 255).astype(int)
            # Optional gamma correction
            pixels = _gamma[pixels]

            r, g, b = pixels
            for idx in range(len(r)):
                self.pixels[idx]['color'] = (r[idx], g[idx], b[idx], 255)

        except TypeError:
            pass

    def close(self):
        """
        Call super method and close audio stream
        """
        super(Music, self).close()

        try:
            # try to stop the stream if any
            self.stream.stop_stream()
            self.stream.close()
        except AttributeError:
            # if there is no recognized microphone then the close operation will fail on the stream
            pass
        finally:
            # terminate the py audio and log
            self.p.terminate()
            music_logger.info("Audio stream stopped")
