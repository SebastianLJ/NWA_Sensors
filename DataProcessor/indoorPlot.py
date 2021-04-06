import csv
import re
from datetime import datetime

import matplotlib.animation as animation
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

filename = '2021-04-06_15-37-20'

time = []
avghum = []
temp = []
window = []
carbondioxide = []
tVOC = []

minutes = mdates.MinuteLocator(byminute=[0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55], interval=1)
qMinutes = mdates.MinuteLocator(byminute=[0, 15, 30, 45], interval=1)
hours = mdates.HourLocator()
# noinspection SpellCheckingInspection
xformatter = mdates.DateFormatter('%H:%M')

fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, sharex='all', figsize=(10, 10))

with open('data/new_data/' + filename + '.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        time.append(datetime.strptime(row[0], '%H:%M:%S'))
        avghum.append(float(row[2]))
        temp.append(float(row[3]))
        if int(row[4]) == 1:
            window.append(float(row[2]))
        else:
            window.append(None)
        carbondioxide.append(float(row[5]))
        tVOC.append(float(row[6]))

ax1.plot(time, avghum, label='indoor avg. rhum', color='blue', linewidth=2)
ax1.plot(time, window, label='window registered as open', color='red', linewidth=2)
ax2.plot(time, temp, label='indoor temperature', color ='red', linewidth=2)
ax3.plot(time, carbondioxide, label="CO2 level", color='black', linewidth=2)
ax4.plot(time, tVOC, label="tVOC level", color="red", linewidth=2)

fig.text(0.5, 0.04, 'Time', ha='center')

ax1.xaxis.set_major_locator(qMinutes)
ax1.xaxis.set_minor_locator(minutes)
ax1.xaxis.set_major_formatter(xformatter)

ax1.grid(which='major', color='black', linestyle='-', linewidth=1, alpha=0.5)
ax1.grid(which='minor', color='gray', linestyle='-', linewidth=0.5, alpha=0.5)
ax2.grid(which='major', color='black', linestyle='-', linewidth=1, alpha=0.5)
ax2.grid(which='minor', color='gray', linestyle='-', linewidth=0.5, alpha=0.5)
ax3.grid(which='major', color='black', linestyle='-', linewidth=1, alpha=0.5)
ax3.grid(which='minor', color='gray', linestyle='-', linewidth=0.5, alpha=0.5)
ax4.grid(which='major', color='black', linestyle='-', linewidth=1, alpha=0.5)
ax4.grid(which='minor', color='gray', linestyle='-', linewidth=0.5, alpha=0.5)

#fig.autofmt_xdate()

ax1.set_title('Indoor Humidity')
ax2.set_title('Indoor Temperature')
ax3.set_title('Indoor CO2 Level')
ax4.set_title('Indoor tVOC Level')
fig.legend()
fig.savefig(fname='plots/indoor_plot_' + filename + '.png')

plt.show()