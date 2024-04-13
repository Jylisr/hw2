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
led1 = Led(22, Pin.OUT)
led2 = Led(21, Pin.OUT)
led3 = Led(20, Pin.OUT)
brightness = 50


press = Fifo(20, typecode = 'i')
ticks = []
rot_butt = Pin(12, Pin.IN, pull = Pin.PULL_UP)

def button_handler(pin):
    press.put(+1)
    timer = time.ticks_ms
    ticks.append(timer)
rot_butt.irq(handler = button_handler, trigger = Pin.IRQ_FALLING, hard = True)


i2c = I2C(1, scl = Pin(15), sda = Pin(14), freq = 400_000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)


text_width = 8
text_height = 8
oled.fill(0)
text_pos_magn = [0,2,4]
oled.text("LED1 - OFF", 0, 0 + 1, 1)
oled.text("LED2 - OFF", 0, (text_height * text_pos_magn[1]) + 1, 1)
oled.text("LED3 - OFF", 0, (text_height * text_pos_magn[2]) + 1, 1)
oled.show()
highlighted_text = 0
highlight = False



while True:
    if highlighted_text != 0:
        pos = text_pos_magn[highlighted_text - 1]
        oled.rect(0, text_height * pos, oled_width, text_height + 2, 1)

    

    
    oled.show()
    
    while rot.fifo.has_data():
        value = rot.fifo.get()
        if value == 1:
            if highlighted_text + 1 < 4:
                pos = text_pos_magn[highlighted_text - 1]
                oled.rect(0, text_height * pos, oled_width, text_height + 2, 0)
                highlighted_text += 1

        elif value == -1:
            if highlighted_text > 1:
                pos = text_pos_magn[highlighted_text - 1]
                oled.rect(0, text_height * pos, oled_width, text_height + 2, 0)
                highlighted_text -= 1
                
        
    while press.has_data():
        val = press.get()
        if time.ticks_add(ticks[-1],ticks[-2] > 50):
            pass
        elif highlighted_text == 1:
            led1.toggle()
        elif highlighted_text == 2:
            led2.toggle()
        elif highlighted_text == 3:
            led3.toggle()
        
        if led1.value():
            oled.rect(0, 0 + 1, oled_width, text_height, 0, [True])
            oled.text("LED1 - ON", 0, 0 + 1, 1)
        else:
            oled.rect(0, 0 + 1, oled_width, text_height, 0, [True])
            oled.text("LED1 - OFF",0, 0 + 1, 1)
        
        if led2.value():
            oled.rect(0, (text_height * text_pos_magn[1]), oled_width, text_height, 0, [True])
            oled.text("LED2 - ON", 0, (text_height * text_pos_magn[1]) + 1, 1)
        else:
            oled.rect(0, (text_height * text_pos_magn[1]), oled_width, text_height, 0, [True])
            oled.text("LED2 - OFF", 0, (text_height * text_pos_magn[1]) + 1, 1)
        
        if led3.value():
            oled.rect(0, (text_height * text_pos_magn[2]), oled_width, text_height, 0, [True])
            oled.text("LED3 - ON", 0, (text_height * text_pos_magn[2]) + 1, 1)
        else:
            oled.rect(0, (text_height * text_pos_magn[2]), oled_width, text_height, 0, [True])
            oled.text("LED3 - OFF", 0, (text_height * text_pos_magn[2]) + 1, 1)
