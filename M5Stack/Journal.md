clone [repo](https://github.com/m5stack/M5Stack_MicroPython)

## Using standrd micropython
- flash software as mentioned in [here](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html)
    - `esptool.py --port /dev/ttyUSB0 erase_flash`
    - `esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 esp32-20180511-v1.9.4.bin`
- start serial prompt with `picocom /dev/ttyUSB0 -b115200`
- tutorial for leds
  [here](https://randomnerdtutorials.com/micropython-ws2812b-addressable-rgb-leds-neopixel-esp32-esp8266/)