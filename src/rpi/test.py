import argparse

import yappi

from patterns import Patterns
from rgb import RGB
from rpi.pi_handler import PiHandler

# Available patterns are:
# ColorWipe
# Fading
# Fire
# FireWork
# Meteor
# Rainbow
# Snow
# Steady
# Strobe
# Chasing
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', type=str, help='Pattern')
    parser.add_argument('--rate', type=float, help='rate', default=0)
    parser.add_argument('--pixels', type=int, help='rate', default=300)
    parser.add_argument('--debug', nargs='?', const=True, default=False,
                        help='If to start in debug mode')
    args = parser.parse_args()
    _NTHREAD = 3

    # choose pattern, rate and color
    pat = Patterns[args.pattern]
    color = RGB(random=True)

    # init app and run
    app = pat(handler=PiHandler(args.pixels), rate=args.rate, pixels=args.pixels, color=color)

    if args.debug:
        yappi.start()

    try:
        app.run()
    except KeyboardInterrupt:
        pass

    if args.debug:

        yappi.stop()
        # retrieve thread stats by their thread id (given by yappi)
        threads = yappi.get_thread_stats()
        lines = []
        for thread in threads:
            print(
                "Function stats for (%s) (%d)" % (thread.name, thread.id)
            )  # it is the Thread.__class__.__name__
            yappi.get_func_stats(ctx_id=thread.id).print_all()
