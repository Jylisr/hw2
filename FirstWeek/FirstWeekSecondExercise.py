from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C
import time
import framebuf

sw2 = Pin(7, Pin.IN, Pin.PULL_UP)
sw0 = Pin(9, Pin.IN, Pin.PULL_UP)
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
character_width = 8
text_height = 8
oled = SSD1306_I2C(oled_width, oled_height, i2c)

x = 0
y = 0
while True:
    if y == 64:
        oled.scroll(0, -text_height)
        y = 56
        oled.rect(x, y, oled_width, character_height, 0,[True])
    text = input('enter text')
    oled.text(text,x,y,1)
    y = y + 8
    oled.show()