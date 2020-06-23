from patterns import Patterns

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
app = pat(rate=rate, color=color)
app.run()
