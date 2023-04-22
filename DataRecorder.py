# Imports - Logging
import logger
import logging

# Start Logger
logger = logging.getLogger("DynamometerControl")
logger.setLevel(logging.DEBUG)

# Other imports
import csv
from  datetime import datetime as datetime

class DataRecorder:
    def __init__(self):
        current_time = datetime.now().strftime('%Y-%m-%d__%H-%M-%S')
        self.filePath = "output/data-" + current_time + ".csv"
        logger.info("Saving data to :" + self.filePath)
        self.data_file = open(self.filePath, mode='w')
        self.data_writer = csv.writer(self.data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        self.data_writer.writerow(['Timestamp (ISO8601 - YYYY:MM:DDThh:mm:ss+/-TimeZoneOffset)', 'Timestamp (POSIX in s)', 'Voltage (Volts)', 'Current (Amps)'])

    def write_data(self, voltage, current):
        """
        @param voltage
        @param current
        """
        current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        current_timestamp = datetime.utcnow().timestamp()
        logger.debug("Saved data: " + current_time + ", " + str(current_timestamp) + ", "+ str(voltage)  + ", " + str(current))
        self.data_writer.writerow([current_time, current_timestamp, voltage, current])

    def close_file(self):
        logger.debug("Closed data file")
        self.data_file.close()

