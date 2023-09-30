"""
ElectronicLoad.py
Control a VISA compatible electronic load with SCPI over USB

@author BSI

This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

# Imports - logger
import logging
import logger

# Imports - exit handling
from sys import exit as sys_exit

# Imports - delays
from time import sleep as time_sleep

# Imports - control
import easy_scpi as scpi
import pyvisa


# Start Logger
logger = logging.getLogger("DynamometerControl")
logger.setLevel(logging.DEBUG)

# easy_scpi Docs: https://pypi.org/project/easy-scpi/
"""
# TODO: Figure out how to extend Python classes?s
class SDL1020X(scpi.Instrument):
    def __init__(self):
        pass
"""

class SDL1020X:
    """
    Control a Siglent SDL1020X-E 200W electronic load via SCPI over USB

    @author BSI
    """
    def __init__(self, port):
        """
        Wrapper object for easy_scpi.Instrument object to control a Siglent SDL1020X-E 200W electronic load over SCPI
        Does not auto configure the instrument
        
        @param port (String) USB port to connect to
        """
        # Connect to Electronic load
        try:
            self.instrument = scpi.Instrument(port=port)
            #ps = KATVisaRM.open_resource("")
            self.instrument.connect()
        except pyvisa.errors.VisaIOError as e:
            logger.fatal("Failed to connect to power supply: " + str(e))
            sys_exit(-1)
            #raise e
        # Get PS information
        logger.info("Connected to: " + self.instrument.query("*IDN?"))
        logger.debug("Power supply last self test results: " + self.instrument.query("**TST?")) # NOt used?

        # It doesn't support displaying messages :(

        raise NotImplementedError

    # Configure
    def configureConstantResistance(self, resistance, currentRange, voltageRange, resistorRange):
        """
        @param resistorRange {LOW | MIDDLE | HIGH | UPPER}
        """
        self.EL_static_mode = "CR"
        logger.info("Electronic static mode: " + str(self.EL_static_mode))
        self.EL_resistance = resistance
        logger.info("Target electronic load resistance: " + str(self.EL_resistance))
        self.EL_currentRange = currentRange
        logger.info("Target electronic load current range: " + str(self.EL_currentRange))
        self.EL_voltageRange = voltageRange
        logger.info("Target electronic load voltage range: " + str(self.EL_voltageRange))
        self.EL_resistorRange = resistorRange
        logger.info("Target electronic load resistor range: " + str(self.EL_resistorRange))

        self.instrument.write(":SOURce:FUNCtion ") + str(self.EL_static_mode)
        self.instrument.write(":SOURce: RESistance:LEVel:IMMediate ") + str(self.EL_resistance)
        self.instrument.write(":SOURce:RESistance:IRANGe ") + str(self.EL_currentRange)
        self.instrument.write(":SOURce:RESistance:VRANGe ") + str(self.EL_voltageRange)
        self.instrument.write(":SOURce:RESistance:RRANGe ") + str(self.EL_resistorRange)

        self.EL_OCP = "ON"
        logger.info("Target Electronic load OCP: " + str(self.EL_OCP))
        self.instrument.write(":SOURce:CURRent:PROTection:STATe ") + str(self.EL_OCP)
        raise NotImplementedError
    
        # TODO: Left off on pg 52

    # Verify configurations
    def verifyConfig(self):
        logger.debug("Electronic load CR resistor value: " + str(self.instrument.query(":SOURce:FUNCtion?")))
        logger.debug("Electronic load CR resistor value: " + str(self.instrument.query(":SOURce:RESistance:LEVel:IMMediate?")))
        logger.debug("Electronic load CR current range value: " + str(self.instrument.query(":SOURce:RESistance:IRANGe?")))
        logger.debug("Electronic load CR voltage range value: " + str(self.instrument.query(":SOURce:RESistance:VRANGe?")))
        logger.debug("Electronic load CR resistor range value: " + str(self.instrument.query(":SOURce:RESistance:RRANGe?")))

        logger.debug("Electronic load OCP state: " + self.powerSupply.query(":SOURce:CURRent:PROTection:STATe?")) # Not sure, this wasn't how it was in the manuel but it makes more since
        
        # Verify parameters
        logger.debug("Power supply Ch. 1 OCP value: " + self.powerSupply.query(":OUTP:OCP:VAL? CH1"))
        logger.debug("Power supply Ch. 1 OVP state: " + self.powerSupply.query(":OUTP:OVP? CH1"))
        logger.debug("Power supply Ch. 1 OVP value: " + self.powerSupply.query(":OUTP:OVP:VAL? CH1"))    
        logger.debug("Power supply OTP state: " + self.powerSupply.query(":SYSTem:OTP?"))
        logger.debug("Power supply system version: " + self.powerSupply.query(":SYSTem:VERSion?"))
        
        raise NotImplementedError # TODO

    # Control
    def enable(self):
        """
        Enable the input of the electronic load.  Make sure it is configured first.
        """
        logger.info("Turning the load input on.")
        self.instrument.write(":SOURce:INPut:STATe ON")

    def disable(self):
        """
        Disables the input of the electronic load
        """
        logger.info("Turning the load input off.")
        self.instrument.write(":SOURce:INPut:STATe OFF")

    # Get data
    def getLoadVoltage(self):
        """
        Fetches the input voltage from the electronic load

        @returns the input voltage from the electronic load
        """
        self.load_voltage = self.instrument.query(":MEASure:VOLTage:DC?")
        logger.debug("Electronic load voltage : " + str(self.load_voltage))
        return self.load_voltage

    def getLoadCurrent(self):
        """
        Fetches the input current from the electronic load

        @returns the input current from the electronic load
        """
        self.load_current = self.instrument.query(":MEASure:CURRent:DC?")
        logger.debug("Electronic load current : " + str(self.load_current))
        return self.load_current
    
    def getLoadPower(self):
        """
        Fetches the input power from the electronic load

        @returns the input power  from the electronic load
        """
        self.load_power = self.instrument.query(":MEASure:POWer:DC?")
        logger.debug("Electronic load current : " + str(self.load_power))
        return self.load_power

    def getLoadResistance(self):
        """
        Fetches the input power from the electronic load

        @returns the input power  from the electronic load
        """
        self.load_resistance = self.instrument.query(":MEASure:POWer:DC?")
        logger.debug("Electronic load current : " + str(self.load_resistance))
        return self.load_resistance

    def testStepNumber(self):
        """
        "Query the number of running step in the LIST/PROGRAM test sequence."

        @returns "the number of running step in the LIST/PROGRAM test sequence."
        """
        self.load_step_number = self.instrument.query(":SOURce:TEST:STEP?")
        logger.debug("Electronic step number: " + str(self.load_step_number))
        return self.load_step_number

