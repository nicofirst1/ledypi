import math

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from patterns import Patterns
from rgb import RGB


class FireBaseConnector:

    def __init__(self, credential_path, database_url):
        # todo: use read file for certificate, url and init database
        cred = credentials.Certificate(credential_path)

        firebase_admin.initialize_app(credential=cred,
                                      options={'databaseURL': database_url})
        self.fb = db.reference('/')
        self.fb.listen(self.listener)

        self.rgba = None
        self.random_colors = False

        # update db with patterns
        self.fb.update(dict(patterns='.'.join(Patterns)))
        # get pattern,rate
        self.pattern_choice = self.get_cur_pattern()
        self.rate = self.get_rate()
        # update rgba
        self.update_rgba()

        # choose correct pattern and start it
        self.pattern = Patterns[self.pattern_choice](rate=self.rate, color=self.rgba)
        self.pattern.start()

    def listener(self, event):
        """
        Main listener, called when db is updated
        :param event: dict
        :return: None
        """
        print(event.event_type)  # can be 'put' or 'patch'
        print(event.path)  # relative to the reference, it seems
        print(event.data)  # new data at /reference/event.path. None if deleted
        print("#" * 20)

        # pass at the start
        if event.path == '/':
            pass

        # todo: add attr update for specific pattern
        # stop and restart pattern if required
        elif "cur_pattern" in event.path or "rate" in event.path:
            # get values
            self.pattern_choice = self.get_cur_pattern()
            self.rate = self.get_rate()
            # stop and restart
            self.pattern.stop()
            self.pattern = Patterns[self.pattern_choice](rate=self.rate)
            self.update_rgba()
            self.pattern.start()
            print(1)

        # update rgba
        elif "RGBA" in event.path:
            self.update_rgba()

        # update pattern attributes
        elif "pattern_attributes" in event.path:
            key = event.path.split("/")[-1]
            self.ps_attrs_getter(key, event.data)



        else:
            raise NotImplementedError(f"No such field for {event.path}")

    def ps_attrs_getter(self, key, data):
        """
        Converts and updates values from db
        :param key: str, name of db variable AND of class attribute
        :param data: str, data to convert
        :return:
        """

        # get the original type from the pattern
        t = type(self.pattern.__dict__[key])

        # convert it
        if t == float:
            data = float(data)
        elif t == int:
            data = floor_int(data)
        elif t == bool:
            data = data == "true"
        else:
            raise NotImplementedError(f"No data conversion implemented for key: '{key}' of type '{t}'")

        # update
        self.pattern.update_args(**{key: data})

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
        self.rgba = RGB(r=r, g=g, b=b, c=a)

        # extract random value and convert to bool
        random = rgba.get("random") == "true"

        # if method is called before pattern initialization skip
        try:
            # update pattern values
            self.pattern.update_args(randomize_color=random)
            self.pattern.update_args(color=self.rgba)
        except AttributeError:
            pass


def floor_int(value):
    value = float(value)
    value = math.floor(value)
    return int(value)
