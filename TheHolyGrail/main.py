import time
from ssd1306 import SSD1306_I2C
from machine import UART, Pin, I2C, ADC
from filefifo import Filefifo
from fifo import Fifo
from led import Led
from piotimer import Piotimer
import micropython
import ujson
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
gap_ms = 4
count = 0
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
character_width = 8
text_height = 8
oled = SSD1306_I2C(oled_width, oled_height, i2c)
sensor = ADC(Pin(26)) #ADC_0
rot = Encoder(10,11)
rot_butt = Pin(12, Pin.IN, pull = Pin.PULL_UP)
info = 0

def button_handler(pin):
    global ts
    ts = time.ticks_ms()
    press.put(1)
    
rot_butt.irq(handler = button_handler, trigger = Pin.IRQ_FALLING, hard = True)



def start_menu():
    global pts
    global highlighted_text
    global max_sample
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
                #print(ts - pts)
                pts = ts
                continue
            else:
                #print(ts - pts)
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
            
            
def collecting_data():
    while not info:
        oled.fill(0)
        oled.text("Collecting", 24, 25, 1)
        oled.text("Data...", 47, 35, 1)
        oled.show()
        
def sending_data():
    while not info:
        oled.fill(0)
        oled.text("Sending", 24, 25, 1)
        oled.text("Data...", 47, 35, 1)
        oled.show()
        
def error_data():
    while not info:
        oled.fill(0)
        oled.text("Error sending data", 2, 2, 1)
        oled.text("Press the button", 2, 10, 1)
        oled.text("to retry or wait 3", 2, 18, 1)
        oled.text("seconds to return.", 2, 26, 1 )
        

            
def measure_hr():
    global ppis, sample_list, count, max_sample, peakcounts, pts, ts
    go_back = False
    while True:
        if go_back == True:
            break
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
                #print(max_value, threshhold)
                count = 0
                
                #gathering peak counts
                for i in sample_list:
                    if i >= threshhold and i > max_sample:
                        max_sample = i
                    elif i < threshhold and max_sample != 0:
                        peakcounts.append(sample_list.index(max_sample))
                        print(sample_list.index(max_sample), max_sample)
                        max_sample = 0
                        
                print(len(peakcounts))
                for i in range(len(peakcounts)):
                    delta = peakcounts[i] - peakcounts [i - 1]
                    ppi = delta * gap_ms
                    if press.has_data():
                        value = press.get()
                        if ts - pts < 250:
                            #print(ts - pts)
                            pts = ts
                            continue
                        else:
                           # print(ts - pts)
                            pts = ts
                            go_back = True
                            break

                    
                    if ppi > 300 and ppi < 1200:
                        heartrate = 60000/ppi
                        heartrate = round(heartrate)
                        if heartrate > minhr and heartrate < maxhr:
                            oled.fill(0)
                            oled.rect(oled_width - (character_width * 4), oled_height - (text_height + 1), character_width * 4, text_height, 1, 1)
                            oled.text("STOP", oled_width - (character_width * 4), oled_height - text_height, 0)
                            oled.text(f"HR : {heartrate} BPM", 0, 30, 1)
                            oled.show()
                            #print(f"HR : {heartrate} BPM")
                            ppis.append(ppi)

                
                sample_list = []
                peakcounts = []




            
            


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

def get_signal(tid):
    samples.put(sensor.read_u16())

timer = Piotimer(period = 4, mode = Piotimer.PERIODIC, callback = get_signal)

if highlighted_text == 1:
    measure_hr()


start_menu()
                
"""if highlighted_text == 2:
    #hrv_analysis()

    mean_ppi = sum(ppis)/len(ppis)
    
    mean_HR = 60000/mean_ppi
    
    for ppi in ppis:
        ibi_diff += (ppi - mean_ppi)**2
    ssdn = math.sqrt(ibi_diff/len(ppis - 1))
    
    for i in range(len(ppis) - 1):
        ibi_diff += (ppis[i] - ppis[i + 1])**2
    rmssd = math.sqrt(ibi_diff/len(ppis - 1))
    
    measurement = {
    "mean_hr": mean_HR,
    "mean_ppi": mean_ppi,
    "rmssd": rmssd,
    "sdnn": sdnn
    }
    json_message = measurement.json()
"""

if highlighted_text == 3:
    error_data()


"""if highlighted_text == 4:
    text_pos_magn = [0, 2, 4, 6]
    highlighted_text = 0
    oled.fill(0)
    oled.text("MEASUREMENT 1", 0, 0 + 1, 1)
    oled.text("MEASUREMENT 2", 0, (text_height * text_pos_magn[1]) + 1, 1)
    oled.text("MEASUREMENT 3", 0, (text_height * text_pos_magn[2]) + 1, 1)
    oled.text("MEASUREMENT 4", 0, (text_height * text_pos_magn[3]) + 1, 1)
    oled.show()
    pass
"""