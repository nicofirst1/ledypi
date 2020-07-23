import argparse

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
    parser.add_argument('--rate', type=int, help='rate', default=10)
    parser.add_argument('--pixels', type=int, help='rate', default=600)
    args = parser.parse_args()

    # choose pattern, rate and color
    pat = Patterns[args.pattern]
    color = RGB(random=True)

    # init app and run
    app = pat(handler=PiHandler, rate=args.rate, pixels=args.pixels, color=color)
    app.run()
