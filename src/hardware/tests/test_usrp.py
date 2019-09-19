"""Test aspects of RadioInterface with mocked USRP."""

import datetime
import json
from copy import deepcopy

import pytest

import hardware.tests.resources.utils as test_utils
from hardware import usrp_iface


class TestUSRP:
    # Ensure we write the test cal file and use mocks
    setup_complete = False

    def easy_gain(self, f, g):
        """ Create an easily interpolated value """
        return (g) + (f / 1e9)

    def is_close(self, a, b, tolerance):
        """ Handle floating point comparisons """
        return abs(a - b) <= tolerance

    @pytest.fixture(autouse=True)
    def setup_calibration_file(self, tmpdir):
        """ Create the mock USRP """

        # Only setup once
        if self.setup_complete:
            return

        # Create the RadioInterface with the mock usrp_block and get the radio
        usrp_iface.connect()
        if not usrp_iface.is_available:
            raise RuntimeError("Receiver is not available.")
        self.rx = usrp_iface.radio

        # Alert that the setup was complete
        self.setup_complete = True

    # Ensure the usrp can recover from acquisition errors
    def test_acquire_samples_with_retries(self):
        """Acquire samples should retry without error up to `max_retries`."""

        # Check that the setup was completed
        assert self.setup_complete, "Setup was not completed"

        max_retries = 5
        times_to_fail = 3
        self.rx.usrp.set_times_to_fail_recv(times_to_fail)

        try:
            self.rx.acquire_samples(1000, retries=max_retries)
        except RuntimeError:
            msg = "Acquisition failing {} times sequentially with {}\n"
            msg += "retries requested should NOT have raised an error."
            msg = msg.format(times_to_fail, max_retries)
            pytest.fail(msg)

        self.rx.usrp.set_times_to_fail_recv(0)

    def test_acquire_samples_fails_when_over_max_retries(self):
        """After `max_retries`, an error should be thrown."""

        # Check that the setup was completed
        assert self.setup_complete, "Setup was not completed"

        max_retries = 5
        times_to_fail = 7
        self.rx.usrp.set_times_to_fail_recv(times_to_fail)

        msg = "Acquisition failing {} times sequentially with {}\n"
        msg += "retries requested SHOULD have raised an error."
        msg = msg.format(times_to_fail, max_retries)
        with pytest.raises(RuntimeError):
            self.rx.acquire_samples(1000, 1000, max_retries)
            pytest.fail(msg)

        self.rx.usrp.set_times_to_fail_recv(0)

    def test_tune_result(self):
        """Check that the tuning is correct"""
        # Check that the setup was completed
        assert self.setup_complete, "Setup was not completed"

        # Use a positive DSP frequency
        f_lo = 1.0e9
        f_dsp = 1.0e6
        self.rx.tune_frequency(f_lo, f_dsp)
        assert f_lo == self.rx.lo_freq and f_dsp == self.rx.dsp_freq

        # Use a 0Hz for DSP frequency
        f_lo = 1.0e9
        f_dsp = 0.0
        self.rx.frequency = f_lo
        assert f_lo == self.rx.lo_freq and f_dsp == self.rx.dsp_freq

        # Use a negative DSP frequency
        f_lo = 1.0e9
        f_dsp = -1.0e6
        self.rx.tune_frequency(f_lo, f_dsp)
        assert f_lo == self.rx.lo_freq and f_dsp == self.rx.dsp_freq

    def test_scaled_data_acquisition(self):
        """Check that the samples are properly scaled"""
        # Check that the setup was completed
        assert self.setup_complete, "Setup was not completed"

        # Do an arbitrary data collection
        self.rx.sample_rate = int(10e6)
        self.rx.frequency = 1e9
        self.rx.gain = 20
        data = self.rx.acquire_samples(1000)

        # The true value should be the 1 / linear gain
        true_val = test_utils.easy_gain(int(10e6), 1e9, 20) - 10
        true_val = 10 ** (-1 * float(true_val) / 20)

        # Get the observed value
        observed_val = data[0]

        # Assert the value
        tolerance = 1e-5
        msg = "Acquisition was not properly scaled.\n"
        msg += "    Algorithm: {}\n".format(observed_val)
        msg += "    Expected: {}\n".format(true_val)
        msg += "    Tolerance: {}\r\n".format(tolerance)
        assert self.is_close(true_val, observed_val, tolerance), msg

    def test_set_sample_rate_also_sets_clock_rate(self):
        """Setting sample_rate should adjust clock_rate"""

        # Check that the setup was completed
        assert self.setup_complete, "Setup was not completed"

        expected_clock_rate = 30720000

        # Set the sample rate and check the clock rate
        self.rx.sample_rate = 15360000
        observed_clock_rate = self.rx.clock_rate

        assert expected_clock_rate == observed_clock_rate

    def check_defaulted_calibration_parameter(self, param, expected, observed):
        msg = "Default calibration parameters were not properly set.\n"
        msg += "    Parameter: {}\n".format(param)
        msg += "    Expected: {}\n".format(expected)
        msg += "    Observed: {}\r\n".format(observed)
        assert expected == observed, msg

    def test_defaulted_calibration_values(self):
        """Ensure that default calibration values are loaded"""

        # Save and clear the calibrations
        sigan_calibration = self.rx.sigan_calibration
        sensor_calibration = self.rx.sensor_calibration
        self.rx.sigan_calibration = None
        self.rx.sensor_calibration = None

        # Create a dummy setup
        sample_rate = 10e6
        gain_setting = 40
        frequency = 100e6

        # Setup the rx
        self.rx.sample_rate = sample_rate
        self.rx.gain = gain_setting
        self.rx.frequency = frequency

        # Recompute the calibration parameters
        self.rx.recompute_calibration_data()

        # Check the defaulted calibration parameters
        self.check_defaulted_calibration_parameter(
            "gain_sigan", gain_setting, self.rx.sigan_calibration_data["gain_sigan"]
        )
        self.check_defaulted_calibration_parameter(
            "enbw_sigan", sample_rate, self.rx.sigan_calibration_data["enbw_sigan"]
        )
        self.check_defaulted_calibration_parameter(
            "noise_figure_sigan",
            0,
            self.rx.sigan_calibration_data["noise_figure_sigan"],
        )
        self.check_defaulted_calibration_parameter(
            "1db_compression_sigan",
            100,
            self.rx.sigan_calibration_data["1db_compression_sigan"],
        )
        self.check_defaulted_calibration_parameter(
            "gain_sensor", gain_setting, self.rx.sensor_calibration_data["gain_sensor"]
        )
        self.check_defaulted_calibration_parameter(
            "enbw_sensor", sample_rate, self.rx.sensor_calibration_data["enbw_sensor"]
        )
        self.check_defaulted_calibration_parameter(
            "noise_figure_sensor",
            0,
            self.rx.sensor_calibration_data["noise_figure_sensor"],
        )
        self.check_defaulted_calibration_parameter(
            "1db_compression_sensor",
            100,
            self.rx.sensor_calibration_data["1db_compression_sensor"],
        )
        self.check_defaulted_calibration_parameter(
            "gain_preselector", 0, self.rx.sensor_calibration_data["gain_preselector"]
        )
        self.check_defaulted_calibration_parameter(
            "noise_figure_preselector",
            0,
            self.rx.sensor_calibration_data["noise_figure_preselector"],
        )
        self.check_defaulted_calibration_parameter(
            "1db_compression_preselector",
            100,
            self.rx.sensor_calibration_data["1db_compression_preselector"],
        )

        # Reload the calibrations in case they're used elsewhere
        self.rx.sigan_calibration = sigan_calibration
        self.rx.sensor_calibration = sensor_calibration
