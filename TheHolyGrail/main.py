import time
from ssd1306 import SSD1306_I2C
from machine import UART, Pin, I2C, ADC
from filefifo import Filefifo
from fifo import Fifo
from led import Led
from piotimer import Piotimer
#import extraction



class Encoder:
    def __init__(self, rot_a = 10, rot_b = 11):
        self.a = Pin(rot_a, mode = Pin.IN, pull = Pin.PULL_UP)
        self.b = Pin(rot_b, mode = Pin.IN, pull = Pin.PULL_UP)
        self.fifo = Fifo(30, typecode = 'i')
        self.a.irq(handler = self.handler, trigger = Pin.IRQ_RISING, hard = True)
        
    def handler(self, pin):
        if self.b():
            self.fifo.put(-1)
        else:
            self.fifo.put(+1)
            
            
samples = Fifo(2000)
minhr = 30
maxhr = 240
ppis = []
ppi_list_processed = []
gap_ms = 4
counter = 0
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
character_width = 8
text_height = 8
oled = SSD1306_I2C(oled_width, oled_height, i2c)
sensor = ADC(Pin(26))
rot = Encoder(10,11)
rot_butt = Pin(12, Pin.IN, pull = Pin.PULL_UP)
            
            


oled.fill(0)
oled.text("Welcome to",24 ,25, 1)
oled.text("PulsePal",32 ,35, 1)

oled.text("Start", 44, 56, 1)
oled.show()

while not rot.fifo.has_data():
    pass

data = rot.fifo.get()
oled.rect(44,56,character_width * 5,text_height, 1, 1)
oled.text("Start", 44, 56, 0)
oled.show()

while rot_butt.value():
    pass

def get_signal():
    data = sensor.read_u16()
    samples.put(data)

timer = Piotimer(period = gap_ms, mode = Piotimer.PERIODIC, callback = get_signal)

 