import time
from ssd1306 import SSD1306_I2C
from machine import UART, Pin, I2C
from filefifo import Filefifo
from fifo import Fifo



data = Filefifo(10, name = "capture_250Hz_01.txt")
data_list = []
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
x = 0
y = 0
oled_width = 128
oled_height = 64
character_width = 8
text_height = 8
oled = SSD1306_I2C(oled_width, oled_height, i2c)


class Encoder:
    def __init__(self, rot_a, rot_b):
        self.a = Pin(rot_a, mode = Pin.IN, pull = Pin.PULL_UP)
        self.b = Pin(rot_b, mode = Pin.IN, pull = Pin.PULL_UP)
        self.fifo = Fifo(30, typecode = 'i')
        self.a.irq(handler = self.handler, trigger = Pin.IRQ_RISING, hard = True)
        
    def handler(self, pin):
        if not self.b():
            self.fifo.put(+1)
        else:
            self.fifo.put(-1)
            
rot = Encoder(10,11)


for _ in range(1000):
    sample = data.get()
    data_list.append(sample)

min,max = min(data_list),max(data_list)

scaler = (max - min)/(64 - 0)
shifter1 = min/scaler - 0
shifter2 = max/scaler - 64
print("Min :",min,"Max :", max)

for i in range(128):
    draw = data_list[i]/scaler - shifter1
    draw = int(draw)
    oled.pixel(i, draw, 1)
    print(i, draw, 1)
oled.show()
start = 128

while True:
    if rot.fifo.has_data():
        value = rot.fifo.get()
        if value == +1:
            x = oled_width - 1
            oled.scroll(-1,0)
            oled.vline(oled_width - 1,0,oled_height,0)
            start += value
            draw = data_list[start]/scaler - shifter1
            y = int(draw)
            oled.pixel(x, y, 1)
            print(x, y)
        elif value == -1:
            x = 1
            oled.scroll(1,0)
            oled.vline(0,0,oled_height,0)
            start += value
            draw = data_list[start]/scaler - shifter1
            y = int(draw)
            oled.pixel(x, y, 1)
            print(x, y)
        if start <= 0:
            print("nope")
        oled.show()
        
        
        
        
        
        """for i in range(0, 128):
            draw = data_list[start+i]/scaler - shifter1
            draw = int(draw)
            oled.pixel(i, draw, 1)
            print(i, draw)
        oled.show()
"""