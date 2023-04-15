# Imports - Logging
import logger
import logging

# Imports - Handle exiting
from sys import exit as sys_exit

# Imports - Control
from odriveMotorController import odriveMotorController
import easy_scpi as scpi
import pyvisa
from powerSupply import DP832


# Start Logger
logger = logging.getLogger("DynamometerControl")
logger.setLevel(logging.DEBUG)

# VISA Configuration
# TODO: Unended if using easy_scpi
# https://pypi.org/project/easy-scpi/
# https://pyvisa.readthedocs.io/en/latest/introduction/configuring.html

# Keysight / Agilent Technologies VISA
#KATVisaRM = pyvisa.highlevel.ResourceManager("C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll")
KATVisaRM = pyvisa.highlevel.ResourceManager()
#a = pyvisa.ResourceManager() #? # Alt method? # TODO

logger.info("Keysight / Agilent Technologies VISA: " + str(KATVisaRM.visalib))
logger.info("Keysight / Agilent Technologies VISA Resources: " + str(KATVisaRM.list_resources()))

# National Instruments VISA
NI_VISA = 'C:\\Windows\\system32\\visa32.dll'
NIVisaRM = pyvisa.highlevel.ResourceManager(NI_VISA)
logger.info("National Instruments VISA: " + str(NIVisaRM.visalib))
logger.info("National Instruments VISA Resources: " + str(NIVisaRM.list_resources()))


# Connect to & Configure Power supply
powerSupply = DP832("USB0", 12.0, 3.0)
powerSupply.enable()

# Connect to & Configure Odrive motor controller
try:
    motor1 = odriveMotorController()
    motor1.configure()
    motor1.verifyConfig()
except AttributeError as e:
    logger.fatal("Failed to connect to odrive controller: " + str(e))
    logger.info("Shutting off the power supply.")
    powerSupply.disable() # Turn off the power supply
    sys_exit(-1)
except NotImplementedError as e:
    logger.fatal("Error when connecting odrive controller du to incomplete script (Yes, you may blame programming this time): " + str(e))
    logger.info("Shutting off the power supply.")
    powerSupply.disable() # Turn off the power supply
    sys_exit(-1)

# Connect to & Configure Multimeter
multimeter = scpi.Instrument(port=None)
# TODO: finish

# Connect to & Configure Digital Load
load = scpi.Instrument(port=None, backend=NI_VISA)
# TODO: finish

# To start:

"""s
try:
    motor1.startSensorless()
except SystemExit as e:
    logger.debug("Failed to start motor: " + str(e))
    logger.info("Shutting off the power supply.")
    powerSupply.disable() # Turn off the power supply
    sys_exit(-1)
#"""
# TODO: finish

# Main loop
#"""
powerSupply.updateOutputStats()
powerSupply.getOutputVoltage()
powerSupply.getOutputCurrent()
powerSupply.getOutputPower()
#"""

# Stop
## TODO: Verify that this is correct
motor1.stop()
powerSupply.disable()

