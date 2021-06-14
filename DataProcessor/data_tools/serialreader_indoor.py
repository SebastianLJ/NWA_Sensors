import csv
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import serial
import os.path

ser = serial.Serial('COM3')
ser.flushInput()

now = datetime.now()
part0 = os.path.dirname(__file__) + "/../data/new_data/indoor_"
part1 = datetime.now().strftime("%Y-%m-%d")
part2 = datetime.now().strftime("%H-%M-%S")

plot_window = 100

rhum = np.array(np.full([plot_window], None))
avghum = np.array(np.full([plot_window], None))
isWindowOpen = np.array(np.full([plot_window], None))
thresholdRes = np.array(np.full([plot_window], None))

plt.ion()
fig, ax = plt.subplots()
line0, = ax.plot(rhum, label='indoor rhum', color='lightblue', linewidth=2)
line1, = ax.plot(avghum, label='indoor avg. rhum', color='blue', linewidth=2)
line2, = ax.plot(isWindowOpen, label='window registered as open', color='red', linewidth=2)


# line 32-41 is from the following implementation.
# https://makersportal.com/blog/2018/2/25/python-datalogger-reading-the-serial-output-from-arduino-to-analyze-data-using-pyserial
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
    thresholdRes = np.append(thresholdRes, float(arrToWrite[4]))
    thresholdRes = thresholdRes[1:plot_window+1]
    if int(arrToWrite[4]) == 1:
        isWindowOpen = np.append(isWindowOpen, float(arrToWrite[2]))
    else:
        isWindowOpen = np.append(isWindowOpen, None)
    isWindowOpen = isWindowOpen[1:plot_window+1]

    line0.set_ydata(rhum)
    line1.set_ydata(avghum)
    line2.set_ydata(isWindowOpen)
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()
    fig.canvas.flush_events()
