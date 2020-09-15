import argparse
import logging
import signal

from firebase import fire_logger
from firebase.controller import FireBaseController
from src import change_level


def control(args):
    def signal_handler(signal, frame):
        fbc.close()

    # import the correct handler depending on the mode
    if args.mode == "pc":
        from DotStar_Emulator.emulator.send_test_data import App

        handler = App
        args.pixels = 64
        print("Running from PC")

    elif args.mode == "rpi":
        if args.strip_type == "neopixel":
            from rpi import NeoPixel

            handler = NeoPixel
        else:
            from rpi import Dotstar

            handler = Dotstar

        print(f"Running from RPI with {handler.__class__} stripe")

    else:
        raise ValueError(f"Mode '{args.mode}' is not supported")

    if args.debug:
        change_level(logging.DEBUG)
        fire_logger.debug("Logging level debug")
    else:
        change_level(logging.INFO)

    # init the firebase connector
    fbc = FireBaseController(credential_path=args.credential, database_url=args.databaseURL, handler=handler,
                             pixels=args.pixels, debug=args.debug)
    fbc.start()

    # add signal handler for interruption
    signal.signal(signal.SIGINT, signal_handler)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse private key json file.')
    parser.add_argument('credential', type=str,
                        help='The path to the private key json file for Firebase')
    parser.add_argument('mode', type=str,
                        help='Where are you running the script, either pc or rpi',
                        choices=["pc", "rpi"],
                        )
    parser.add_argument('--databaseURL', type=str, nargs='?', default="https://ledypie.firebaseio.com/",
                        help='The Firebase database url')
    parser.add_argument('--pixels', type=int, nargs='?', default="300",
                        help='Number of pixels')
    parser.add_argument('--strip_type', type=str, help='Type of the strip', default='neopixel',
                        choices=['neopixel', 'dotstar'], )

    parser.add_argument('--debug', nargs='?', const=True,
                        help='If to start in debug mode')

    args = parser.parse_args()

    control(args)
