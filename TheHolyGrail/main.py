import time
from ssd1306 import SSD1306_I2C
from machine import UART, Pin, I2C, ADC
from filefifo import Filefifo
from fifo import Fifo
from led import Led 
#import extraction


sensor = ADC(Pin(26))
while True:
    adc_value = sensor.read_u16()
    print(adc_value)