import time
from ssd1306 import SSD1306_I2C
from machine import UART, Pin, I2C
from filefifo import Filefifo
from fifo import Fifo
from led import Led 



data = Filefifo(10, name = "capture_250Hz_01.txt")



frequency = 250
prev_value = 0
slope = 0
prev_slope = 0
samples = 0
rising = False
start_count = False
sample_list = []
sample_time = 2
min_list = []
max_list = []


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



min_list.sort()
max_list.sort()
min = min_list[0]
max = max_list[-1]





tup = (min, max)

scaler = (tup[1] - tup[0])/(100 - 0)
shifter1 = tup[0]/scaler - 0
shifter2 = tup[1]/scaler - 100


while True:
    value = data.get()
    if sample_time >= 10:
        break
    print((value/scaler) - shifter1)
    if (value/scaler - shifter1) == 100:
        sample_time += 1