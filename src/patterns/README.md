In this directory all the available patters will be stored.

## Adding a new pattern
To add a new patter you will need to create a new class which inherits from [Default](./src/patterns/default.py).

The new class has to have:
- `**kwargs` as only argument (check out the other classes).
- call to `super().__init__(**kwargs)` as the first line of the init
- implementation of the _fill_ method

### Pixels attribute
The pixel status is store in the pixel dictionary.
This dict has the following structure at initialization: `pixels:Dict[Dict]`.
The first dictionary maps an index (the pixel position) to another dictionary containing its attributes, at initialization the only attribute is:

`color:RGB.RGB`

which is a [RGB](./src/rgb.py) object. During the init or fill method you can add more attribute to each pixel as you see fit.

### Fill method
To change the values of the pixel, the fill method has to be implemented. This method will be called once every loop 
iteration to change the attributes of the pixels which will be then written wih the `set_pixels` method.

### Adding to init
To make the new pattern available to the database add it in the [init file](./src/patterns/__init__.py) as the value of the Pattern dictionary. 
