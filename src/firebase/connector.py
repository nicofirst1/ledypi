import logging
import math
import operator
import time
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

        self.root = db.reference('/')

        self.rgba = None
        self.random_colors = False

        # update db with patterns
        self.local_db = None

        self.root.update(dict(patterns='.'.join(Patterns)))
        self.init_attributes()
        self.init_rgba()
        self.init_other()
        self.pattern_attributes = db.reference('/pattern_attributes')

        self.listener = self.root.listen(self.listener)
        time.sleep(1)

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

        if event.event_type == "patch": return

        # get all the keys, remove empty
        keys = event.path.split("/")
        keys.pop(0)
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

    def check_diff(self, request):

        # check for pattern difference
        rq_pattern = request.get("cur_pattern")
        if not rq_pattern == "" and rq_pattern != self.local_db.get("cur_pattern"):
            # if yes update both local and remote
            self.root.update(dict(cur_pattern=rq_pattern))
            self.local_db["cur_pattern"] = rq_pattern

        # check for rate difference
        rq_rate = request.get("rate")
        rq_rate=int(rq_rate)
        if rq_rate != self.local_db.get("rate"):
            # if yes update both local and remote
            self.root.update(dict(rate=rq_rate))
            self.local_db["rate"] = rq_rate

        # map random switch from on/missing to true/false
        if "random" in request.keys():
            request['random'] = True
        else:
            request['random'] = False

        # check for rgba difference
        to_update = {}
        for k, v in self.local_db['RGBA'].items():
            rq = int(request.get(k))
            if v != rq:
                to_update[k] = rq

        if len(to_update) > 0:
            to_update = dict(list(self.local_db["RGBA"].items()) + list(to_update.items()))
            self.root.update(dict(RGBA=to_update))
            self.local_db["RGBA"] = to_update

        # update pattern attributes
        to_update = {}

        for k, v in self.local_db['pattern_attributes'][rq_pattern].items():
            try:
                if request[k] != v:
                    to_update[k] = request[k]
            except KeyError:
                continue

        if len(to_update) > 0:
            to_update = dict(list(self.local_db['pattern_attributes'][rq_pattern].items()) + list(to_update.items()))
            self.pattern_attributes.update(dict(rq_pattern=to_update))
            self.local_db["pattern_attributes"][rq_pattern] = to_update

    def init_other(self):
        """
        Add rate, cur_pattern and patterns to the database if not present
        :return:
        """

        to_update={}
        # check rate
        val = self.get("rate", None)
        if val is None:
            to_update['rate'] = 10

        # check cur_pattern
        val = self.get("cur_pattern", None)
        if val is None:
            to_update['cur_pattern'] = "Steady"

        # check patterns
        val = self.get("patterns", None)
        if val is None:
            to_update['patterns'] = ".".join(Patterns.keys())

        if len(to_update)>0:
            self.root.update(to_update)


    def init_rgba(self):
        """
        Add RGBA to the database if not present
        :return:
        """

        data = self.get("RGBA", {})

        RGBA = dict(
            r=255, g=255, b=255, a=100, random=0
        )

        to_update = {}
        for k, v in RGBA.items():

            try:
                if data[k] != v:
                    to_update[k] = data[k]
            except KeyError:
                to_update[k] = v

        if len(to_update) > 0:
            to_update = dict(list(RGBA.items()) + list(to_update.items()))
            self.root.update(dict(RGBA=to_update))

    def init_attributes(self):
        """
        Add all the attributes from the default modifier dictionary to the remote database
        """
        # get the attributes from the remote
        data = self.get("pattern_attributes", {})

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
        self.root.update(dict(pattern_attributes=pattern_attributes))

        return pattern_attributes

    def get(self, key, default=None):
        """
        Get a key from the database
        :param key: str, key to get
        :param default: obj, default value to return if key is not found
        :return: the key
        """
        gets = self.root.get()

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
        # todo: check if android can go with int
        # rgba = {k: v.split('.')[0] if '.' in v else v for k, v in rgba.items()}

        # update
        self.local_db["RGBA"] = rgba


def floor_int(value):
    value = float(value)
    value = math.floor(value)
    return int(value)


def get_from_dictr(data_dict, map_list):
    return reduce(operator.getitem, map_list, data_dict)


def set_in_dict(data_dict, map_list, value):
    try:
        get_from_dictr(data_dict, map_list[:-1])[map_list[-1]] = value
    except KeyError:
        for k, v in value.items():
            get_from_dictr(data_dict, map_list[:-1])[k] = v
