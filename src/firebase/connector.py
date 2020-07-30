import logging
import math
import operator
from functools import reduce
from threading import Thread

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from patterns import Patterns

fire_logger = logging.getLogger("fire_logger")


class FireBaseConnector(Thread):
    """
    Firebase connecting class.
    Allows for the modification of the pattern and attributes
    """

    def __init__(self, credential_path, database_url="https://ledypie.firebaseio.com/", debug=None):

        # init thread class
        super().__init__()
        self.stop = False

        cred = credentials.Certificate(credential_path)

        if debug is not None:
            fire_logger.setLevel(logging.DEBUG)

        firebase_admin.initialize_app(credential=cred,
                                      options={'databaseURL': database_url})

        self.fb = db.reference('/')
        self.listener = self.fb.listen(self.listener)

        self.rgba = None
        self.random_colors = False

        # update db with patterns
        self.local_db = None

        self.fb.update(dict(patterns='.'.join(Patterns)))
        self.init_attributes()
        # update rgba
        self.floor_rgba()

    def listener(self, event):
        """
        Update the local db on every change
        :param event:
        :return:
        """

        # if the local db has not been initialized yet, do it
        if self.local_db is None:
            self.local_db = event.data
            return

        # get all the keys, remove empty
        keys = event.path.split("/")
        keys = [elem for elem in keys if elem]
        # update local db
        set_in_dict(self.local_db, keys, event.data)

        self.floor_rgba()

    def run(self) -> None:

        try:
            while not self.stop:
                pass
        except KeyboardInterrupt:
            fire_logger.info("FireBaseConnector has been interrupted")

        self.close()

    def close(self):
        fire_logger.info("Closing firebase connection, this make take a few seconds...")
        self.stop = True

    def init_attributes(self):
        """
        Add all the attributes from the default modifier dictionary to the remote database
        """
        # get the attributes from the remote
        data = self.get("pattern_attributes")

        if data is None:
            data = {}

        pattern_attributes = {}

        # for every pattern in the pattern dict
        for k, pt in Patterns.items():
            remote_att = {}
            # get the local ones and find differences
            local_att = pt(handler=None, rate=1, pixels=1).modifiers
            # get the remote attributes
            try:
                remote_att = data[k]
            except KeyError:
                if len(local_att) > 0:
                    fire_logger.warning(f"Patter '{k}' not found in pattern dict")

            # set the remote ones by default
            pattern_attributes[k] = remote_att

            to_add = set(local_att.keys()) - set(remote_att.keys())

            # for every difference update with the local one
            for at in to_add:
                pattern_attributes[k][at] = local_att[at]

        # update the database
        self.fb.update(dict(pattern_attributes=pattern_attributes))

        return pattern_attributes

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

    def floor_rgba(self):
        """
        Update RGBA values taking them from the database
        :return:
        """

        # get data from db
        rgba = self.local_db["RGBA"]

        # remove points
        rgba = {k: v.split('.')[0] if '.' in v else v for k, v in rgba.items()}

        # update
        self.local_db["RGBA"] = rgba


def floor_int(value):
    value = float(value)
    value = math.floor(value)
    return int(value)


def get_from_dictr(data_dict, map_list):
    return reduce(operator.getitem, map_list, data_dict)


def set_in_dict(data_dict, map_list, value):
    get_from_dictr(data_dict, map_list[:-1])[map_list[-1]] = value
