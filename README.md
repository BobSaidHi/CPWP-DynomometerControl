# Cal Poly Wind Power Club - Power Team - Automated Test Control Software

This script is intended to perform semi-automated testing on a generator as well as wind-tunnel testing for a wind turbine.  Data is recorded to a `.csv` file in the `/output/` directory and logs are stored in `/logs/`.  Different components can be enabled or disabled by changing the variables marked by `# CONFIG`.

## Dynamometer Control

Performs automated dynamometer testing on a generator by controlling & monitoring the following components over USB:

- A VISA compatible power supply (Rigol DP832) using SCPI
- An Odrive motor connected to a Odrive Robotics v3.6 controller using the odrive library
- (Optional) A VISA compatible multimeter (Agilent U3606A) using SCPI
- (Recommended) A VISA compatible programable electronic road (Siglent SDL1020X-E) using SCPI

Note that this program is specific to the use case and ignores things a more generic library might include, such as multiple power supply channels.

## Wind Tunnel Testing

Records data and manages wind tunnel testing on a hobbyist wind turbine by controlling & monitoring the following components over USB:

- An Odrive motor connected to a Odrive Robotics v3.6 controller using the odrive library
- (Optional) A VISA compatible multimeter (Agilent U3606A) using SCPI
- (Recommended) A VISA compatible programable electronic road (Siglent SDL1020X-E) using SCPI

Note that this program is specific to the use case and ignores things a more generic library might include, such as multiple power supply channels.

## Key terms

- Virtual Instrument Software architecture (VISA library) [More info - Wikipedia](https://en.wikipedia.org/wiki/Virtual_instrument_software_architecture)
- Standard Commands for Programmable Instruments (SCPI) [More information - Wikipedia](https://en.wikipedia.org/wiki/Standard_Commands_for_Programmable_Instruments)
- `.csv` - Comma separated values file extension - basically a spreadsheet represented in plain text

## SCPI

The SCPI syntax is hierarchial - A root command might be `:MEASure` with a subcommand `:VOLTage` and then `:DC?` under that.  Note that `:` is used a separator and `?` indicate query while setter commands don't have a question mark afterwords.  For example, to putting the above together would result in `MEASure:VOLTage:DC?`, which would measure the DC voltage.  Not that only the capital letters are required.
Additionally, commands can be concatenated with a semicolon in between and arguments can be provided after a space.

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

## License

This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
