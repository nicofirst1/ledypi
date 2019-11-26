import firebase_admin
import math
from firebase_admin import credentials
from firebase_admin import db

import Fillers
from RGB import RGB


class FBC:

    def __init__(self):
        cred = credentials.Certificate("/Users/giulia/Desktop/ledypie/FireBase/firebase_key.json")

        firebase_admin.initialize_app(credential=cred,
                                      options={'databaseURL': 'https://ledypie.firebaseio.com/'})
        self.fb = db.reference('/')
        self.fb.listen(self.listener)

        self.pattern_choice = None
        self.rgba = None
        self.rate = None
        self.init_vars()

        self.pattern = Fillers.Patterns[self.pattern_choice](self.rate)
        self.pattern.run()

    def listener(self,event):
        print(event.event_type)  # can be 'put' or 'patch'
        print(event.path)  # relative to the reference, it seems
        print(event.data)  # new data at /reference/event.path. None if deleted

        if "cur_pattern" in event.path:

            self.pattern_choice=self.get_cur_pattern(data=event.data)
            self.pattern.stop()
            self.pattern = Fillers.Patterns[self.pattern_choice](self.rate)
            self.pattern.run()



    def get(self,key,default=None):
        gets=self.fb.get()

        if key in gets.keys():
            return gets[key]

        return default

    def init_vars(self):
        self.fb.update(dict(patterns='.'.join(Fillers.Patterns)))
        self.pattern_choice = self.get_cur_pattern()
        self.rate = floor_int(self.get('rate'))
        self.get_rgba()

    def get_cur_pattern(self,data=None):
        if data is None:
            data= self.get('cur_pattern')

        return data.replace('"','')

    def get_rgba(self):
        rgba=self.get("RGBA")
        r =rgba.get( "r")
        g = rgba.get( "g")
        b = rgba.get( "b")
        a = rgba.get( "a")

        r = floor_int(r)
        g = floor_int(g)
        b = floor_int(b)
        a = floor_int(a)

        self.rgba = RGB(r=r, g=g, b=b, c=a)


def floor_int(value):
    value = float(value)
    value = math.floor(value)
    return int(value)


fbc = FBC()
