from filefifo import Filefifo

def normalize (data, sample_time=2, frequency=250):
    
    samples = 0
    sample_list = []
    min_value = float("inf")
    max_value = float("-inf")
    
    while True:
        value = data.get()
        samples += 1
        if value < min_value:
            min_value = value
        if value > max_value:
            max_value = value
        if (samples + sum(sample_list)) >= (sample_time * frequency):
            break
    
tup = (min, max)

scaler = (tup[1] - tup[0])/(100 - 0)
shifter1 = tup[0]/scaler - 0
shifter2 = tup[1]/scaler - 100

normalized_data = []

while True:
    value = data.get()
    if sample_time >= 10:
        break
    
    normalized_value = (value/scaler) - shifter1
    normalized_data.append(normalized_value)
    
    if normalized_value == 100:
        sample_time += 1
    
return normalized_data
    
    
    
    