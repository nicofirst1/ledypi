import logging
import time

from firebase.connector import FireBaseConnector, floor_int
from patterns import Patterns

fire_logger = logging.getLogger("fire_logger")

# since the firebase updater will call the listener a lot
# during the slider value change, we need a way to skip too frequent updates.
# with the frequency function the call to the listener will be
# skipped if there was a previous call less than '__call_resolution' seconds before

__last_call = time.time()
__call_resolution = 0.1


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

        super().__init__(credential_path=credential_path, database_url=database_url, debug=debug)
        # add listener to firebase
        self.listener = self.fb.listen(self.listener)
        # update rgba
        self.update_rgba()

        self.handler = handler
        self.pixels = pixels

        # choose correct pattern and start it
        self.pattern = Patterns[self.pattern_choice](rate=self.rate, color=self.rgba, handler=handler, pixels=pixels)
        self.pattern.start()

    def close(self):
        super().close()
        self.pattern.stop()
        self.listener.close()

    @frequency
    def listener(self, event):
        """
        Main listener, called when db is updated
        :param event: dict
        :return: None
        """

        to_log = f"{event.event_type}\n{event.path}\n{event.data}"
        fire_logger.debug(to_log)

        if "rate" in event.path:
            rate = self.get_rate(data=event.data)
            self.pattern.set_rate(rate)
            self.rate = rate

        # stop and restart pattern if required
        elif "cur_pattern" in event.path:
            # get values
            self.pattern_choice = self.get_cur_pattern()
            self.rate = self.get_rate()
            # stop and restart
            self.pattern.stop()
            self.pattern = Patterns[self.pattern_choice](rate=self.rate, handler=self.handler, pixels=self.pixels)
            self.update_rgba()
            self.pattern.start()

        # update rgba
        elif "RGBA" in event.path:
            self.update_rgba()

        # update pattern attributes
        elif "pattern_attributes" in event.path:
            key = event.path.split("/")[-1]
            self.ps_attrs_getter(key, event.data)

        elif event.path != '/':
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

    def update_rgba(self):
        """
        Update RGBA values taking them from the database
        :return:
        """
        super(FireBaseController, self).update_rgba()
        # if method is called before pattern initialization skip
        try:
            # update pattern values
            self.pattern.update_args(randomize_color=self.random_colors)
            self.pattern.update_args(color=self.rgba)
        except AttributeError:
            pass
