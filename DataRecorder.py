"""
DataRecorder.py
Saves test data to a file.

@author BSI

This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

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
    """
    Saves test data to a file.

    @author BSI
    """
    def __init__(self, PS_ENABLE= False, MULTIMETER_ENABLE = False, LOAD_ENABLE = False, CONTROLLER_ENABLE = True):
        """
        Create an object to record data to a file.  File will be created in /output and will have a time-based filename
        @param PS_ENABLE: True to accept and log data from a power supply, False to not
        @param MULTIMETER_ENABLE: True to accept and log data from a multimeter, False to not
        @param LOAD_ENABLE: True to accept and log data from an electronic load, False to not
        @param CONTROLLER_ENABLE: True to accept and log data from a motor controller, False to not
        """
        # Update instance variables
        self.PS_ENABLE = PS_ENABLE
        self.MULTIMETER_ENABLE = MULTIMETER_ENABLE
        self.LOAD_ENABLE = LOAD_ENABLE
        self.CONTROLLER_ENABLE = CONTROLLER_ENABLE

        # Create file to save data to
        current_time = datetime.now().strftime('%Y-%m-%d__%H-%M-%S')
        self.filePath = "output/data-" + current_time + ".csv"
        logger.info("Saving data to :" + self.filePath)
        self.data_file = open(self.filePath, mode='w')
        self.data_writer = csv.writer(self.data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Add column headers to file
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
        Records data to the file opened in __init__
        Ensure that the parameters being passed match what is enabled in __init__

        @param ps_voltage
        @param ps_current
        @param odrive_bus_voltage
        @param odrive_bus_current
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
        """
        Closes the file opened in __init__
        """
        logger.debug("Closed data file")
        self.data_file.close()

