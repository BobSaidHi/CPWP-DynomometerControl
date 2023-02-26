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
# TODO: Figure out how to extend Pythong classes?s
class DP832(scpi.Instrument):
    def __init__(self):
        pass
"""

class DP832:
    def __init__(self, port, voltage, current):
        """
        Wrapper object for easy_scpi.Instrument object to control a Rigol DP832 power supply over SCPI

        @param port (String) USB port to connect to
        @param voltage target for power supply
        @param current (max?) target for power supply
        """
        # Connect to & Configure Power supply
        try:
            self.powerSupply = scpi.Instrument(port=port) # "USB0"
            #ps = KATVisaRM.open_resource("USB0::6833::3601::DP8C213302983::0::INSTR")
            self.powerSupply.connect()
        except pyvisa.errors.VisaIOError as e:
            logger.fatal("Failed to connect to power supply: " + str(e))
            sys_exit(-1)
            #raise e
        # Get PS information
        logger.info("Connected to: " + self.powerSupply.query("*IDN?"))
        logger.debug("Power supply last self test results: " + self.powerSupply.query("**TST?"))
        logger.debug("Power supply Ch. 1 output mode: " + self.powerSupply.query(":OUTPut:MODE?"))
        logger.debug("Power supply Ch. 1 OCP state: " + self.powerSupply.query(":OUTPut:OCP? CH1"))
        logger.debug("Power supply Ch. 1 OCP value: " + self.powerSupply.query(":OUTP:OCP:VAL? CH1"))
        logger.debug("Power supply Ch. 1 OVP state: " + self.powerSupply.query(":OUTP:OVP? CH1"))
        logger.debug("Power supply Ch. 1 OVP value: " + self.powerSupply.query(":OUTP:OVP:VAL? CH1"))    
        logger.debug("Power supply OTP state: " + self.powerSupply.query(":SYSTem:OTP?"))
        logger.debug("Power supply system version: " + self.powerSupply.query(":SYSTem:VERSion?"))

        # Send a message to be displayed for fun and to make it obvious that it's being remote controlled
        self.powerSupply.write(':DISPlay:TEXT "CONNECTED TO DYNAMOTOR TEST APPLICATION",10,10')
        time_sleep(2)
        self.powerSupply.write(":DISPlay:TEXT:CLEar")

        # Set parameters
        self.PS_VOLTAGE = voltage  # 12.0
        self.PS_CURRENT = current # 3.0
        logger.info("Target power supply voltage: " + self.PS_VOLTAGES_VOLTAGE)
        logger.info("Target power supply current: " + self.PS_CURRENT)
        self.powerSupply.write(":APPLy CH1,12.0,3.0")

        # Verify parameters
        logger.debug("Power supply set to: " + self.powerSupply.query(":APPLy? CH1")) # Get channel 1 voltage and current

    # Control
    def enable(self, bypassVerification=False):
        """
        Prompts for verification if bypassVerification is False and turns channel 1 on
        Skips verification if bypassVerification is True

        @param bypassVerification (Boolean)
        """
        if not bypassVerification:
            print("Ready to enable the power supply.  Continue? (Y/n): ")
            response = input()
            logger.debug('User response to "Ready to enable the power supply.  Continue? (Y/n): " ' + response)
            if not response == 'Y':
                logger.fatal("Power-up canceled by user!")
                #raise KeyboardInterrupt("Power-up canceled by user!")
                sys_exit(-1)
            else:
                logger.debug("Continuing...")
                self.enable(True)
        else:
            logger.info("Turning ps channel 1 on.")
            self.powerSupply.write(":OUTP CH1,ON")

    def disable(self):
        """
        Turns channel 1 off
        """
        self.powerSupply.write(":OUTP CH1,OFF")

    # Get data
    def updateOutputStats(self):
        """
        Fetches the output stats from the power supply
        """
        powerStats = self.powerSupply.query(":MEAS:ALL? CH1")
        logger.debug("Power stats (volts, amps, power:): " + powerStats)
        temp = powerStats.split[',']
        self.output_voltage = temp[0]
        self.output_current = temp[1]
        self.output_power = temp[2]

    def getOutputVoltage(self):
        """
        Fetches the last known output voltage of the power supply

        Run updateOutputStats() to update this value
        """
        return self.output_voltage

    def getOutputCurrent(self):
        """
        Fetches the last known output current of the power supply

        Run updateOutputStats() to update this value
        """
        return self.output_current
    
    def getOutputPower(self):
        """
        Fetches the last known output power of the power supply

        Run updateOutputStats() to update this value
        """
        return self.output_power

