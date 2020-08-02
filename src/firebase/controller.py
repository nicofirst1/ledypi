import logging
import time

from firebase.connector import FireBaseConnector
from patterns import Patterns
from rgb import RGB

fire_logger = logging.getLogger("fire_logger")

# since the firebase updater will call the listener a lot
# during the slider value change, we need a way to skip too frequent updates.
# with the frequency function the call to the listener will be
# skipped if there was a previous call less than '__call_resolution' seconds before

__last_call = time.time()
__call_resolution = 0.01


def frequency(listener):
    """
    Decoratorr to skip call to the firebase listener
    :param listener:
    :return:
    """

    def wrap(*args):
        # get the global time of the last call
        global __last_call
        # check that the last call was made after tot secs
        if time.time() - __last_call > __call_resolution:
            # if yes call the listener and update time
            ret = listener(*args)
            __last_call = time.time()
            return ret
        # else skip

    return wrap


class FireBaseController(FireBaseConnector):
    """
    Controller for the firebase databse.
    Extends the FireBaseConnector to allow modification of the pixels in both pc or rpi mode
    """

    def __init__(self, credential_path, database_url, handler, pixels, debug=None):

        # dummy pattern to avoid exception
        self.pattern = Patterns['Steady'](rate=10,handler=handler, pixels=pixels)

        super().__init__(credential_path=credential_path, database_url=database_url, debug=debug)


        self.handler = handler
        self.pixels = pixels

        # choose correct pattern and start it
        cur_pattern=self.get_cur_pattern()
        rate=self.get_rate()
        rgba=self.get_rgba()
        self.pattern = Patterns[cur_pattern](rate=rate, color=rgba, handler=handler, pixels=pixels)
        self.pattern.start()


    def close(self):
        super().close()
        self.pattern.stop()
        self.listener.close()

    @frequency
    def listener_method(self, event):
        """
        Main listener, called when db is updated
        :param event: dict
        :return: None
        """

        super(FireBaseController, self).listener_method(event)

        to_log = f"{event.event_type}\n{event.path}\n{event.data}"
        fire_logger.debug(to_log)

        k=event.data.keys()
        k=list(k)

        if "rate" in k:
            rate = self.get_rate(data=event.data)
            self.pattern.set_rate(rate)
            self.rate = rate

        # stop and restart pattern if required
        elif "cur_pattern" in k:
            # get values
            pattern_choice = self.get_cur_pattern()
            rate = self.get_rate()
            rgba= self.get_rgba()
            # stop and restart
            self.pattern.stop()
            self.pattern = Patterns[pattern_choice](rate=rate, color=rgba, handler=self.handler, pixels=self.pixels)
            self.pattern.start()

        # update rgba
        elif "RGBA" in k:
            self.floor_rgba(event.data)

        # update pattern attributes
        elif "pattern_attributes" in event.path:
            self.ps_attrs_getter(event.data)

        else:
            raise NotImplementedError(f"No such field for {event.path}")

    def ps_attrs_getter(self, data):
        """
        Converts and updates values from db
        :param key: str, name of db variable AND of class attribute
        :param data: str, data to convert
        :return:
        """

        # check that the values to modify are indeed of the current pattern
        pattern= next(iter(data))
        assert self.pattern.pattern_name == pattern
        # remove pattern name
        data=data[pattern]
        # and update pattern
        self.pattern.update_args(**data)

    def floor_rgba(self, data):
        """
        Update RGBA values taking them from the database
        :return:
        """

        def init_rgba(rgba):
            r = rgba['r']
            g = rgba['g']
            b = rgba['b']
            a = rgba['a']

            r = int(r)
            g = int(g)
            b = int(b)
            a = int(a)

            return RGB(r=r,g=g,b=b,a=a)

        # if method is called before pattern initialization skip
        try:
            # update pattern values
            random= data["RGBA"]['random']
            rgba=init_rgba(data["RGBA"])
            self.pattern.update_args(randomize_color=bool(random))
            self.pattern.update_args(color=rgba)
        except AttributeError:
            pass
