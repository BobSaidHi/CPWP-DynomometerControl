# Imports - Logging
import logger
import logging

# Imports - Handle exiting
from sys import exit as sys_exit

# Start Logger
logger = logging.getLogger("DynamometerControl")
logger.setLevel(logging.DEBUG)

## CONFIG
CONTROLLER_ENABLE = True
PS_ENABLE = False
MULTIMETER_ENABLE = False
LOAD_ENABLE = False
#TEST_MODE = "DYNO"
TEST_MODE = "TUNNEL"

logger.info("Test Config: CONTROLLER_ENABLE=%s, PS_ENABLE=%s, MULTIMETER_ENABLE=%s, LOAD_ENABLE=%s", CONTROLLER_ENABLE, PS_ENABLE, MULTIMETER_ENABLE, LOAD_ENABLE)

# Imports - Control
if CONTROLLER_ENABLE:
    logger.debug("Importing odriveMotorController")
    from odriveMotorController import odriveMotorController
if PS_ENABLE or MULTIMETER_ENABLE or LOAD_ENABLE:
    logger.debug("Importing easy_scpi and pyvisa")
    import easy_scpi as scpi
    import pyvisa
    if PS_ENABLE:
        logger.debug("Importing powerSupply")
        from powerSupply import DP832

# Imports - data handling
from DataRecorder import DataRecorder
recorder = DataRecorder()
recorder.write_data(-1.9, -1.3)

# Warn if PS Control unavailable
if (not PS_ENABLE) and CONTROLLER_ENABLE:
    logger.warning("Controller enabled without power supply!  Power shutoff on error unavailable.")

# VISA Configuration
if PS_ENABLE or MULTIMETER_ENABLE or LOAD_ENABLE:
    # VISA Configuration
    # TODO: Unended if using easy_scpi
    # https://pypi.org/project/easy-scpi/
    # https://pyvisa.readthedocs.io/en/latest/introduction/configuring.html

    # Keysight / Agilent Technologies VISA
    if PS_ENABLE or MULTIMETER_ENABLE:
        #KATVisaRM = pyvisa.highlevel.ResourceManager("C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll")
        KATVisaRM = pyvisa.highlevel.ResourceManager()
        #a = pyvisa.ResourceManager() #? # Alt method? # TODO

        logger.info("Keysight / Agilent Technologies VISA: " + str(KATVisaRM.visalib))
        logger.info("Keysight / Agilent Technologies VISA Resources: " + str(KATVisaRM.list_resources()))

    # National Instruments VISA
    if LOAD_ENABLE:
        NI_VISA = 'C:\\Windows\\system32\\visa32.dll'
        NIVisaRM = pyvisa.highlevel.ResourceManager(NI_VISA)
        logger.info("National Instruments VISA: " + str(NIVisaRM.visalib))
        logger.info("National Instruments VISA Resources: " + str(NIVisaRM.list_resources()))


    # Connect to & Configure Power supply
    if PS_ENABLE:
        powerSupply = DP832("USB0", 12.0, 3.0)
        powerSupply.enable()

def PSSafeShutdown():
    if PS_ENABLE:
        powerSupply.disable()
    else:
        logger.critical("Power Supply control not enabled.  FAILED TO SHUTOFF POWER.")

# Connect to & Configure Odrive motor controller
if CONTROLLER_ENABLE:
    try:
        motor1 = odriveMotorController()
        #motor1.configure() #TODO
        motor1.verifyConfig()
    except AttributeError as e:
        logger.fatal("Failed to connect to odrive controller: " + str(e))
        logger.info("Shutting off the power supply.")
        PSSafeShutdown()
        sys_exit(-1)
    except NotImplementedError as e:
        logger.fatal("Error when connecting odrive controller du to incomplete script (Yes, you may blame programming this time): " + str(e))
        logger.info("Shutting off the power supply.")
        PSSafeShutdown()
        sys_exit(-1)

def ControllerSafeShutdown():
    ## TODO: Verify that this is correct
    if CONTROLLER_ENABLE:
        motor1.stop()

# Connect to & Configure Multimeter
if MULTIMETER_ENABLE:
    multimeter = scpi.Instrument(port=None)
    # TODO: finish

# Connect to & Configure Digital Load
if LOAD_ENABLE:
    load = scpi.Instrument(port=None, backend=NI_VISA)
    # TODO: finish

# Prepare data collection
recorder = DataRecorder()

# To start:
if CONTROLLER_ENABLE:
    if TEST_MODE == "DYNO":
        raise NotImplementedError
        try:
            motor1.startSensorless()
        except SystemExit as e:
            logger.debug("Failed to start motor: " + str(e))
            logger.info("Shutting off the power supply.")
            PSSafeShutdown()
            sys_exit(-1)
        # TODO: finish
    elif TEST_MODE == "TUNNEL":
        try:
            motor1.startSensorless()
        except SystemExit as e:
            logger.debug("Failed to start motor: " + str(e))
            logger.info("Shutting off the power supply.")
            PSSafeShutdown()
            sys_exit(-1)

# Main loop
#"""

#"""


try:
    while True:
        if CONTROLLER_ENABLE:
            recorder.write_data(motor1.getDCBusVoltage(), motor1.getDCBusCurrent())
        if PS_ENABLE:
            powerSupply.updateOutputStats()
            powerSupply.getOutputVoltage()
            powerSupply.getOutputCurrent()
            powerSupply.getOutputPower()
except KeyboardInterrupt as e :
    logger.fatal("Shutting down due to keyboard Interrupt: ", e)
    ControllerSafeShutdown()
    PSSafeShutdown()

