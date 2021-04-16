from data_tools import indoorLogReader

filename = 'indoor_2021-04-16_09-48-58'
# delay in seconds
arduino_delay = 5

data = indoorLogReader.read_file(filename)
