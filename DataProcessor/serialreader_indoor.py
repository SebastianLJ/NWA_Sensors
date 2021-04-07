import serial
from datetime import datetime
import csv

import matplotlib
import matplotlib.animation as animation
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np

ser = serial.Serial('COM3')
ser.flushInput()

now = datetime.now()
part0 = "data/new_data/indoor_"
part1 = datetime.now().strftime("%Y-%m-%d")
part2 = datetime.now().strftime("%H-%M-%S")

plot_window = 100

rhum = np.array(np.full([plot_window], None))
avghum = np.array(np.full([plot_window], None))
isWindowOpen = np.array(np.full([plot_window], None))

plt.ion()
plt.ylim([20,50])
fig, ax = plt.subplots()
line0, = ax.plot(rhum, label='indoor rhum', color='lightblue', linewidth=2)
line1, = ax.plot(avghum, label='indoor avg. rhum', color='blue', linewidth=2)
line2, = ax.plot(isWindowOpen, label='window registered as open', color='red', linewidth=2)



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

    rhum = np.append(rhum, float(arrToWrite[1]))
    rhum = rhum[1:plot_window+1]
    avghum = np.append(avghum, float(arrToWrite[2]))
    avghum = avghum[1:plot_window+1]
    if int(arrToWrite[4]) == 1:
        isWindowOpen = np.append(isWindowOpen, float(arrToWrite[2]))
    else:
        isWindowOpen = np.append(isWindowOpen, None)
    isWindowOpen = isWindowOpen[1:plot_window+1]

    line0.set_ydate(rhum)
    line1.set_ydata(avghum)
    line2.set_ydata(isWindowOpen)
    ax.autoscale_view()
    fig.canvas.draw()
    fig.canvas.flush_events()