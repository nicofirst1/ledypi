from DotStar_Emulator.emulator.send_test_data import App

from patterns import Patterns
from utils.rgb import RGB

# choose pattern, rate and color
pat = Patterns['ColorMap']
rate = 1
color = RGB(random=True)

# init app and run
app = pat(handler=App(rate), rate=rate, pixels=64, color=color)
app.run()
