import urllib.request

import PIL.Image
import numpy as np

from patterns.default import Default
from utils.modifier import Modifier


class Image(Default):
    """
    Turno on/off the strip with a specific speed
    """

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.pattern_name = "Image"

        self.image = None
        self.image_url = Modifier('image url',
                                  "https://raw.githubusercontent.com/nicofirst1/ledypi/master/Resources/logo.png",
                                  on_change=self.on_change)

        self.step = 0
        self.modifiers = dict(
            loss=self.image_url,
        )

    def on_change(self, value):
        """
        Read image
        :param value:
        :return:
        """

        try:

            # open image from url and convert to array
            img = PIL.Image.open(urllib.request.urlopen(value)).convert('RGB')
            img = np.array(img)

            # reduce/expand third dimension to be 3
            if img.shape[2] > 3:
                img = img[:, :, :3]

            # resize using csv interpolation
            #fixme: use something compatible with Apache
            import cv2
            img = cv2.resize(img, dsize=(self.strip_length, img.shape[1],), interpolation=cv2.INTER_CUBIC)

            # add brightness level
            img = np.insert(img, 3, 255, axis=2)

            # show image
            # PIL.Image.fromarray(img, "RGBA").show()

            # set image
            self.image = img
        except PIL.UnidentifiedImageError:
            print("No image found in the provided url")
        except ValueError:
            print(f"'{value}' is not a valid url")
        except urllib.error.HTTPError:
            print("the image could not be provided")

    def fill(self):

        # set the pixel
        for idx in range(self.strip_length):
            self.pixels[idx]['color'] = self.image[self.step, idx]

        self.step += 1
        self.step %= self.image.shape[0]
