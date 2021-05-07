import numpy as np
from data_tools import indoorLogReader
from signal_processing import peak_detection

# delays in seconds
arduino_delay = 5
aceptable_delay = 90

files = ['indoor_2021-04-16_09-48-58', 'indoor_2021-04-19_09-42-42', 'indoor_2021-04-15_14-59-05']


def get_results(filename):
    data = indoorLogReader.read_file(filename)

    return dict(mean_rhum=get_relative_acc(data, peak_detection.mean_algo(data["rHum"], 100, 2)),
                mean_co2=get_relative_acc(data, peak_detection.mean_algo(data["CO2"], 10, 100)),
                thresholding_rhum=get_relative_acc(data, peak_detection.thresholding_algo(np.array(data["rHum"]),
                                                                                          peak_detection.rhum_lag,
                                                                                          peak_detection.rhum_threshold,
                                                                                          peak_detection.rhum_influence)[
                                                  "signals"]),
                thresholding_co2=get_relative_acc(data, peak_detection.thresholding_algo(np.array(data["CO2"]),
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


# can only increment tp once per window
def get_relative_acc(data, alg_result):
    tp, fp, tn, fn = 0, 0, 0, 0
    correct = False
    time_since_last_fp = 0
    start_sat, end_sat = False, False
    start, end = 0, 0
    # tp and fn
    for i in range(len(data["windowState"])):
        if data["windowState"][i] == 1 and alg_result[i] != 0 and not correct:
            correct = True
            tp += 1
        elif data["windowState"][i - 1] == 1 and data["windowState"][i] == 0 and not correct:
            fn += 1

        elif data["windowState"][i] == 0 and correct:
            correct = False

        if data["windowState"][i] == 0 and not start_sat:
            start = i
            start_sat = True

        if i > start and data["windowState"][i-1] == 0 and (data["windowState"][i] == 1 or i == len(data["windowState"])-1):
            end = i
            end_sat = True
        if start_sat and end_sat:
            fi = np.where(alg_result[start:end] == 0)[0][0]
            s = np.sum(alg_result[start+fi:end])
            if s == 0:
                tn += 1
            start_sat = False
            end_sat = False

    for i in range(len(alg_result)):
        # fp test
        if alg_result[i] != 0:
            correct = False
            for j in range(i - int((5 * 60) / arduino_delay), i+1):
                if j > 0 and data["windowState"][j] == 1:
                    correct = True
                    break
            if not correct and time_since_last_fp > 60:
                fp += 1
                time_since_last_fp = 0
        time_since_last_fp += arduino_delay

    return get_conf_matrix(tp, fp, tn ,fn)

def get_true_acc(data, alg_result):
    tp, fp, tn, fn = 0, 0, 0, 0
    window = data["windowState"]
    for i in range(len(alg_result)):
        if alg_result[i] == 0 and window[i] == 0:
            tn += 1
        elif alg_result[i] == 0 and window[i] == 1:
            fn += 1
        elif alg_result[i] != 0 and window[i] == 0:
            fp += 1
        elif alg_result[i] != 0 and window[i] == 1:
            tp += 1

    return get_conf_matrix(tp, fp, tn ,fn)

def get_conf_matrix(tp, fp, tn ,fn):
    cm = dict(tp=tp, fp=fp, tn=tn, fn=fn)
    cm["tpr"] = tp / (tp + fn)
    cm["tnr"] = tn / (tn + fp)
    cm["ppv"] = tp / (tp + fp)
    cm["acc"] = (tp + tn) / (tp + tn+ fp + fn)
    return cm
