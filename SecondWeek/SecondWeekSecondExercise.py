import time
from ssd1306 import SSD1306_I2C
from machine import UART, Pin, I2C
from filefifo import Filefifo
from fifo import Fifo

#scaler = 99.99
#shifter = 70.007

data = Filefifo(10, name = "capture_250Hz_01.txt")


#def main(time = 2, scaler = 1, shifter = 0, display_graph = False):
    
prev_value = 0
samples = 0
rising = False
start_count = False
sample_list = []
sample_time = 0
min_list = []
max_list = []


while True:
    value = data.get()
    if sample_time >= 2:
        break
    if rising == True and prev_value > value:
        sample_list.append(samples)
        if sample_list[0] == 0:
            sample_list.pop()
        if min_list[0] == 0:
                min_list.pop()

        elif len(sample_list) > 1:
            sample_time += (1/250) * sample_list[-1]
            sample_time = round(sample_time)
        samples = 0
        max_list.append(prev_value)
        start_count = True
        rising = False

    if value > prev_value:
        if rising == False:
            min_list.append(prev_value)
        rising = True
        
    if start_count == True:
        samples += 1
    
    prev_value = value



min_list.sort()
max_list.sort()
min = min_list[0]
max = max_list[-1]





tup = (min, max)

scaler = (tup[1] - tup[0])/(100 - 0)
shifter1 = tup[0]/scaler - 0
shifter2 = tup[1]/scaler - 100

#main(time = 10, scaler = scaler, shifter = shifter1, display_graph = True)
while True:
    value = data.get()
    if sample_time >= 10:
        break
    print((value/scaler) - shifter1)
    if (value/scaler - shifter1) == 100:
        sample_time += 1
