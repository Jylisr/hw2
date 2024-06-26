import time
from ssd1306 import SSD1306_I2C
from machine import UART, Pin, I2C
from filefifo import Filefifo
from fifo import Fifo

#scaler = 99.99
#shifter = 70.007

data = Filefifo(10, name = "capture_250Hz_01.txt")



frequency = 250
prev_value = 0
slope = 0
prev_slope = 0
samples = 0
sample_list = []
sample_time = 2
min_list = []
max_list = []


while not [samples + sum(sample_list)] >= [sample_time * frequency]:
    value = data.get()
    samples += 1
    current_slope = value - prev_value
    if current_slope <= 0 and prev_slope > 0:
        sample_list.append(samples)
        samples = 0
        max_list.append(prev_value)

    if current_slope >= 0 and prev_slope < 0:
            min_list.append(prev_value)

    if current_slope >= 0 and prev_slope < 0:
            min_list.append(prev_value)

        

    
    prev_value = value
    prev_slope = current_slope




min = min(min_list)
max = max(max_list)





tup = (min, max)

scaler = (tup[1] - tup[0])/(100 - 0)
shifter1 = tup[0]/scaler - 0
shifter2 = tup[1]/scaler - 100


while not sample_time >= 10:
    value = data.get()
    print((value/scaler) - shifter1)
    if (value/scaler - shifter1) == 100:
        sample_time += 1