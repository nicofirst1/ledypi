from Patterns import Patterns, ColorWipe

from RGB import RGB

pat= Patterns['Fading']
rate=10
color=RGB(white=True)
config=dict(rate=rate, color=color)
app= pat(config)
app.run()
