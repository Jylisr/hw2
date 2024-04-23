import time
from ssd1306 import SSD1306_I2C
from machine import UART, Pin, I2C
from filefifo import Filefifo
from fifo import Fifo
from led import Led

data = Filefifo(20, name = "capture02_250Hz.txt")

frequency = 250
prev_value = 0
slope = 0
prev_slope = 0
samples = 0
sample_list = []
sample_time = 2
min_list = []
max_list = []


prev_value = 0
samples = 0
rising = False
start_count = False
sample_list = []
frq = 250
current_slope = 0
prev_slope = 0

while True:
    value = data.get()
    samples += 1
    current_slope = value - prev_value
    if current_slope <= 0 and prev_slope > 0:
        sample_list.append(samples)
        samples = 0
        max_list.append(prev_value)

    if current_slope >= 0 and prev_slope < 0:
            min_list.append(prev_value)


    if [samples + sum(sample_list)] >= [sample_time * frequency]:
        break

    if current_slope >= 0 and prev_slope < 0:
            min_list.append(prev_value)

        

    
    prev_value = value
    prev_slope = current_slope


    
print(sample_list)

average_samples = sum(sample_list)//len(sample_list)
        
sample_time = (1/frq) * average_samples   
print(sample_time)
        
frq_samples = 1/sample_time        
print(frq_samples)
