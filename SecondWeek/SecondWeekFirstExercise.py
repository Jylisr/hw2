import time
from ssd1306 import SSD1306_I2C
from machine import UART, Pin, I2C
from filefifo import Filefifo
from fifo import Fifo


data = Filefifo(10, name = "capture_250Hz_01.txt")
prev_value = 0
samples = 0
rising = False
start_count = False
sample_list = []
frq = 250

while len(sample_list) < 4:
    value = data.get()
    if value > prev_value:
        rising = True
    if start_count == True:
        samples += 1
    
    if rising == True and prev_value > value:
        sample_list.append(samples)
        if sample_list[0] == 0:
            sample_list.pop()
        samples = 0
        current_peak = prev_value
        start_count = True
        rising = False
    prev_value = value
    
print(sample_list)

average_samples = sum(sample_list)//len(sample_list)
        
sample_time = (1/frq) * average_samples   
print(sample_time)        
        
frq_samples = 1/sample_time        
print(frq_samples)
