import os
import sys


dir_path = os.path.dirname(os.path.realpath(__file__))
root = dir_path.split("ledypi")[0] + "ledypi"

paths = [f"{root}/DotStar_Emulator", f"{root}/src"]
sys.path += paths


from DotStar_Emulator.emulator import EmulatorApp

app = EmulatorApp()
app.run()
