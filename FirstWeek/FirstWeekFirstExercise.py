import time
from ssd1306 import SSD1306_I2C
from machine import UART, Pin, I2C

right = Pin(9,Pin.IN,Pin.PULL_UP)
left = Pin(7,Pin.IN,Pin.PULL_UP)
i2c = I2C(1, scl = Pin(15), sda = Pin(14), freq = 400_000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

class UFO:
    def __init__(self,text_width = 8, text_height = 8, ufo = "<=>"):
        self.ufo = ufo
        self.text_height = text_height
        self.text_width = text_width
        self.text_x = oled_height - text_height
        self.text_y = int((oled_width/2) - (text_width * (len(ufo)/2)))
        self.left_end = int((oled_width) - (text_width * (len(ufo))))
        print(self.left_end)
        
    def spawn_ufo(self):
        oled.fill(0)
        oled.text(self.ufo, self.text_x, self.text_y, 1)
        oled.show()
    
    def right(self):
        if self.text_x + 1 < self.left_end:
            self.text_x += 1
            oled.fill(0)
            oled.text(self.ufo, self.text_x, self.text_y, 1)
            oled.show()
        
    def left(self):
        if self.text_x - 1 > 0:
            self.text_x -= 1
            oled.fill(0)
            oled.text(self.ufo, self.text_x, self.text_y, 1)
            oled.show()

ufo = UFO()
ufo.spawn_ufo()
while True:
    while right() and left() == 1:
        time.sleep(0.05)
    
    if right() == 0:
        ufo.right()

    if left() == 0:
        ufo.left()
    
    else:
        pass