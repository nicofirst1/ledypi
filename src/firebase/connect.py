import argparse
import signal
import sys

from firebase.connector import FireBaseConnector


def connect(args):
    def signal_handler(signal, frame):
        fbc.close()
        # your code here
        sys.exit(0)

    # import the correct handler depending on the mode
    if args.mode == "pc":
        from DotStar_Emulator.emulator.send_test_data import App

        handler = App
        print("Running from PC")

    elif args.mode == "rpi":
        from rpi.pi_handler import PiHandler

        handler = PiHandler
        print("Running from RPI")

    else:
        raise ValueError(f"Mode '{args.mode}' is not supported")

    # init the firebase connector
    fbc = FireBaseConnector(credential_path=args.credential, database_url=args.databaseURL, handler=handler,
                            pixels=args.pixels, debug=args.debug)

    # add signal handler for interruption
    signal.signal(signal.SIGINT, signal_handler)

    # keep the thread alive
    try:
        while True:
            pass
    except KeyboardInterrupt:
        fbc.close()


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

    parser.add_argument('--debug', nargs='?',
                        help='If to start in debug mode')

    args = parser.parse_args()

    connect(args)
