# threshold algorithm implemented in python by R Kiselev
# https://stackoverflow.com/questions/22583391/peak-signal-detection-in-realtime-timeseries-data/43512887#43512887

import numpy as np

# rhum settings for z-score
rhum_lag = 100
rhum_threshold = 4
rhum_influence = 0.5
# co2 settings for z-score
co2_lag = 100
co2_threshold = 6
co2_influence = 0.5

def mean_algo(y,lag, threshold):
    signals = np.zeros(len(y))
    for i in range(lag, len(y)):
        mean = np.mean(y[i-lag:i+1])
        if mean - y[i] > threshold:
            signals[i] = 1
        else:
            signals[i] = 0
    return np.asarray(mean_clean_up(signals))


def mean_clean_up(signals):
    clean_signals = np.zeros(len(signals))
    for i in range(len(signals)):
        if signals[i] != 0:
            start = i
            end = i
            for j in range(i + 1, i+200):
                if j < len(signals) and signals[j] != 0:
                    end = j
                    break
            clean_signals[start:end + 1] = 1
    return clean_signals


def standard_score_algo(y, lag, threshold, influence):
    signals = np.zeros(len(y))
    filteredY = np.array(y)
    avgFilter = [0]*len(y)
    stdFilter = [0]*len(y)
    avgFilter[lag - 1] = np.mean(y[0:lag])
    stdFilter[lag - 1] = np.std(y[0:lag])
    for i in range(lag, len(y)):
        if avgFilter[i-1] - y[i] > threshold * stdFilter [i-1]:
            signals[i] = 1
            filteredY[i] = influence * y[i] + (1 - influence) * filteredY[i-1]
        else:
            signals[i] = 0
            filteredY[i] = y[i]
        avgFilter[i] = np.mean(filteredY[(i - lag + 1):i + 1])
        stdFilter[i] = np.std(filteredY[(i - lag + 1):i + 1])

    return dict(signals = np.asarray(signals),
                avgFilter = np.asarray(avgFilter),
                stdFilter = np.asarray(stdFilter))
