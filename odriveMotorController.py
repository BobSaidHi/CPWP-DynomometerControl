"""
OdriveMotorController.py
Control an Odrive motor controller over USB

@author BSI

This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

# Imports - logger
import logging
import logger

# Imports - exit handling
import sys

# Imports - control
import odrive


# Start Logger
logger = logging.getLogger("DynamometerControl")
logger.setLevel(logging.DEBUG)


class odriveMotorController:
    """
    Control an Odrive motor controller over USB

    Useful links:
    Our controller is a bit old, this version is more relevant: # https://docs.odriverobotics.com/v/0.5.4/getting-started.html
    Latest: https://docs.odriverobotics.com/v/0.5.5/specifications.html
    https://docs.odriverobotics.com/v/0.5.5/getting-started.html
    Troubleshooting: https://docs.odriverobotics.com/v/latest/troubleshooting.html
    """

    def __init__(self):
        """
        Object to control an Odrive motor
        """
        # Start Logger
        self.logger = logging.getLogger("DynamometerControl")
        self.logger.setLevel(logging.DEBUG)

        # Connect to Odrive
        self.odrv0 = odrive.find_any

        # Get version number
        try:
            self.logger.info("self.odrv0.hw_version_major:", self.odrv0.hw_version_major) # 3
            self.logger.info("self.odrv0.hw_version_minor:", self.odrv0.hw_version_minor) # 6
            self.logger.info("self.odrv0.hw_version_revision:", self.odrv0.hw_version_revision) # Doesn’t work

            self.logger.info("self.odrv0.fw_version_major:", self.odrv0.fw_version_major) # 3
            self.logger.info("self.odrv0.fw_version_minor:", self.odrv0.fw_version_minor) # 5
            self.logger.info("self.odrv0.fw_version_revision:", self.odrv0.fw_version_revision) # 5
        except AttributeError as e:
            self.logger.fatal("Could not retrieve odrive information: " + str(e))
            raise e
    
    def configure(self):
        """
        Reconfigures odrv0 and odrv0.axis0
        """

        raise NotImplementedError
        # Reset
        self.odrv0.erase_configuration() # Error

        # https://docs.odriverobotics.com/v/0.5.5/getting-started.html#setting-the-limits
        self.odrv0.axis0.motor.config.current_lim = 10 # Up to 40A w/o heat sink (Watch out for motor overheat!)

        self.odrv0.axis0.controller.config.vel_limit = 2

        self.odrv0.axis0.motor.config.calibration_current = 2 # 10 by default, set 2 for now

        # https://docs.odriverobotics.com/v/0.5.5/getting-started.html#setting-other-hardware-parameters
        self.odrv0.config.enable_brake_resistor = True
        self.odrv0.config.brake_resistance = -1 # 50 W Default, but needs to be in Ohms # 2 defualt, measure somewhat close
        # self.odrv0.config.dc_max_negative_current = .01 # Default 10 mA (in Amps)

        self.odrv0.axis0.motor.config.pole_pairs = 7
        self.odrv0.axis0.motor.config.torque_constant = 8.27 / 270
        self.odrv0.axis0.motor.config.motor_type = MotorType.HIGH_CURRENT

        # Thermistor configured by default, do not change
        #<axis>.motor.fet_thermistor.config.temp_limit_lower # Default 100
        #<axis>.motor.fet_thermistor.config.temp_limit_upper # Default 120

        # https://docs.odriverobotics.com/v/0.5.5/commands.html#setting-up-sensorless
        # Velocity control:
        #self.odrv0.axis0.config.sensorless_ramp.vel = # rad/sec # Default 400 rad → 270 rpm → 28.27
        #self.odrv0.axis0.config.sensorless_ramp.accel =  # rad/sec^2 # Default 200 rad/s^2 – > 28.27 /2 

        # These values are good for the D5065 motor (which we have (I think))
        self.odrv0.axis0.controller.config.vel_gain = 0.01
        self.odrv0.axis0.controller.config.vel_integrator_gain = 0.05
        self.odrv0.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
        #self.odrv0.axis0.controller.config.vel_limit = <a value greater than axis.config.sensorless_ramp.vel / (2pi * 7)>
        self.odrv0.axis0.motor.config.current_lim = 2 * self.odrv0.axis0.config.sensorless_ramp.current
        self.odrv0.axis0.sensorless_estimator.config.pm_flux_linkage = 5.51328895422 / (7 * 270)
        self.odrv0.axis0.config.enable_sensorless_mode = True

        # https://docs.odriverobotics.com/v/0.5.5/getting-started.html#watchdog-timer

        # TODO: Calibrate

        # Save config
        self.odrv0.save_configuration()
        # TODO: Reconnect
        return False

    def calibrate(self, bypassVerification):
        """
        Prompts for verification if bypassVerification is False and runs a full calibration.  This may not be required for sensorless mode
        Skips verification if bypassVerification is True

        @param bypassVerification (Boolean)
        """
        if not bypassVerification:
            print("Ready to run a full calibration.  Continue? (Y/n): ")
            response = input()
            logger.debug('User response to "Ready to run a full calibration.  Continue? (Y/n): " ' + response)
            if not response == 'Y':
                logger.fatal("Motor calibration canceled by user!")
                raise SystemExit("Motor calibration canceled by user!")
            else:
                logger.debug("Continuing...")
                self.calibrate(True)
        else:
            logger.info("Starting calibration.")
            self.odrv0.axis0.requested_state = odrive.AXIS_STATE_MOTOR_CALIBRATION
            print("Press any key to save config once the motor stops or send a KeyboardInterrupt to cancel ([CTRL] + [C])")
            response = input()
            logger.debug('User response to "Press any key to save config once the motor stops or send a KeyboardInterrupt to cancel ([CTRL] + [C])" ' + response)
            self.odrv0.save_configuration()
            # TODO: Reconnect
            raise NotImplementedError

    # Verify config
    def verifyConfig(self):
        """
        Verifies the motor configuration of odrv0.asis0
        """
        try:
            self.logger.info("self.odrv0.axis0.motor.config.current_lim:", self.odrv0.axis0.motor.config.current_lim)
            self.logger.info("self.odrv0.axis0.controller.config.vel_limit:", self.odrv0.axis0.controller.config.vel_limit)
            self.logger.info("self.odrv0.axis0.motor.config.calibration_current:", self.odrv0.axis0.motor.config.calibration_current)
            self.logger.info("self.odrv0.config.enable_brake_resistor:", self.odrv0.config.enable_brake_resistor)
            self.logger.info("self.odrv0.config.brake_resistance:", self.odrv0.config.brake_resistance)
            self.logger.info("self.odrv0.config.dc_max_negative_current:", self.odrv0.config.dc_max_negative_current)
            self.logger.info("self.odrv0.axis0.motor.config.pole_pairs:", self.odrv0.axis0.motor.config.pole_pairs)
            self.logger.info("self.odrv0.axis0.motor.config.torque_constant:", self.odrv0.axis0.motor.config.torque_constant)
            self.logger.info("self.odrv0.axis0.motor.config.motor_type:", self.odrv0.axis0.motor.config.motor_type)
            self.logger.info("self.odrv0.axis0.config.sensorless_ramp.ve", self.odrv0.axis0.config.sensorless_ramp.vel)
            self.logger.info("self.odrv0.axis0.config.sensorless_ramp.accel", self.odrv0.axis0.config.sensorless_ramp.accel)
            self.logger.info("self.odrv0.axis0.controller.config.vel_gain:", self.odrv0.axis0.controller.config.vel_gain)
            self.logger.info("self.odrv0.axis0.controller.config.vel_integrator_gain:", self.odrv0.axis0.controller.config.vel_integrator_gain)
            self.logger.info("self.odrv0.axis0.controller.config.control_mode:", self.odrv0.axis0.controller.config.control_mode)
            self.logger.info("self.odrv0.axis0.motor.config.current_lim:", self.odrv0.axis0.motor.config.current_lim)
            self.logger.info("self.odrv0.axis0.sensorless_estimator.config.pm_flux_linkage:", self.odrv0.axis0.sensorless_estimator.config.pm_flux_linkage)
            self.logger.info("self.odrv0.axis0.config.enable_sensorless_mode:",  self.odrv0.axis0.config.enable_sensorless_mode)
            self.logger.info("self.odrv0.axis0.motor.is_calibrated", self.odrv0.axis0.motor.is_calibrated)
        except AttributeError as e:
            self.logger.error("Could not verify odrive information: " + str(e))
            raise e
        return False

    # Control

    def setVelocity(self, velocity):
        """
        Updates the motor's target velocity

        @param velocity in rad/s
        """
        self.odrv0.axis0.config.sensorlesss_ramp = velocity

    def startSensorless(self, bypassVerification=False):
        """
        Prompts for verification if bypassVerification is False and starts the motor in sensorless mode assuming the target velocity has already been set
        Skips verification if bypassVerification is True

        @param bypassVerification (Boolean)
        """
        if not bypassVerification:
            print("Ready to enable the motor in sensorless mode.  Continue? (Y/n): ")
            response = input()
            logger.debug('User response to "Ready to enable the motor in sensorless mode.  Continue? (Y/n): " ' + response)
            if not response == 'Y':
                logger.fatal("Motor enable canceled by user!")
                raise SystemExit("Motor enable canceled by user!")
            else:
                logger.debug("Continuing...")
                self.startSensorless(True)
        else:
            logger.info("Starting the motor.")
            self.odrv0.axis0.requested_state = odrive.AXIS_STATE_CLOSED_LOOP_CONTROL

    def stop(self):
        """
        Sets the motor's target velocity to 0 rad/s
        """
        self.setVelocity(0)

    def getDCBusVoltage(self):
        """
        @return Voltage on the DC bus as measured by the ODrive.
        """
        temp = self.odrv0.vbus_voltage
        logger.debug("DCBusVoltage: " + temp)
        return 

    def getDCBusCurrent(self):
        """
        @return Current on the DC bus as calculated by the ODrive.
            A positive value means that the ODrive is consuming power from the power supply, a negative value means that the ODrive is sourcing power to the power supply.
        This value is equal to the sum of the motor currents and the brake resistor currents. The motor currents are measured, the brake resistor current is calculated based on config.brake_resistance.

        """
        temp = self.odrv0.ibus
        return logger.debug("DCBusCurrent: " + temp)

