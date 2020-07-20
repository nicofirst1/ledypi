import time

import numpy as np
import pyaudio
from scipy.ndimage import gaussian_filter1d

import config
import dsp
from patterns.default import Default
from visualization import mel_gain, mel_smoothing, fft_window, visualize_spectrum, \
    visualize_energy, visualize_scroll

# Number of audio samples to read every time frame
samples_per_frame = int(config.MIC_RATE / config.FPS)
# Array containing the rolling audio sample window
y_roll = np.random.rand(config.N_ROLLING_HISTORY, samples_per_frame) / 1e16
_gamma = np.load(config.GAMMA_TABLE_PATH)
"""Gamma lookup table used for nonlinear brightness correction"""
frames_per_buffer = int(config.MIC_RATE / config.FPS)

class Music(Default):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pattern_name = "Music"

        self.visualizations_dict = dict(
            spectrum=visualize_spectrum,
            energy=visualize_energy,
            scroll=visualize_scroll,
        )

        self.visualizer = self.visualizations_dict['spectrum']

        self.modifiers = dict(
            visualizer=self.visualizer,
        )

        self.p = None
        self.stream = None
        self.setup()

    def setup(self):
        """
        Setup stream
        """
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=config.MIC_RATE,
                                  input=True,
                                  frames_per_buffer=frames_per_buffer)

    @property
    def rate(self):
        return 0

    @rate.setter
    def rate(self, value):
        pass

    def read_audio(self):
        try:
            y = np.fromstring(self.stream.read(frames_per_buffer, exception_on_overflow=False), dtype=np.int16)
            y = y.astype(np.float32)
            self.stream.read(self.stream.get_read_available(), exception_on_overflow=False)
            return y
        except IOError:
            print('Audio buffer has overflowed')

    def fill(self):
        """
        Read from audio stream and set pixels
        """


        output=self.read_audio()

        try:
            pixels = microphone_update(output, self.visualizer)
            # Truncate values and cast to integer
            pixels = np.clip(pixels, 0, 255).astype(int)
            # Optional gamma correction
            pixels = _gamma[pixels]

            r, g, b = pixels
            for idx in range(len(r)):
                self.pixels[idx]['color'] = (r[idx], g[idx], b[idx], 255)

        except TypeError:
            pass



    def stop(self):
        """
        Call super method and close audio stream
        """
        super(Music, self).stop()

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()


def microphone_update(audio_samples, visualizer):
    """
    Function adapted from audio-reactive-led-strip
    """
    global y_roll
    # Normalize samples between 0 and 1
    y = audio_samples / 2.0 ** 15
    # Construct a rolling window of audio samples
    y_roll[:-1] = y_roll[1:]
    y_roll[-1, :] = np.copy(y)
    y_data = np.concatenate(y_roll, axis=0).astype(np.float32)

    vol = np.max(np.abs(y_data))
    if vol < config.MIN_VOLUME_THRESHOLD:
        print('No audio input. Volume below threshold. Volume:', vol)
        output = np.tile(0, (3, config.N_PIXELS))

    else:
        # Transform audio input into the frequency domain
        N = len(y_data)
        N_zeros = 2 ** int(np.ceil(np.log2(N))) - N
        # Pad with zeros until the next power of two
        y_data *= fft_window
        y_padded = np.pad(y_data, (0, N_zeros), mode='constant')
        YS = np.abs(np.fft.rfft(y_padded)[:N // 2])
        # Construct a Mel filterbank from the FFT data
        mel = np.atleast_2d(YS).T * dsp.mel_y.T
        # Scale data to values more suitable for visualization
        # mel = np.sum(mel, axis=0)
        mel = np.sum(mel, axis=0)
        mel = mel ** 2.0
        # Gain normalization
        mel_gain.update(np.max(gaussian_filter1d(mel, sigma=1.0)))
        mel /= mel_gain.value
        mel = mel_smoothing.update(mel)
        # Map filterbank output onto LED strip
        output = visualizer(mel)

    return output
