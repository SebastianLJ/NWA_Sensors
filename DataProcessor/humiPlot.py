import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import csv
import re
from datetime import datetime

x = []
rhum = []
avghum = []
window = []

minutes = mdates.MinuteLocator(byminute=[0,5,10,15,20,25,30,35,40,45,50,55], interval=1)
qMinutes = mdates.MinuteLocator(byminute=[0,15,30,45], interval=1)
hours = mdates.HourLocator()
xformatter = mdates.DateFormatter('%H:%M')

with open('data/indoorlog.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        stime = re.search('\d\d:\d\d:\d\d', str(row[0])).group()
        x.append(datetime.strptime(stime, '%H:%M:%S'))
        rhum.append(float(row[1]))
        avghum.append(float(row[2]))
        if int(row[4]) == 1:
            window.append(float(row[2]))
        else:
            window.append(None)

plt.plot(x,avghum, label='avg. hum',color='blue')
plt.plot(x,window, label='window', color='red')
plt.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.5)
plt.xlabel('Time')
plt.ylabel('Relative Humidity')
plt.title('Indoor Relative Humidity')
plt.legend()
plt.gcf().axes[0].xaxis.set_major_locator(qMinutes)
plt.gcf().axes[0].xaxis.set_minor_locator(minutes)
plt.gcf().axes[0].xaxis.set_major_formatter(xformatter)
plt.gcf().autofmt_xdate()
plt.show()
