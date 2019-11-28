import math

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import Fillers
from RGB import RGB


class FBC:

    def __init__(self):
        #todo: use read file for certificate, url and init database
        cred = credentials.Certificate("/Users/giulia/Desktop/ledypie/FireBase/firebase_key.json")

        firebase_admin.initialize_app(credential=cred,
                                      options={'databaseURL': 'https://ledypie.firebaseio.com/'})
        self.fb = db.reference('/')
        self.fb.listen(self.listener)

        self.pattern_choice = None
        self.rgba = None
        self.delay = None
        self.random_colors = False
        self.update_vars()

        self.pattern = Fillers.Patterns[self.pattern_choice](delay=self.delay,color=self.rgba)
        self.pattern.start()

    def listener(self, event):
        print(event.event_type)  # can be 'put' or 'patch'
        print(event.path)  # relative to the reference, it seems
        print(event.data)  # new data at /reference/event.path. None if deleted
        print("#" * 20)

        if event.path == '/':
            pass

        elif "cur_pattern" in event.path:
            self.pattern_choice = self.get_cur_pattern(data=event.data)
            self.pattern.stop()
            self.pattern = Fillers.Patterns[self.pattern_choice](delay=self.delay)
            self.update_rgba()
            self.pattern.start()
            print(1)

        elif "rate" in event.path:
            self.delay = self.get_rate(data=event.data)
            self.pattern.stop()
            self.pattern = Fillers.Patterns[self.pattern_choice](delay=self.delay)
            self.update_rgba()
            self.pattern.start()


        elif "RGBA" in event.path:
            self.update_rgba()


        elif "pattern_attributes" in event.path:
            key = event.path.split("/")[-1]
            self.ps_attrs_getter(key, event.data)



        else:
            raise NotImplementedError(f"No such field for {event.path}")

    def ps_attrs_getter(self, key, data):

        # get the original type from the pattern
        t=type(self.pattern.__dict__[key])

        # convert it
        if t==float:
            data=float(data)
        elif t==int:
            data=floor_int(data)
        else:
            raise NotImplementedError(f"No data conversion implemented for key: '{key}' of type '{t}'")

        # update
        self.pattern.update_args(**{key:data})


    def get(self, key, default=None):
        gets = self.fb.get()

        if key in gets.keys():
            return gets[key]

        return default

    def update_vars(self):
        self.fb.update(dict(patterns='.'.join(Fillers.Patterns)))
        self.pattern_choice = self.get_cur_pattern()
        self.delay = self.get_rate()
        self.update_rgba()

    def get_rate(self, data=None):
        if data is None:
            data = self.get('rate')

        return floor_int(data)

    def get_cur_pattern(self, data=None):
        if data is None:
            data = self.get('cur_pattern')

        return data.replace('"', '')

    def update_rgba(self):
        rgba = self.get("RGBA")

        random = rgba.get("random") == "true"



        r = rgba.get("r")
        g = rgba.get("g")
        b = rgba.get("b")
        a = rgba.get("a")

        r = floor_int(r)
        g = floor_int(g)
        b = floor_int(b)
        a = floor_int(a)

        self.rgba = RGB(r=r, g=g, b=b, c=a)

        # if method is called before pattern initialization skip
        try:
            self.pattern.update_args(randomize_color=random)
            self.pattern.update_args(color=self.rgba)

        except AttributeError:
            pass


def floor_int(value):
    value = float(value)
    value = math.floor(value)
    return int(value)


if __name__ == '__main__':
    fbc = FBC()
