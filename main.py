# Imports - Logging
import logger
import logging

# Imports - Control
from odriveMotorController import odriveMotorController
import easy_scpi as scpi
import pyvisa

# Start Logger
logger = logging.getLogger("DynamometerControl")
logger.setLevel(logging.DEBUG)

# https://pypi.org/project/easy-scpi/
# https://pyvisa.readthedocs.io/en/latest/introduction/configuring.html

# Keysight / Agilent Technologies VISA
#KATVisaRM = pyvisa.highlevel.ResourceManager("C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll")
KATVisaRM = pyvisa.highlevel.ResourceManager()
logger.debug("Keysight / Agilent Technologies VISA: " + str(KATVisaRM.visalib))
logger.debug("Keysight / Agilent Technologies VISA Resources: " + str(KATVisaRM.list_resources()))

# National Instruments VISA
NI_VISA = 'C:\\Windows\\system32\\visa32.dll'
NIVisaRM = pyvisa.highlevel.ResourceManager(NI_VISA)
logger.debug("National Instruments VISA: " + str(NIVisaRM.visalib))
logger.debug("National Instruments VISA Resources: " + str(NIVisaRM.list_resources()))

# Connect to & Configure Power supply
powerSupply = scpi.Instrument(port=None)

# Connect to & Configure Odrive motor controller
motor1 = odriveMotorController()
#motor1.configure()
motor1.verifyConfig()

# Connect to & Configure Multimeter
multimeter = scpi.Instrument(port=None)

# Connect to & Configure Digital Load
load = scpi.Instrument(port=None, backend=NI_VISA)

# To start:
# odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

