import math
from firebase import firebase
import Fillers
from RGB import RGB


class FBC:

    def __init__(self):
        self.fb = firebase.FirebaseApplication('https://ledypie.firebaseio.com/', None)

        self.pattern_choice=None
        self.rgba=None
        self.rate=None
        self.init_vars()

        self.pattern=Fillers.Patterns[self.pattern_choice](self.rate)

        print(self.rate)
        print(self.rgba)
        print(self.pattern_choice)

    def init_vars(self):
        self.fb.put('','patterns','.'.join(Fillers.Patterns))
        self.pattern_choice=self.fb.get('', 'cur_pattern')
        self.rate=self.fb.get('','rate')
        self.get_rgba()

    def get_rgba(self):
        divisor="RGBA"
        r=self.fb.get(divisor,"r")
        g=self.fb.get(divisor,"g")
        b=self.fb.get(divisor,"b")
        a=self.fb.get(divisor,"a")

        r=floor_int(r)
        g=floor_int(g)
        b=floor_int(b)
        a=floor_int(a)

        self.rgba=RGB(r=r,g=g,b=b,c=a)

def floor_int(value):
    value=float(value)
    value=math.floor(value)
    return int(value)

fbc=FBC()