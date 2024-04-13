import time
from ssd1306 import SSD1306_I2C
from machine import UART, Pin, I2C
from filefifo import Filefifo
from fifo import Fifo


data = Filefifo(10, name = "capture_250Hz_03.txt")
prev_value = 0
samples = 0
rising = False
start_count = False
sample_list = []
frq = 250
current_slope = 0
prev_slope = 0

while len(sample_list) < 4:
    value = data.get()
    current_slope = value - prev_value
    samples += 1
    
    if current_slope <= 0 and prev_slope > 0:
        sample_list.append(samples)
        samples = 0
        current_peak = prev_value
    prev_value = value
    prev_slope = current_slope
    
print(sample_list)

average_samples = sum(sample_list)//len(sample_list)
        
sample_time = (1/frq) * average_samples   
print(sample_time)
        
frq_samples = 1/sample_time        
print(frq_samples)


#change current program and base it off of previous and current slope
