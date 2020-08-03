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
from rgb import RGB

fire_logger = logging.getLogger("fire_logger")


class FireBaseConnector(Thread):
    """
    Firebase connecting class.
    Allows for the modification of the pattern and attributes
    """

    def __init__(self, credential_path, database_url="https://ledypie.firebaseio.com/", debug=False, tracker=None):
        """
        :param credential_path: str, path to the firebase credential json file
        :param database_url: str, URL of the firebase
        :param debug: bool, set to true to allow debug output
        :param tracker: func, function to be called when the database has been updated with new values
        """

        # init thread class
        super().__init__(name="FireBaseConnectorThread")

        # define local attributes
        self.tracker = tracker if tracker is not None else lambda: None
        self.stop = False
        self.rgba = None
        self.random_colors = False
        self.local_db = None

        if debug:
            fire_logger.setLevel(logging.DEBUG)

        # connect to firebase
        cred = credentials.Certificate(credential_path)
        firebase_admin.initialize_app(credential=cred,
                                      options={'databaseURL': database_url})

        # update db and get references
        self.root = db.reference('/')
        self.init_db()
        self.pattern_attributes = db.reference('/pattern_attributes')

        # add listener and sleep to wait for the first call where self.local_db is initialized
        self.listener = self.root.listen(self.listener_method)
        time.sleep(1)

    def listener_method(self, event):
        """
        Update the local db on every change
        :param event:
        :return:
        """

        # if the local db has not been initialized yet, do it
        if self.local_db is None:
            self.local_db = event.data
            return False

        if event.event_type == "patch": return

        # get all the keys, remove empty
        keys = event.path.split("/")
        keys.pop(0)

        # check if there is a difference
        if get_from_dict(self.local_db, keys) != event.data:
            # update local db
            set_in_dict(self.local_db, keys, event.data)
            self.tracker()

        return True

    def run(self) -> None:
        """
        Run the firebasa connection in a separate thread
        :return:
        """

        try:
            while not self.stop:
                pass
        except KeyboardInterrupt:
            fire_logger.info("FireBaseConnector has been interrupted")
            self.close()

    def close(self):
        fire_logger.info("Closing firebase connection, this make take a few seconds...")
        self.listener.close()
        self.stop = True
        fire_logger.info("Firebase connection closed")

    def update_db(self, request):
        """
        Check the differences between the request and the local db, if there are then update local and remote db
        :param request: dict, current values
        :return: None
        """

        def pattern():
            """
            Check differences on the current pattern
            :return:
            """
            # check for pattern difference
            rq_pattern = request.get("cur_pattern")
            if not rq_pattern == "" and rq_pattern != self.local_db.get("cur_pattern"):
                # if yes update both local and remote
                self.root.update(dict(cur_pattern=rq_pattern))
                self.local_db["cur_pattern"] = rq_pattern

        def rate():
            """
            Check differences on the rate
            :return:
            """

            # check for rate difference
            rq_rate = request.get("rate")
            rq_rate = int(rq_rate)
            if rq_rate != self.local_db.get("rate"):
                # if yes update both local and remote
                self.root.update(dict(rate=rq_rate))
                self.local_db["rate"] = rq_rate

        def rgba():
            """
            Check differences on the rgba
            :return:
            """
            # map random switch from on/missing to true/false
            if request['random'] == "true":
                request['random'] = True
            else:
                request['random'] = False

            # check for rgba difference
            to_update = {}
            for k, v in self.local_db['RGBA'].items():
                rq = request.get(k)
                if isinstance(rq, bool):
                    rq = bool(rq)
                else:
                    rq = int(request.get(k))
                if v != rq:
                    to_update[k] = rq

            if len(to_update) > 0:
                to_update = update_dict_no_override(self.local_db['RGBA'], to_update)
                self.root.update(dict(RGBA=to_update))
                self.local_db["RGBA"] = to_update

        def pattern_attributes():
            """
            Check differences on the pattern attributes
            :return:
            """
            # update pattern attributes
            to_update = {}
            rq_pattern = request.get("cur_pattern")

            if self.local_db['pattern_attributes'][rq_pattern] == "NA": return

            for mod_name, modifier in self.local_db['pattern_attributes'][rq_pattern].items():

                # get the attributes
                tp = eval(modifier['type'])
                value = modifier['value']
                name = modifier['name']

                try:
                    # cast to correct type
                    if tp == bool:
                        request[mod_name] = request[name] == 'true'
                    elif tp == int:
                        request[mod_name] = int(request[name])
                    elif tp == float:
                        request[mod_name] = float(request[name])
                    elif tp==list or tp ==str:
                        request[mod_name] = str(request[name])

                    else:
                        fire_logger.info(f"Type {tp} not recognized for modifier {name} ({mod_name})")

                    # check if to update
                    if request[mod_name] != value:
                        to_update[mod_name] = modifier
                        to_update[mod_name]['value'] = request[mod_name]

                except KeyError:
                    continue

            # if there is something to update
            if len(to_update) > 0:
                # add missing (not to update) elements to the update dict
                to_update = update_dict_no_override(self.local_db['pattern_attributes'][rq_pattern], to_update)
                # send update both remotely and locally
                self.pattern_attributes.update({rq_pattern: to_update})
                self.local_db["pattern_attributes"][rq_pattern] = to_update

        # check the differences for the following entries
        pattern()
        rate()
        rgba()
        pattern_attributes()

    def init_db(self):
        """
        Initialize all the components of the database if not present
        :return:
        """

        def init_other():
            """
            Add rate, cur_pattern and patterns to the database if not present
            :return:
            """

            to_update = {}
            # check rate
            val = self.get("rate", None)
            if val is None:
                to_update['rate'] = 10

            # check cur_pattern
            val = self.get("cur_pattern", None)
            if val is None:
                to_update['cur_pattern'] = "Steady"

            if len(to_update) > 0:
                self.root.update(to_update)

        def init_rgba():
            """
            Add RGBA to the database if not present
            :return:
            """

            data = self.get("RGBA", {})

            # define standard RGBA components
            RGBA = dict(r=255, g=255, b=255, a=100, random=0)

            to_update = {}
            for k, v in RGBA.items():
                # try to check if the value is updated
                try:
                    if data[k] != v:
                        to_update[k] = data[k]
                except KeyError:
                    to_update[k] = v

            # if there are updates push them
            if len(to_update) > 0:
                to_update = update_dict_no_override(RGBA, to_update)
                self.root.update(dict(RGBA=to_update))

        def init_pattern_attributes():
            """
            Add all the attributes from the default modifier dictionary to the remote database
            """
            # get the attributes from the remote
            data = self.get("pattern_attributes", {})

            pattern_attributes = {}

            # for every pattern in the pattern dict
            for pt_name, pt_class in Patterns.items():

                remote_att = {}
                # get the local modifier dictionary
                local_att = pt_class(handler=None, rate=1, pixels=1).modifiers

                # if there are none, then set to NA
                if len(local_att) == 0:
                    pattern_attributes[pt_name] = "NA"
                    continue

                # get the remote attributes
                try:
                    remote_att = data[pt_name]
                except KeyError:
                    if len(local_att) > 0:
                        fire_logger.warning(f"Patter '{pt_name}' not found in pattern dict")

                pattern_attributes[pt_name] = {}

                # for every attribute
                for att_name, modifier in local_att.items():

                    # generate a dictionary with the corresponding values
                    att_dict = dict(
                        value=modifier.value,
                        name=modifier.name,
                        type=modifier.type.__name__
                    )
                    if modifier.type == list:
                        att_dict['options'] = modifier.options

                    # try to override the default value with the one from the db
                    try:
                        att_dict['value'] = remote_att[att_name]['value']
                    except (TypeError, KeyError):
                        pass
                    # set the value
                    pattern_attributes[pt_name][att_name] = att_dict

            # update the database
            self.root.update(dict(pattern_attributes=pattern_attributes))

            return pattern_attributes

        init_other()
        init_rgba()
        init_pattern_attributes()

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
        else:
            data = data['rate']

        return floor_int(data)

    def get_rgba(self, data=None):
        """
        Return rgb class from the database
        :param data: dict, optional database
        :return: RGB class
        """

        if data is None:
            data = self.get("RGBA")

        return RGB(r=data["r"], g=data['g'], b=data['b'], a=data['a'], random=data['random'])

    def get_cur_pattern(self, data=None):
        """
        Manipulate cur_pattern output from db
        :param data: str, data from db, optional, will be loaded if None
        :return: str, Usable data
        """
        if data is None:
            data = self.get('cur_pattern')

        return data.replace('"', '')


def floor_int(value):
    value = float(value)
    value = math.floor(value)
    return int(value)


def get_from_dict(data_dict, map_list):
    return reduce(operator.getitem, map_list, data_dict)


def set_in_dict(data_dict, map_list, value):
    try:
        get_from_dict(data_dict, map_list[:-1])[map_list[-1]] = value
    except KeyError:
        for k, v in value.items():
            get_from_dict(data_dict, map_list[:-1])[k] = v


def update_dict_no_override(additional_dict, base_dict):
    """
    Update the base dict with the new pairs from additional_dict. If there are some same keys then keep the ones on base_dict
    """
    return dict(list(additional_dict.items()) + list(base_dict.items()))


if __name__ == '__main__':
    # init the firebase connector
    fbc = FireBaseConnector(credential_path="./credential.json", debug=True)
    fbc.start()
