In this directory all the available patters will be stored.

# Adding a new pattern
To add a new patter you will need to create a new class which inherits from [Default](default.py).

The new class has to have:
- `**kwargs` as only argument (check out the other classes).
- call to `super().__init__(**kwargs)` as the first line of the init
- implementation of the _fill_ method

## Pixels attribute
The pixel status is store in the pixel dictionary.
This dict has the following structure at initialization: `pixels:Dict[Dict]`.
The first dictionary maps an index (the pixel position) to another dictionary containing its attributes, at initialization the only attribute is:

`color:RGB.RGB`

which is a [RGB](/src/rgb.py) object. During the init or fill method you can add more attribute to each pixel as you see fit.

## Fill method
To change the values of the pixel, the fill method has to be implemented. This method will be called once every loop 
iteration to change the attributes of the pixels which will be then written wih the `set_pixels` method.

## Adding to init
To make the new pattern available to the database add it in the [init file](__init__.py) as the value of the Pattern dictionary. 


## Modifiers
Each pattern inherit a dictionary called _modifiers_  which should be populated with instances from the [Modifier class](utils/modifier.py).

This class accepts two mandatory attributes and 3 (as for now) optional ones:
- __name__: str, the name which will be shown in the web/android app.
- __value__: the initial value.
- __min/max__: by default, if the value is an int/float, it will be scaled at setting time to be in range [min,max].
- __choices__: for multi-choice options, provide a list of allowed values. 

It is fundamental that the key in the _modifiers_ dict and the instance name are the same for the app to correctly identify them.
For example the pattern Fire shows:

```python
class Fire(Default):
    """
    Fire pattern
    """

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.cooling = Modifier('cooling', 10, minimum=1, maximum=self.strip_length)
        self.sparking = Modifier('sparking', 40, minimum=1, maximum=255)
        self.cooldown_list = [0 for _ in range(self.strip_length)]
        self.pattern_name = "Fire"
        self.mid = self.strip_length // 2

        self.modifiers = dict(
            cooling=self.cooling,
            sparking=self.sparking
        )

```

Notice how the modifiers names "self.cooling" and "self.sparking" are the same as they appear in the dictionary keys.

Since _Modifier_ is a custom class you need to access it's value with a call function, e.g. `self.cooling()` and set it with: `self.cooling.value=1`


### Properties
Some time you want to have some rule to set an attribute before actually setting it. In this case you would normally use a `@proprety` and wrap it with your custom function. 

To allow the same thing with the _modifiers_ dictionary take a look at the following simplified example of the Equation Pattern:

```python



class Equation(Default):
    """
    Use user-defined function for the rgb values. The function may depend on :
        - the pixel position in the led strip 'idx'
        - the current timestep 't' which cycles in a predefined allowed range.
        - both
        - none
    """

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.pattern_name = "Equation"

        self.fns = {}

        # modifier named after the hidden variable for red_equation
        self._r_eq = Modifier('red equation', "cos(t)")
        
        # the main attribute with it's default value
        self.red_equation = "cos(t)"
            
        self.modifiers = dict(
            # a map between the main attribute name and the hidden variable value
            red_equation=self._r_eq,

        )

    @property
    def red_equation(self):
        # returning the value of the hidden variable
        return self._r_eq()

    @red_equation.setter
    def red_equation(self, value):
        # change the red equation in the fns dict and then assing the modifiers with its new value
        self.fns['r_fn'] = Expression(value, ["t", "idx"])
        self._r_eq.value = value

```

As you can see from the init function, the modifier instance name is the hidden value of the red_equation.
 By keeping the _modifiers_ key the same as the main attribute "red_equation" you can process the hidden variable "_r_eq" 
 as you like.























