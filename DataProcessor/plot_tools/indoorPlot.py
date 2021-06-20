from signal_processing import peak_detection
from signal_processing import AlgoChecker
from data_tools import indoorLogReader
from data_tools import algoSettings

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np

#maj
filename = 'indoor_2021-04-19_09-42-42'

#juni
#filename = 'indoor_2021-06-14_10-08-13'

minutes = mdates.MinuteLocator(byminute=[0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55], interval=1)
qMinutes = mdates.MinuteLocator(byminute=[0, 15, 30, 45], interval=1)
hours = mdates.HourLocator()
# noinspection SpellCheckingInspection
xformatter = mdates.DateFormatter('%H:%M')

data = indoorLogReader.read_file(filename)


def plot1():
    fig1, (ax1, ax2) = plt.subplots(2, sharex='all', figsize=(10, 5))
    fig2, (ax3) = plt.subplots(1, sharex='all', figsize=(10, 5))

    ax1.plot(data["time"], data["rHum"], label='indoor rhum', color='lightblue', linewidth=2)
    ax1.plot(data["time"], data["avgHum"], label='indoor avg. rhum', color='blue', linewidth=2)
    ax1.plot(data["time"], data["window"], label='window registered as open', color='red', linewidth=2)
    ax2.plot(data["time"], data["windowState"], label='rhum peaks', color='red', linewidth=2)
    ax3.plot(data["time"], data["CO2"], label="CO2 level", color='black', linewidth=2)

    fig1.text(0.5, 0.04, 'Time', ha='center')
    fig2.text(0.5, 0.04, 'Time', ha='center')

    ax1.xaxis.set_major_locator(qMinutes)
    ax1.xaxis.set_minor_locator(minutes)
    ax1.xaxis.set_major_formatter(xformatter)
    ax3.xaxis.set_major_locator(qMinutes)
    ax3.xaxis.set_minor_locator(minutes)
    ax3.xaxis.set_major_formatter(xformatter)

    ax1.grid(which='major', color='black', linestyle='-', linewidth=1, alpha=0.5)
    ax1.grid(which='minor', color='gray', linestyle='-', linewidth=0.5, alpha=0.5)
    ax2.grid(which='major', color='black', linestyle='-', linewidth=1, alpha=0.5)
    ax2.grid(which='minor', color='gray', linestyle='-', linewidth=0.5, alpha=0.5)
    ax3.grid(which='major', color='black', linestyle='-', linewidth=1, alpha=0.5)
    ax3.grid(which='minor', color='gray', linestyle='-', linewidth=0.5, alpha=0.5)

    fig1.autofmt_xdate()
    fig2.autofmt_xdate()

    ax1.set_title('Indoor Humidity')
    ax2.set_title('Rhum Peaks')
    ax3.set_title('Arduino Rhum Peaks')
    ax3.set_title('Indoor CO2 level')
    ax3.set_title('CO2 Peaks')
    fig1.legend()
    fig2.legend()
    fig1.savefig(fname='plots/indoor_hum_' + filename + '.png')
    fig2.savefig(fname='plots/indoor_co2_' + filename + '.png')
    plt.show()


def plotFiltersHum():
    # plot rhum, real window state, filters
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, sharex='all', figsize=(10, 10))
    m_rhum = peak_detection.mean_algo(np.array(data["rHum"]), algoSettings.hum_lag, algoSettings.hum_threshold)
    z_rhum = \
        peak_detection.thresholding_algo(np.array(data["rHum"]), peak_detection.rhum_lag, peak_detection.rhum_threshold,
                                         peak_detection.rhum_influence)['signals']
    acc_res = AlgoChecker.get_results(filename)

    ax1.plot(data["time"], data["rHum"], label='indoor rhum', color='blue', linewidth=2)
    #ax1.plot(data["time"], data["avgHum"], label='indoor avg. rhum', color='royalblue', linewidth=2)
    #ax1.plot(data["time"], data["window"], color='red', linewidth=2)
    ax1.plot(data["time"], list(map(lambda x: x - algoSettings.hum_threshold, data["avgHum"])), label="lower threshold",
             color="red", linewidth=2, alpha=0.8)
    ax2.plot(data["time"], data["windowState"], label='window state', color='red', linewidth=2)
    ax3.plot(data["time"], m_rhum, label='mean filter, acc: ' + str('%.2f' % acc_res["mean_rhum"]["acc"]), color='darkblue', linewidth=2)
    ax4.plot(data["time"], z_rhum, label='z-score filter, acc: ' + str('%.2f' % acc_res["thresholding_rhum"]["acc"]), color='darkgreen', linewidth=2)

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

    fig.autofmt_xdate()

    ax1.set_title('Indoor Humidity')
    ax2.set_title('Window State')
    ax3.set_title('Mean Filter')
    ax4.set_title('Z-Score Filter')
    #fig.legend()
    fig.savefig(fname='plots/indoor_hum_' + filename + '.png')
    plt.show()


def plotFiltersCO2():
    # plot co2, real window state, filters
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, sharex='all', figsize=(10, 10))

    m_co2 = peak_detection.mean_algo(np.array(data["CO2"]), algoSettings.co2_lag, algoSettings.co2_threshold)
    z_co2 = \
        peak_detection.thresholding_algo(np.array(data["CO2"]), peak_detection.co2_lag, peak_detection.co2_threshold,
                                         peak_detection.co2_influence)['signals']
    acc_res = AlgoChecker.get_results(filename)

    ax1.plot(data["time"], data["CO2"], label='indoor rhum', color='blue', linewidth=2)
    ax2.plot(data["time"], data["windowState"], label='window state', color='red', linewidth=2)
    ax3.plot(data["time"], m_co2, label='mean filter, acc: ' + str('%.2f' % acc_res["mean_co2"]["acc"]),
             color='darkblue', linewidth=2)
    ax4.plot(data["time"], z_co2, label='z-score filter, acc: ' + str('%.2f' % acc_res["thresholding_co2"]["acc"]),
             color='darkgreen', linewidth=2)

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

    fig.autofmt_xdate()

    ax1.set_title('Indoor CO2 Level')
    ax2.set_title('Window State')
    ax3.set_title('Mean Filter')
    ax4.set_title('Z-Score Filter')
    fig.legend()

    fig.savefig(fname='plots/indoor_co2_' + filename + '.png')

    plt.show()

plotFiltersHum()
#plotFiltersCO2()
#plot1()
print(AlgoChecker.get_results(filename))