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
        self.random_colors=False
        self.update_vars()

        self.pattern = Fillers.Patterns[self.pattern_choice](self.rate)
        self.update_args()
        self.pattern.run()

    def listener(self,event):
        print(event.event_type)  # can be 'put' or 'patch'
        print(event.path)  # relative to the reference, it seems
        print(event.data)  # new data at /reference/event.path. None if deleted
        print("#"*20)

        if event.path=='/':
            pass

        elif "cur_pattern" in event.path :
            self.pattern_choice=self.get_cur_pattern(data=event.data)
            self.pattern.stop()
            self.pattern = Fillers.Patterns[self.pattern_choice](self.rate)
            self.update_args()
            self.pattern.run()

        elif "rate" in event.path:
            self.rate = self.get_rate(data=event.data)
            self.pattern.stop()
            self.pattern = Fillers.Patterns[self.pattern_choice](self.rate)
            self.update_args()
            self.pattern.run()


        elif "RGBA" in event.path:
            self.update_rgba()
            changed=self.pattern.update_args(color=self.rgba)
            changed = self.pattern.update_args(random_colors=self.random_colors)

        elif "pattern_attributes" in event.path:
            key=event.path.split("/")[-1]
            if "rainbow" in event.path:
                self.rainbow_getter(key,data=event.data)
            elif 'fading' in event.path:
                self.fading_getter(data=event.data)

        else:
            raise NotImplementedError(f"No such field for {event.path}")


    def fading_getter(self, key,data=None):
        
        # get the data
        if data is None:
            data=self.get("pattern_attributes").get('fading').get('key')

        # get every attribute
        if key == "point_number":
            self.pattern.update_args(point_number=data)
        elif key == "rate_start":
            self.pattern.update_args(rate_start=data)
        elif key == "rate_end":
            self.pattern.update_args(rate_end=data)
        elif key == "random_color":
            self.pattern.update_args(random_color=data)

        else:
            raise NotImplementedError(f"No such field for {key} in faiding getter")


    def rainbow_getter(self, key, data=None):
        # get the data
        if data is None:
            data=self.get("pattern_attributes").get('rainbow').get(key)

        data=floor_int(data)
        
        # get every attribute
        if key=="max_range":
            self.pattern.update_args(max_range=data)
        elif key=="b_phi":
            self.pattern.update_args( b_phi=data)
        elif key=="g_phi":
            self.pattern.update_args( g_phi=data)
        elif key == "r_phi":
            self.pattern.update_args(r_phi=data)

        else:
            raise NotImplementedError(f"No such field for {key} in rainbow getter")

    def fireworks_getter(self, data=None):
        # get the data
        if data is None:
            data=self.get("pattern_attributes").get('fireworks')
        
        # get every attribute
        num_fires=data.get('num_fires')
        

        # update in class
        self.pattern.update_args(fires=num_fires)

        
        

    def update_args(self):
        changed = self.pattern.update_args(color=self.rgba)
        changed = self.pattern.update_args(random_colors=self.random_colors)


    def get(self,key,default=None):
            gets=self.fb.get()

            if key in gets.keys():
                return gets[key]

            return default

    def update_vars(self):
        self.fb.update(dict(patterns='.'.join(Fillers.Patterns)))
        self.pattern_choice = self.get_cur_pattern()
        self.rate = self.get_rate()
        self.update_rgba()

    def get_rate(self,data=None):
        if data is None:
            data=self.get('rate')

        return floor_int(data)

    def get_cur_pattern(self,data=None):
        if data is None:
            data= self.get('cur_pattern')

        return data.replace('"','')

    def update_rgba(self):
        rgba=self.get("RGBA")

        random=rgba.get("random")

        if not random:

            r =rgba.get( "r")
            g = rgba.get( "g")
            b = rgba.get( "b")
            a = rgba.get( "a")

            r = floor_int(r)
            g = floor_int(g)
            b = floor_int(b)
            a = floor_int(a)

            self.rgba = RGB(r=r, g=g, b=b, c=a)
        else:
            self.rgba=RGB(random=True)
            self.random_colors=True
            try:
                self.pattern.update_args(random=True)
            except AttributeError:
                # skip if pattern has not been initialized yet
                pass


def floor_int(value):
    value = float(value)
    value = math.floor(value)
    return int(value)


fbc = FBC()
