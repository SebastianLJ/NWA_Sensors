import serial
from datetime import datetime
import csv

ser = serial.Serial('COM4')
ser.flushInput()
now = datetime.now()
part1 = datetime.now().strftime("%Y-%m-%d")
part2 = datetime.now().strftime("%H-%M-%S")

while True:
    try:
        ser_bytes = ser.readline()
        decoded_bytes = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
        print(decoded_bytes)
        with open(part1 + "_" + part2 + ".csv","a", buffering=1) as f:
            writer = csv.writer(f,delimiter=",")
            writer.writerow([datetime.now().strftime("%H:%M:%S"),decoded_bytes])
    except:
        print("Keyboard Interrupt")
        break