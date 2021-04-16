import numpy as np
from data_tools import indoorLogReader
import peak_detection

filename = 'indoor_2021-04-16_09-48-58'
# delays in seconds
arduino_delay = 5
aceptable_delay = 90



def get_results(filename):
    data = indoorLogReader.read_file(filename)

    return dict(mean_alg=getAcc(data, peak_detection.mean_algo(data["rHum"], 100, 2)),
                thresholding_algo=getAcc(data, peak_detection.thresholding_algo(np.array(data["rHum"]),50,20,0.2)["signals"]))


def getAcc(data, alg_result):
    tp, fp, tn, fn = 0, 0, 0, 0

    skip_to_next = False
    correct = False
    # tp and fn teset
    for i in range(len(data["windowState"])):
        if data["windowState"][i] == 1 and not correct:
            for j in range(i, i + int(aceptable_delay/arduino_delay)+1):
                if alg_result[j] != 0:
                    correct = True
                    tp += 1
                    break
            if not correct: fn += 1
        elif data["windowState"][i] == 0 and correct:
            correct = False

    for i in range(len(alg_result)):
        # fp test
        if alg_result[i] != 0:
            correct = False
            for j in range(i-arduino_delay*100, i+1):
                if j > 0 and data["windowState"][j] == 1:
                    correct = True
                    break
            if not correct: fp += 1

    return dict(tp=tp,
                fp=fp,
                tn=tn,
                fn=fn,
                acc=(tp+tn)/(tp+tn+fp+fn))

