from patterns import Patterns
from raspberrypi.pi_handler import PiHandler
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

# choose pattern, rate and color
pat = Patterns['Chasing']
rate = 10
color = RGB(random=True)

# init app and run
app = pat(handler=PiHandler, rate=rate, pixels=64, color=color)
app.run()
