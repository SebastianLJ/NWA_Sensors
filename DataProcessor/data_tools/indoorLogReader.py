import csv
from datetime import datetime
import os.path


def read_file(filename):
    time = []
    avghum = []
    rhum = []
    temp = []
    windowState = []
    window = []
    carbondioxide = []
    tVOC = []
    with open(os.path.dirname(__file__) + '/../data/new_data/' + filename + '.csv', 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            time.append(datetime.strptime(row[0], '%H:%M:%S'))
            rhum.append(float(row[1]))
            avghum.append(float(row[2]))
            temp.append(float(row[3]))
            windowState.append(float(row[4]))
            if int(row[4]) == 1:
                window.append(float(row[2]))
            else:
                window.append(None)
            carbondioxide.append(float(row[5]))
            tVOC.append(float(row[6]))
    return dict(time=time,
                rHum=rhum,
                avgHum=avghum,
                temp=temp,
                windowState=windowState,
                window=window,
                CO2=carbondioxide,
                tVOC=tVOC)