from Patterns import Patterns, ColorWipe

from RGB import RGB

pat= Patterns['Chasing']
rate=10
color=RGB(white=True)
config=dict(rate=rate, color=color)
app= pat(rate=rate, color=color)
app.run()
