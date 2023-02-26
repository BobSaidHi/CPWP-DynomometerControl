# DynomometerControl

Performs automated dynamometer testing on a generator by controlling & monitoring the following components over USB:

- A VISA compatible power supply (Rigol DP832) using SCPI
- An odrive motor connected to a Odrive Robotics v3.6 controller using the odrive library
- (Optional) A VISA compatible multimeter (Agilent U3606A) using SCPI
- (Recommended) A VISA compatible programable electronic road (Siglent SDL1020X-E) using SCPI

Note that this program is specified to the use case and ignores things a more generic library might include, such as multiple power supply channels

## Key terms

- Virtual Instrument Software architecture (VISA library)
- Standard Commands for Programmable Instruments (SCPI)

## Questions, Comments, and work put off for the future

- pyvisa + SCPI or easy_scpi as API?:  Currently a weird mix of both is used
- Extending scpi.Instrument vs creating a self.[object of scpi.Instrument] 
- NIVisa and/or Keysight VISA?
  - It implies that NIVisa, if not both, or are cross-compatible with other vendors
  - Except Keysight Connection Expert is nice (haven't tried NI MAX)
  - and National Instruments (NI) software causes my computer to crash more
  - Keysight Connection Expert prefers Keysight Visa sometimes
  - The Keysight VISA has some extra libraries that cause it to need extra configuration for pyvisa
  - [See Wikipedia - VISA on compatibility](https://en.wikipedia.org/wiki/Virtual_instrument_software_architecture_
- 32-bit vs. 64-bit: I didn't realize that both NI and Keysight provided 64-bit VISAs so I installed python 3.11 32-bit and now I can't be bothered to switch back to whatever 64-bit version of Python I had before
