import pyvisa
import odrive
#import simple

#rm = pyvisa.ResourceManager()
#print(rm.list_resources())

# National Instruments VISA
NIVisaRM = pyvisa.highlevel.ResourceManager('C:\\Windows\\system32\\visa32.dll')
print("National Instruments VISA:", NIVisaRM.visalib)
print("National Instruments VISA Resources:", NIVisaRM.list_resources())

# Keysight / Agilent Technologies VISA
#KATVisaRM = pyvisa.highlevel.ResourceManager("C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll")
KATVisaRM = pyvisa.highlevel.ResourceManager()
print("Keysight / Agilent Technologies VISA:", KATVisaRM.visalib)
print("Keysight / Agilent Technologies VISA Resources:", KATVisaRM.list_resources())
#KATVisaRM = pyvisa.highlevel.ResourceManager('C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\ktvisa\\ktbin\\visa32.dll')

#IVIVisaRM = pyvisa.highlevel.ResourceManager('C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\bin\\NiViUsb.dll')
#NIVisaRM = pyvisa.highlevel.ResourceManager('C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\NIvisa')

