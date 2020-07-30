import logging
import math

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from patterns import Patterns
from rgb import RGB
from threading import Thread
fire_logger = logging.getLogger("fire_logger")


class FireBaseConnector(Thread):
    """
    Firebase connecting class.
    Allows for the modification of the pattern and attributes
    """

    def __init__(self, credential_path, database_url, debug=None):

        # init thread class
        super().__init__()
        self.stop=False

        cred = credentials.Certificate(credential_path)

        if debug is not None:
            fire_logger.setLevel(logging.DEBUG)

        firebase_admin.initialize_app(credential=cred,
                                      options={'databaseURL': database_url})

        self.fb = db.reference('/')

        self.rgba = None
        self.random_colors = False

        # update db with patterns
        self.fb.update(dict(patterns='.'.join(Patterns)))
        self.init_attributes()
        # get pattern,rate
        self.pattern_choice = self.get_cur_pattern()
        self.rate = self.get_rate()
        # update rgba
        self.update_rgba()

    def run(self) -> None:

        try:
            while not self.stop:
                pass
        except KeyboardInterrupt:
           pass

        self.close()


    def close(self):
        fire_logger.info("Closing firebase connection, this make take a few seconds...")
        self.stop=True

    def init_attributes(self):
        """
        Add all the attributes from the default modifier dictionary to the remote database
        """
        # get the attributes from the remote
        data = self.get("pattern_attributes")
        pattern_attributes = {}

        # for every pattern in the pattern dict
        for k, pt in Patterns.items():
            remote_att = {}
            # get the remote attributes
            try:
                remote_att = data[k]
            except Exception:
                fire_logger.warning(f"Patter '{k}' not found in pattern dict")

            # set the remote ones by default
            pattern_attributes[k] = remote_att

            # get the local ones and find differences
            local_att = pt(handler=None, rate=1, pixels=1).modifiers
            to_add = set(local_att.keys()) - set(remote_att.keys())

            # for every difference update with the local one
            for at in to_add:
                pattern_attributes[k][at] = local_att[at]

        # update the database
        self.fb.update(dict(pattern_attributes=pattern_attributes))

    def get(self, key, default=None):
        """
        Get a key from the database
        :param key: str, key to get
        :param default: obj, default value to return if key is not found
        :return: the key
        """
        gets = self.fb.get()

        if key in gets.keys():
            return gets[key]

        return default

    def get_rate(self, data=None):
        """
       Manipulate rate output from db
       :param data: str, data from db, optional, will be loaded if None
       :return: int, Usable data
       """
        if data is None:
            data = self.get('rate')

        return floor_int(data)

    def get_cur_pattern(self, data=None):
        """
        Manipulate cur_pattern output from db
        :param data: str, data from db, optional, will be loaded if None
        :return: str, Usable data
        """
        if data is None:
            data = self.get('cur_pattern')

        return data.replace('"', '')

    def update_rgba(self):
        """
        Update RGBA values taking them from the database
        :return:
        """

        # get data from db
        rgba = self.get("RGBA")

        # extract values
        r = rgba.get("r")
        g = rgba.get("g")
        b = rgba.get("b")
        a = rgba.get("a")

        # convert them to ints
        r = floor_int(r)
        g = floor_int(g)
        b = floor_int(b)
        a = floor_int(a)

        # update attr
        self.rgba = RGB(r=r, g=g, b=b, a=a)

        # extract random value and convert to bool
        self.random_colors = rgba.get("random") == "true"

        # todo : return update


def floor_int(value):
    value = float(value)
    value = math.floor(value)
    return int(value)
