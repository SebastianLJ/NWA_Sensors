import serial
from datetime import datetime
import csv

import matplotlib.pyplot as plt
import numpy as np

ser = serial.Serial('COM4')
ser.flushInput()

now = datetime.now()
part0 = "data/new_data/outdoor_"
part1 = datetime.now().strftime("%Y-%m-%d")
part2 = datetime.now().strftime("%H-%M-%S")

plot_window = 100

temp = np.array(np.full([plot_window], None))

plt.ion()
fig, ax = plt.subplots()
line1, = ax.plot(temp, label='indoor avg. rhum', color='red', linewidth=2)


while True:
    ser_bytes = ser.readline()
    decoded_bytes = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8")).split(",")
    print(str(decoded_bytes))
    with open(part0 + part1 + "_" + part2 + ".csv", "a", buffering=1, newline='') as f:
        writer = csv.writer(f, delimiter=",", quoting=csv.QUOTE_MINIMAL)
        arrToWrite = []
        arrToWrite.append(datetime.now().strftime("%H:%M:%S"))
        arrToWrite += decoded_bytes
        writer.writerow(arrToWrite)

    temp = np.append(temp, float(arrToWrite[3]))
    temp = temp[1:plot_window+1]

    line1.set_ydata(temp)
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()
    fig.canvas.flush_events()