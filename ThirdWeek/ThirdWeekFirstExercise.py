import time
from ssd1306 import SSD1306_I2C
from machine import UART, Pin, I2C
from filefifo import Filefifo
from fifo import Fifo
from led import Led 

class Encoder:
    def __init__(self, rot_a, rot_b):
        self.a = Pin(rot_a, mode = Pin.IN, pull = Pin.PULL_UP)
        self.b = Pin(rot_b, mode = Pin.IN, pull = Pin.PULL_UP)
        self.fifo = Fifo(30, typecode = 'i')
        self.a.irq(handler = self.handler, trigger = Pin.IRQ_RISING, hard = True)
        
    def handler(self, pin):
        if self.b():
            self.fifo.put(-1)
        else:
            self.fifo.put(+1)
            
rot = Encoder(10,11)
light = Led(20, Pin.OUT)
rot_butt = Pin(12, Pin.IN, pull = Pin.PULL_UP)
brightness = 50

if light.value():
    light.off()
    
while True:
    if not rot_butt.value():
        time.sleep(0.5)
        if light.value():
            light.off()
        elif not light.value():
            light.on()
            while True:
                if rot.fifo.has_data():
                    data = rot.fifo.get()
                    if (brightness + data) >= 0.5 and (brightness + data) <= 100:
                        brightness += data
                    else:
                        print("Number out of range rotate other way")
                    print(data)
                    print(brightness)
                    light.brightness(brightness)
                elif not rot_butt.value():
                    light.off()
                    break
                else:
                    pass
        time.sleep(0.5)

