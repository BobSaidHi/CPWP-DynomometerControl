# Imports
import odrive

class odriveMotorController:
    # Our controller is a bit old, this version is more relevant: # https://docs.odriverobotics.com/v/0.5.4/getting-started.html
    # Latest: https://docs.odriverobotics.com/v/0.5.5/specifications.html
    # https://docs.odriverobotics.com/v/0.5.5/getting-started.html
    # Troubleshooting: https://docs.odriverobotics.com/v/latest/troubleshooting.html

    def __init__(self):
        # Connect to Odrive
        self.odrv0 = odrive.find_any

        # Get version number
        print("self.odrv0.hw_version_major:", self.odrv0.hw_version_major) # 3
        print("self.odrv0.hw_version_minor:", self.odrv0.hw_version_minor) # 6
        print("self.odrv0.hw_version_revision:", self.odrv0.hw_version_revision) # Doesn’t work

        print("self.odrv0.fw_version_major:", self.odrv0.fw_version_major) # 3
        print("self.odrv0.fw_version_minor:", self.odrv0.fw_version_minor) # 5
        print("self.odrv0.fw_version_revision:", self.odrv0.fw_version_revision) # 5

    def configure(self):
        raise NotImplementedError
        # Reset
        self.odrv0.erase_configuration() # Error

        # https://docs.odriverobotics.com/v/0.5.5/getting-started.html#setting-the-limits
        self.odrv0.axis0.motor.config.current_lim = 10 # Up to 40A w/o heat sink (Watch out for motor overheat!)

        self.odrv0.axis0.controller.config.vel_limit = 2

        self.odrv0.axis0.motor.config.calibration_current = 2 # 10 by default, set 2 for now

        # https://docs.odriverobotics.com/v/0.5.5/getting-started.html#setting-other-hardware-parameters
        self.odrv0.config.enable_brake_resistor = True
        self.odrv0.config.brake_resistance =  # 50 W Default, but needs to be in Ohms # 2 defualt, measure somewhat close
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

        # Save config
        self.odrv0.save_configuration()
        return False

    # Verify config
    def verifyConfig():
        print("self.odrv0.axis0.motor.config.current_lim:", self.odrv0.axis0.motor.config.current_lim)
        print("self.odrv0.axis0.controller.config.vel_limit:", self.odrv0.axis0.controller.config.vel_limit)
        print("self.odrv0.axis0.motor.config.calibration_current:", self.odrv0.axis0.motor.config.calibration_current)
        print("self.odrv0.config.enable_brake_resistor:", self.odrv0.config.enable_brake_resistor)
        print("self.odrv0.config.brake_resistance:", self.odrv0.config.brake_resistance)
        print("self.odrv0.config.dc_max_negative_current:", self.odrv0.config.dc_max_negative_current)
        print("self.odrv0.axis0.motor.config.pole_pairs:", self.odrv0.axis0.motor.config.pole_pairs)
        print("self.odrv0.axis0.motor.config.torque_constant:", self.odrv0.axis0.motor.config.torque_constant)
        print("self.odrv0.axis0.motor.config.motor_type:", self.odrv0.axis0.motor.config.motor_type)
        print("self.odrv0.axis0.config.sensorless_ramp.ve", self.odrv0.axis0.config.sensorless_ramp.vel)
        print("self.odrv0.axis0.config.sensorless_ramp.accel", self.odrv0.axis0.config.sensorless_ramp.accel)
        print("self.odrv0.axis0.controller.config.vel_gain:" self.odrv0.axis0.controller.config.vel_gain)
        print("self.odrv0.axis0.controller.config.vel_integrator_gain:", self.odrv0.axis0.controller.config.vel_integrator_gain)
        print("self.odrv0.axis0.controller.config.control_mode:", self.odrv0.axis0.controller.config.control_mode)
        print("self.odrv0.axis0.motor.config.current_lim:", self.odrv0.axis0.motor.config.current_lim)
        print("self.odrv0.axis0.sensorless_estimator.config.pm_flux_linkage:", self.odrv0.axis0.sensorless_estimator.config.pm_flux_linkage)
        print("self.odrv0.axis0.config.enable_sensorless_mode:",  self.odrv0.axis0.config.enable_sensorless_mode)
        print(":", )
        return False

