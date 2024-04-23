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
prev_delta = 0
delta_list = []

while len(sample_list) < 5:
    value = data.get()
    current_slope = value - prev_value
    samples += 1
    
    if current_slope <= 0 and prev_slope > 0:
        sample_list.append(samples)
        current_peak = prev_value
        prev_delta = samples
    prev_value = value
    prev_slope = current_slope
for i in range(4):
    delta_list.append(sample_list[i+1] - sample_list[i])
    
print(delta_list)

average_samples = sum(delta_list)//len(delta_list)
        
sample_time = (1/frq) * average_samples   
print(sample_time)
        
frq_samples = 1/sample_time        
print(frq_samples)




