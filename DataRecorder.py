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
    def __init__(self, PS_ENABLE= False, MULTIMETER_ENABLE = False, LOAD_ENABLE = False, CONTROLLER_ENABLE = True):
        self.PS_ENABLE = PS_ENABLE
        self.MULTIMETER_ENABLE = MULTIMETER_ENABLE
        self.LOAD_ENABLE = LOAD_ENABLE
        self.CONTROLLER_ENABLE = CONTROLLER_ENABLE

        current_time = datetime.now().strftime('%Y-%m-%d__%H-%M-%S')
        self.filePath = "output/data-" + current_time + ".csv"
        logger.info("Saving data to :" + self.filePath)
        self.data_file = open(self.filePath, mode='w')
        self.data_writer = csv.writer(self.data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        header = ['Timestamp (ISO8601 - YYYY:MM:DDThh:mm:ss+/-TimeZoneOffset)', 'Timestamp (POSIX in s)']
        if PS_ENABLE:
            header.append('Power Supply Voltage (Volts)')
            header.append('Power Supply Current (Amps)')
        if MULTIMETER_ENABLE:
            raise NotImplementedError
        if LOAD_ENABLE:
            raise NotImplementedError
        if CONTROLLER_ENABLE:
            header.append('Odrive Dc Bus Voltage (Volts)')
            header.append('Odrive Dc Bus Current (Amps)')
        logger.debug("Data header as list: " + str(header))
        self.data_writer.writerow(header)

    def write_data(self, ps_voltage=-1, ps_current=-1, odrive_bus_voltage=-1, odrive_bus_current = -1):
        """
        @param voltage
        @param current
        """
        current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        current_timestamp = datetime.utcnow().timestamp()
        logger.debug("Saved data: " + current_time + ", " + str(current_timestamp) + ", " + str(ps_voltage) + ", " + str(ps_current) + ", " + str(odrive_bus_voltage)  + ", " + str(odrive_bus_current))
        
        output = [current_time, current_timestamp]
        if self.PS_ENABLE:
            output.append(ps_voltage)
            output.append(ps_current)
        if self.MULTIMETER_ENABLE:
            raise NotImplementedError
        if self.LOAD_ENABLE:
            raise NotImplementedError
        if self.CONTROLLER_ENABLE:
            output.append(odrive_bus_voltage)
            output.append(odrive_bus_current)
        self.data_writer.writerow(output)

    def close_file(self):
        logger.debug("Closed data file")
        self.data_file.close()

