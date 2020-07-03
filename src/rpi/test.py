import argparse

from patterns import Patterns
from rpi.pi_handler import PiHandler
from rgb import RGB

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
    parser.add_argument('-p', '--pattern', action='store_true', type=str, help='Pattern')
    parser.add_argument('-r', '--rate', action='store_true', type=int, help='rate')
    args = parser.parse_args()

    # choose pattern, rate and color
    pat = Patterns[args.pattern]
    rate = args.rate
    color = RGB(random=True)

    # init app and run
    app = pat(handler=PiHandler, rate=rate, pixels=300, color=color)
    app.run()
