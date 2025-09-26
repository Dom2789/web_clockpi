import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
from io import BytesIO

def plot_roomtemp(data):
    # raw_data needs to be a list of strings
    raw_data = [item['content'] for item in data]

    time = []
    temperature = []
    pressure = [] 
    humidity = []

    data = [time, temperature, pressure, humidity]

    chars_to_replace = ["C", "[", "]", "hPa", "%"]

    no_datasets = len(raw_data)

    for line in raw_data:
        for char in chars_to_replace:
            line = line.replace(char, "")
        line = line.split()
        for idx, listing in enumerate(data):
            if idx == 0:
                hours, min, sec = line[idx].split(":")
                data[idx].append((int(hours),int(min),int(sec)))
            else:
                data[idx].append(float(line[idx]))

    first_timestamp = data[0][0]
    last_timestamp = data[0][-1]

    #creating structure for x-axis
    # every hour contains 60 list for corresponding minutes 
    # every minute contains 60 lists for corresponding secondes
    timeline = [[[[] for z in range(60)] for y in range(60)] for x in range(first_timestamp[0],last_timestamp[0]+1)]

    # filling time series with data
    starting_hour = first_timestamp[0]

    for i in range(no_datasets):
        for j in range(1,4):
            timeline[data[0][i][0]-starting_hour][data[0][i][1]][data[0][i][2]].append(data[j][i])

    time_series = []

    for h in timeline:
        for min in h:
            for sec in min:
                time_series.append(sec)

    # create list with data pints where the at index 0 are the seconds which passed since start of logging
    time_beam = []
    temperature_sec = []
    pressure_sec = []
    humidity_sec = []

    for idx, ele in enumerate(time_series):
        if ele != []:
            time_beam.append(idx)
            temperature_sec.append(ele[0])
            pressure_sec.append(ele[1])
            humidity_sec.append(ele[2])


    # create plot temperature
    figure, axis = plt.subplots(3, 1, figsize=(14,10))

    axis[0].plot(time_beam,temperature_sec, 'r--')
    axis[1].plot(time_beam,pressure_sec, 'k--')
    axis[2].plot(time_beam,humidity_sec, 'b--')

    axis[0].set_title("Temperature in °C")
    axis[1].set_title("Pressure in hPa")
    axis[2].set_title("Humidity in %")

    # adding times to the x-axis
    labels, locs= plt.xticks()
    labels = list(labels)
    new_x_axis = []
    offset = first_timestamp[0]*3600 -3600 #-3600 compensates for summertime

    for number in labels:
        new_labels = []
        seconds = int(number) + offset
        new_labels.append(str(seconds%60))
        minutes = seconds // 60
        new_labels.append(str(minutes%60))
        hours = minutes // 60
        new_labels.append(str(hours))

        for idx, digit in enumerate(new_labels):
            if len(digit) == 1:
                new_labels[idx] = "0" + digit

        string = f"{new_labels[2]}:{new_labels[1]}:{new_labels[0]}"

        new_x_axis.append(string)

    axis[0].set_xticklabels(new_x_axis)
    axis[1].set_xticklabels(new_x_axis)
    axis[2].set_xticks(labels, new_x_axis)
    plt.xlabel(f"Time of day")

    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight', facecolor='white')
    
    return buffer

    