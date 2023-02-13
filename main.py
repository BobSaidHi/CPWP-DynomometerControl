# Imports
import pyvisa
import odriveMotorController
import easy_scpi as scpi
from odriveMotorController import odriveMotorController

# https://pypi.org/project/easy-scpi/
# https://pyvisa.readthedocs.io/en/latest/introduction/configuring.html

# Keysight / Agilent Technologies VISA
#KATVisaRM = pyvisa.highlevel.ResourceManager("C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll")
KATVisaRM = pyvisa.highlevel.ResourceManager()
print("Keysight / Agilent Technologies VISA:", KATVisaRM.visalib)
print("Keysight / Agilent Technologies VISA Resources:", KATVisaRM.list_resources())

# National Instruments VISA
NI_VISA = 'C:\\Windows\\system32\\visa32.dll'
NIVisaRM = pyvisa.highlevel.ResourceManager(NI_VISA)
print("National Instruments VISA:", NIVisaRM.visalib)
print("National Instruments VISA Resources:", NIVisaRM.list_resources())

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

