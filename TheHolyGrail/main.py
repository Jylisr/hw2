import time
from ssd1306 import SSD1306_I2C
from machine import UART, Pin, I2C, ADC
from filefifo import Filefifo
from fifo import Fifo
from led import Led 
#import extraction


data_list = []
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
x = 0
y = 0
oled_width = 128
oled_height = 64
character_width = 8
text_height = 8
oled = SSD1306_I2C(oled_width, oled_height, i2c)
sensor = ADC(Pin(26))
while True:
    adc_value = sensor.read_u16()
    print(adc_value)