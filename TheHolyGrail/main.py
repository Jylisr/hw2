import time
from ssd1306 import SSD1306_I2C
from machine import UART, Pin, I2C, ADC
from filefifo import Filefifo
from fifo import Fifo
from led import Led
from piotimer import Piotimer
import micropython
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
            

micropython.alloc_emergency_exception_buf(200)
samples = Fifo(2000)
press = Fifo(20)
sample_list = []
peakcounts = []
max_sample = 0
minhr = 30
maxhr = 240
pts = 0
ppis = []
ppi_list_processed = []
gap_ms = 4
count = 0
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
character_width = 8
text_height = 8
oled = SSD1306_I2C(oled_width, oled_height, i2c)
sensor = ADC(Pin(26))
rot = Encoder(10,11)
rot_butt = Pin(12, Pin.IN, pull = Pin.PULL_UP)

def button_handler(pin):
    global ts
    ts = time.ticks_ms()
    press.put(1)
    
rot_butt.irq(handler = button_handler, trigger = Pin.IRQ_FALLING, hard = True)



def start_menu():
    global pts
    global highlighted_text
    text_pos_magn = [0, 2, 4, 6]
    highlighted_text = 0
    oled.fill(0)
    oled.text("MEASURE HR", 0, 0 + 1, 1)
    oled.text("BASIC HRV ANALYSIS", 0, (text_height * text_pos_magn[1]) + 1, 1)
    oled.text("HISTORY", 0, (text_height * text_pos_magn[2]) + 1, 1)
    oled.text("KUBIOS", 0, (text_height * text_pos_magn[3]) + 1, 1)
    oled.show()

    while True:
        if highlighted_text != 0:
            pos = text_pos_magn[highlighted_text - 1]
            oled.rect(0, text_height * pos, oled_width, text_height + 2, 1)
        
        oled.show()
        if press.has_data():
            value = press.get()
            if ts - pts < 250:
                print(ts - pts)
                pts = ts
                continue
            else:
                print(ts - pts)
                pts = ts
                break
        
        while rot.fifo.has_data():
            value = rot.fifo.get()
            if value == 1:
                if highlighted_text + 1 < 5:
                    pos = text_pos_magn[highlighted_text - 1]
                    oled.rect(0, text_height * pos, oled_width, text_height + 2, 0)
                    highlighted_text += 1

            elif value == -1:
                if highlighted_text > 1:
                    pos = text_pos_magn[highlighted_text - 1]
                    oled.rect(0, text_height * pos, oled_width, text_height + 2, 0)
                    highlighted_text -= 1

            
"""        if time.ticks_diff(time.ticks_ms(), pts) >= 250:
            break  """
            


def get_signal(tid):
    samples.put(sensor.read_u16())

timer = Piotimer(period = 4, mode = Piotimer.PERIODIC, callback = get_signal)

            
            


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

while not press.has_data():
    pass

data = press.get()
pts = ts
start_menu()


if highlighted_text == 1:
    while True:
        if samples.has_data():
            sample = samples.get()
            sample_list.append(sample)
            count += 1
            if sample < 0:
                break
            if count >= 750:
                max_value = max(sample_list)
                min_value = min(sample_list)
                threshhold = (4*max_value + min_value)/5
                print(max_value)
                #prev = sample_list[0]
                print(threshhold)
                count = 0
                
                #gathering peak counts
                for i in sample_list:
                    if i >= threshhold and i > max_sample:
                        max_sample = i
                    if i < threshhold and max_sample != 0:
                        peakcounts.append(sample_list.index(max_sample))
                        max_sample = 0
                        
                        
                for i in range(len(peakcounts)):
                    delta = peakcounts[i] - peakcounts [i - 1]
                    ppi = delta * gap_ms
                    
                    if ppi > 0:
                        heartrate = 60000/ppi
                        heartrate = round(heartrate)
                        if heartrate > minhr and heartrate < maxhr:
                            oled.fill(0)
                            oled.text(f"HR : {heartrate} BPM", 0, 30, 1)
                            oled.show()
                            print(f"HR : {heartrate} BPM")
                            ppis.append(ppi)
                        

