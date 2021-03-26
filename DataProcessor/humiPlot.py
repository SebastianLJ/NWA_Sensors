import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import rcParams
import numpy as np
import csv
import re
from datetime import datetime

x1 = []
rhum = []
avghum = []
window = []
x2 = []
outAvgHum = []

minutes = mdates.MinuteLocator(byminute=[0,5,10,15,20,25,30,35,40,45,50,55], interval=1)
qMinutes = mdates.MinuteLocator(byminute=[0,15,30,45], interval=1)
hours = mdates.HourLocator()
xformatter = mdates.DateFormatter('%H:%M')

with open('data/indoorlog.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        stime = re.search('\d\d:\d\d:\d\d', str(row[0])).group()
        x1.append(datetime.strptime(stime, '%H:%M:%S'))
        rhum.append(float(row[1]))
        avghum.append(float(row[2]))
        if int(row[4]) == 1:
            window.append(float(row[2]))
        else:
            window.append(None)

with open('data/outdoorlog.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        stime = re.search('\d\d:\d\d:\d\d', str(row[0])).group()
        x2.append(datetime.strptime(stime, '%H:%M:%S'))
        outAvgHum.append(float(row[2]))

fig, (ax1, ax2) = plt.subplots(2, sharex='all', figsize=(10,6))

ax1.plot(x1, avghum, label='indoor avg. rhum', color='blue')
ax1.plot(x1, window, label='window registered as open', color='red')
ax2.plot(x2, outAvgHum, label='outdoor avg. rhum', color='green')

fig.text(0.5, 0.04, 'Time', ha='center')
fig.text(0.04, 0.5, 'Relative Humidity', va='center', rotation='vertical')
ax1.xaxis.set_major_locator(qMinutes)
ax1.xaxis.set_minor_locator(minutes)
ax2.xaxis.set_major_locator(qMinutes)
ax2.xaxis.set_minor_locator(minutes)
ax1.xaxis.set_major_formatter(xformatter)
ax2.xaxis.set_major_formatter(xformatter)

ax1.grid(which='major', color='black', linestyle='-', linewidth=1, alpha=0.5)
ax1.grid(which='minor', color='gray', linestyle='-', linewidth=0.5, alpha=0.5)
ax2.grid(which='major', color='black', linestyle='-', linewidth=1, alpha=0.5)
ax2.grid(which='minor', color='gray', linestyle='-', linewidth=0.5, alpha=0.5)

fig.autofmt_xdate()

ax1.set_title('Indoor Humidity')
ax2.set_title('Outdoor Humidity')
fig.legend()
plt.show()
fig.savefig(fname='plots/hPlot.png')
