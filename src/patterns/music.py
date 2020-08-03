from logging import getLogger

import numpy as np
import pyaudio

from config import CONFIGS
from patterns.default import Default
from visualization import Visualizer

_gamma = np.load(CONFIGS['gamma_table_path'])
"""Gamma lookup table used for nonlinear brightness correction"""

music_logger = getLogger("music_logger")


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
        self.effect = 'spectrum'

        self.modifiers = dict(
            visualizer=self.effect,
            __visualizer=list(self.effect_dict.keys())
        )

        # attributes for the mic
        self.p = None
        self.stream = None
        self.frames_per_buffer = int(CONFIGS['mic_rate'] / CONFIGS['fps'])

        try:
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

        music_logger.info("Audio stream initialized")

    @property
    def effect(self):
        return self._effect

    @effect.setter
    def effect(self, value):
        """
        Set the effect to a certain value and change the visualization effect in the vis calss
        """
        try:
            ef = self.effect_dict[value]
            self.vis.visualization_effect = ef
            self._effect = value

        except KeyError as e:
            print(f"Error for key {value}\n{e}")

    @property
    def rate(self):
        """
        Rate should always be zero here9
        """
        return 0

    @rate.setter
    def rate(self, value):
        pass

    def read_audio(self):
        """
        Read audio and return it
        """
        try:
            y = np.fromstring(self.stream.read(self.frames_per_buffer, exception_on_overflow=False),
                              dtype=np.int16)
            y = y.astype(np.float32)
            self.stream.read(self.stream.get_read_available(), exception_on_overflow=False)
            return y
        except IOError:
            print('Audio buffer has overflowed')

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

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        music_logger.info("Audio stream stopped")
