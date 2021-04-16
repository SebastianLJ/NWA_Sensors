import csv
from datetime import datetime
import peak_detection

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np

filename = 'indoor_2021-04-16_09-48-58'

time = []
avghum = []
rhum = []
temp = []
window = []
hum_filter = []
carbondioxide = []
tVOC = []

minutes = mdates.MinuteLocator(byminute=[0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55], interval=1)
qMinutes = mdates.MinuteLocator(byminute=[0, 15, 30, 45], interval=1)
hours = mdates.HourLocator()
# noinspection SpellCheckingInspection
xformatter = mdates.DateFormatter('%H:%M')

fig1, (ax1, ax2, ax3) = plt.subplots(3, sharex='all', figsize=(10, 5))
fig2, (ax4, ax5) = plt.subplots(2, sharex='all', figsize=(10,5))

#indoor dataread
with open('data/new_data/' + filename + '.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        time.append(datetime.strptime(row[0], '%H:%M:%S'))
        rhum.append(float(row[1]))
        avghum.append(float(row[2]))
        temp.append(float(row[3]))
        hum_filter.append(int(row[4]))
        if int(row[4]) == 1:
            window.append(float(row[2]))
        else:
            window.append(None)
        carbondioxide.append(float(row[5]))
        tVOC.append(float(row[6]))

m_rhum = peak_detection.mean_algo(np.array(rhum), 100, 2)
m_co2 = peak_detection.mean_algo(np.array(carbondioxide), 10, 100)
z_rhum = peak_detection.thresholding_algo(np.array(rhum), peak_detection.rhum_lag, peak_detection.rhum_threshold, peak_detection.rhum_influence)['signals']
z_co2 = peak_detection.thresholding_algo(np.array(carbondioxide), peak_detection.co2_lag, peak_detection.co2_threshold, peak_detection.co2_influence)['signals']

ax1.plot(time, rhum, label='indoor rhum', color='lightblue', linewidth=2)
ax1.plot(time, avghum, label='indoor avg. rhum', color='blue', linewidth=2)
ax1.plot(time, window, label='window registered as open', color='red', linewidth=2)
ax2.plot(time, m_rhum, label='rhum peaks', color ='red', linewidth=2)
ax3.plot(time, hum_filter, label='rhum peaks', color ='red', linewidth=2)
ax4.plot(time, carbondioxide, label="CO2 level", color='black', linewidth=2)
ax5.plot(time, m_co2, label="tVOC level", color="red", linewidth=2)

fig1.text(0.5, 0.04, 'Time', ha='center')
fig2.text(0.5, 0.04, 'Time', ha='center')

ax1.xaxis.set_major_locator(qMinutes)
ax1.xaxis.set_minor_locator(minutes)
ax1.xaxis.set_major_formatter(xformatter)
ax4.xaxis.set_major_locator(qMinutes)
ax4.xaxis.set_minor_locator(minutes)
ax4.xaxis.set_major_formatter(xformatter)

ax1.grid(which='major', color='black', linestyle='-', linewidth=1, alpha=0.5)
ax1.grid(which='minor', color='gray', linestyle='-', linewidth=0.5, alpha=0.5)
ax2.grid(which='major', color='black', linestyle='-', linewidth=1, alpha=0.5)
ax2.grid(which='minor', color='gray', linestyle='-', linewidth=0.5, alpha=0.5)
ax3.grid(which='major', color='black', linestyle='-', linewidth=1, alpha=0.5)
ax3.grid(which='minor', color='gray', linestyle='-', linewidth=0.5, alpha=0.5)
ax4.grid(which='major', color='black', linestyle='-', linewidth=1, alpha=0.5)
ax4.grid(which='minor', color='gray', linestyle='-', linewidth=0.5, alpha=0.5)
ax5.grid(which='major', color='black', linestyle='-', linewidth=1, alpha=0.5)
ax5.grid(which='minor', color='gray', linestyle='-', linewidth=0.5, alpha=0.5)

fig1.autofmt_xdate()
fig2.autofmt_xdate()

ax1.set_title('Indoor Humidity')
ax2.set_title('Rhum Peaks')
ax3.set_title('Arduino Rhum Peaks')
ax4.set_title('Indoor CO2 level')
ax4.set_title('CO2 Peaks')
fig1.legend()
fig2.legend()
fig1.savefig(fname='plots/indoor_hum_' + filename + '.png')
fig2.savefig(fname='plots/indoor_co2_' + filename + '.png')


plt.show()



