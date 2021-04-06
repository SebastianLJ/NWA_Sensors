import csv
import re
from datetime import datetime

import matplotlib.animation as animation
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

x1 = []
rhum = []
avghum = []
window = []
x2 = []
outAvgHum = []

minutes = mdates.MinuteLocator(byminute=[0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55], interval=1)
qMinutes = mdates.MinuteLocator(byminute=[0, 15, 30, 45], interval=1)
hours = mdates.HourLocator()
# noinspection SpellCheckingInspection
xformatter = mdates.DateFormatter('%H:%M')

fig, (ax1, ax2) = plt.subplots(2, sharex='all', figsize=(10, 6))


def animate(i):
    with open('data/new_data/2021-04-06_15-37-20.csv', 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            print(row)
            x1.append(str(row[0]))
            rhum.append(float(row[1]))
            avghum.append(float(row[2]))
            if int(row[4]) == 1:
                window.append(float(row[2]))
            else:
                window.append(None)

    with open('data/outdoorlog.csv', 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            stime = re.search('\d\d:\d\d:\d\d', str(row[0])).group()
            x2.append(datetime.strptime(stime, '%H:%M:%S'))
            outAvgHum.append(float(row[2]))

    ax1.clear()
    ax2.clear()

    ax1.plot(x1, avghum, label='indoor avg. rhum', color='blue', linewidth=2)
    ax1.plot(x1, window, label='window registered as open', color='red', linewidth=2)
    ax2.plot(x2, outAvgHum, label='outdoor avg. rhum', color='green', linewidth=2)

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
    fig.savefig(fname='plots/hPlot.png')


ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
