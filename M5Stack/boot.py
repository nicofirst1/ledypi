# This file is executed on every boot (including wake-boot from deepsleep)
import sys
from m5stack import lcd


sys.path[1] = '/flash/lib'
lcd.print('hello world!')
