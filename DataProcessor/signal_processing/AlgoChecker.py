import numpy as np
from data_tools import indoorLogReader
from signal_processing import peak_detection

# delays in seconds
arduino_delay = 5
aceptable_delay = 90

files = ['indoor_2021-04-16_09-48-58', 'indoor_2021-04-19_09-42-42']


def get_results(filename):
    data = indoorLogReader.read_file(filename)

    return dict(mean_rhum=getAcc(data, peak_detection.mean_algo(data["rHum"], 100, 2)),
                mean_co2=getAcc(data, peak_detection.mean_algo(data["rHum"], 100, 2)),
                thresholding_rhum=getAcc(data,
                                              peak_detection.thresholding_algo(np.array(data["rHum"]),
                                                                               peak_detection.rhum_lag,
                                                                               peak_detection.rhum_threshold,
                                                                               peak_detection.rhum_influence)[
                                                  "signals"]),
                thresholding_co2=getAcc(data,
                                             peak_detection.thresholding_algo(np.array(data["CO2"]),
                                                                              peak_detection.co2_lag,
                                                                              peak_detection.co2_threshold,
                                                                              peak_detection.co2_influence)["signals"]))

def get_results_arr(filenames):
    x = ("tp", "fp", "tn", "fn")
    algs = ("mean_rhum", "mean_co2", "thresholding_rhum", "thresholding_co2")
    res = dict.fromkeys(algs,dict.fromkeys(x,0))
    for fname in filenames:
        y = get_results(fname)
        for i in range(0,len(algs)):
            res[algs[i]] = {k: res[algs[i]].get(k, 0) + y[algs[i]].get(k, 0) for k in set(y[algs[i]])}

    for i in range(0, len(algs)):
        res[algs[i]]["acc"] = (res[algs[i]]["tp"] + res[algs[i]]["tn"]) / \
                              (res[algs[i]]["tp"] + res[algs[i]]["tn"] + res[algs[i]]["fp"] + res[algs[i]]["fn"])

    return res


def getAcc(data, alg_result):
    tp, fp, tn, fn = 0, 0, 0, 0

    skip_to_next = False
    correct = False
    time_since_last_fp = 0
    # tp and fn teset
    for i in range(len(data["windowState"])):
        if data["windowState"][i] == 1 and alg_result[i] == -1 and not correct:
            correct = True
            tp += 1
        elif data["windowState"][i - 1] == 1 and data["windowState"][i] == 0 and not correct:
            fn += 1

        if data["windowState"][i] == 0 and correct:
            correct = False

    for i in range(len(alg_result)):
        # fp test
        if alg_result[i] == -1:
            correct = False
            for j in range(i - arduino_delay * 120, i + 1):
                if j > 0 and data["windowState"][j] == 1:
                    correct = True
                    break
            if not correct and time_since_last_fp > 60:
                fp += 1
                time_since_last_fp = 0
        time_since_last_fp += arduino_delay

    return dict(tp=tp,
                fp=fp,
                tn=tn,
                fn=fn,
                acc=(tp + tn) / (tp + tn + fp + fn))

print(get_results_arr(files))