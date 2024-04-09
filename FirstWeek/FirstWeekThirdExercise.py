import time
from ssd1306 import SSD1306_I2C
from machine import UART, Pin, I2C

up = Pin(9,Pin.IN,Pin.PULL_UP)
down = Pin(7,Pin.IN,Pin.PULL_UP)
stop = Pin(8,Pin.IN,Pin.PULL_UP)
i2c = I2C(1, scl = Pin(15), sda = Pin(14), freq = 400_000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

x = 0
y = 31

oled.fill(0)
while True:
    while x < 127:
        if y > 0 and y < oled_height:
            print(x,y)
            oled.pixel(x, y, 1)
            oled.show()
            if up() == 0:
                y -= 1
            if down() == 0:
                y += 1
            if stop() == 0:
                oled.fill(0)
                time.sleep(1)
                break
        elif y <= 0:
            y = 1
            continue
        elif y >= 63:
            y = 63
            continue
        x += 1
    x = 0