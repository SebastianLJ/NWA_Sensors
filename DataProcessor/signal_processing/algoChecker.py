import numpy as np
from data_tools import logReader
from signal_processing import algorithms, algoSettings

# delays in seconds
arduino_delay = 5
aceptable_delay = 90


def get_results(filename):
    data = logReader.readFile(filename)

    return dict(mean_rhum=get_relative_acc(data, algorithms.mean_algo(data["rHum"],
                                                                      algoSettings.hum_lag,
                                                                      algoSettings.hum_threshold)),
                mean_co2=get_relative_acc(data, algorithms.mean_algo(data["CO2"],
                                                                     algoSettings.co2_lag,
                                                                     algoSettings.co2_threshold)),
                thresholding_rhum=get_relative_acc(data, algorithms.standard_score_algo(np.array(data["rHum"]),
                                                                                        algorithms.rhum_lag,
                                                                                        algorithms.rhum_threshold,
                                                                                        algorithms.rhum_influence)[
                                                  "signals"]),
                thresholding_co2=get_relative_acc(data, algorithms.standard_score_algo(np.array(data["CO2"]),
                                                                                       algorithms.co2_lag,
                                                                                       algorithms.co2_threshold,
                                                                                       algorithms.co2_influence)["signals"]))

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
            matches = np.where(alg_result[start:end] == 0)
            if matches[0].size > 0:
                fi = matches[0][0]
                s = np.sum(alg_result[start+fi:end])
            else:
                s = 0
            if s == 0:
                tn += 1
            start_sat = False
            end_sat = False

    for i in range(len(alg_result)):
        # fp test
        if alg_result[i] != 0 and alg_result[i-1] == 0 and data["windowState"][i] == 0:
            fp += 1

    return get_conf_matrix(tp, fp, tn, fn)


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

    return get_conf_matrix(tp, fp, tn, fn)


def get_conf_matrix(tp, fp, tn ,fn):
    cm = dict(tp=tp, fp=fp, tn=tn, fn=fn)
    if tp + fn > 0:
        cm["tpr"] = tp / (tp + fn)
    else:
        cm["tpr"] = 0
    if tn + fp > 0:
        cm["tnr"] = tn / (tn + fp)
    else:
        cm["tnr"] = 0
    if tp + fp > 0:
        cm["ppv"] = tp / (tp + fp)
    else:
        cm["ppv"] = 0
    if tp + tn + fp+ fn > 0:
        cm["acc"] = (tp + tn) / (tp + tn+ fp + fn)
    else:
        cm["acc"] = 0
    return cm
