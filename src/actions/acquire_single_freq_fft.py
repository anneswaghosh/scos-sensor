# What follows is a parameterizable description of the algorithm used by this
# action. The first line is the summary and should be written in plain text.
# Everything following that is the extended description, which can be written
# in Markdown and MathJax. Each name in curly brackets '{}' will be replaced
# with the value specified in the `description` method which can be found at
# the very bottom of this file. Since this parameterization step affects
# everything in curly brackets, math notation such as {m \over n} must be
# escaped to {{m \over n}}.
#
# To print out this docstring after parameterization, see
# REPO_ROOT/scripts/print_action_docstring.py. You can then paste that into the
# SCOS Markdown Editor (link below) to see the final rendering.
#
# Resources:
# - MathJax reference: https://math.meta.stackexchange.com/q/5020
# - Markdown reference: https://commonmark.org/help/
# - SCOS Markdown Editor: https://ntia.github.io/scos-md-editor/
#
r"""Apply m4s detector over {nffts} {fft_size}-pt FFTs at {frequency:.2f} MHz.

# {name}

## Radio setup and sample acquisition

This action first tunes the radio to {frequency:.2f} MHz and requests a sample
rate of {sample_rate:.2f} Msps and {gain} dB of gain.

It then begins acquiring, and discards an appropriate number of samples while
the radio's IQ balance algorithm runs. Then, ${nffts} \times {fft_size}$
samples are acquired gap-free.

## Time-domain processing

First, the ${nffts} \times {fft_size}$ continuous samples are acquired from
the radio. If specified, a voltage scaling factor is applied to the complex
time-domain signals. Then, the data is reshaped into a ${nffts} \times
{fft_size}$ matrix:

$$
\begin{{pmatrix}}
a_{{1,1}}      & a_{{1,2}}     & \cdots  & a_{{1,fft\_size}}     \\\\
a_{{2,1}}      & a_{{2,2}}     & \cdots  & a_{{2,fft\_size}}     \\\\
\vdots         & \vdots        & \ddots  & \vdots                \\\\
a_{{nffts,1}}  & a_{{nfts,2}}  & \cdots  & a_{{nfts,fft\_size}}  \\\\
\end{{pmatrix}}
$$

where $a_{{i,j}}$ is a complex time-domain sample.

At that point, a Flat Top window, defined as

$$w(n) = &0.2156 - 0.4160 \cos{{(2 \pi n / M)}} + 0.2781 \cos{{(4 \pi n / M)}} -
         &0.0836 \cos{{(6 \pi n / M)}} + 0.0069 \cos{{(8 \pi n / M)}}$$

where $M = {fft_size}$ is the number of points in the window, is applied to
each row of the matrix.

## Frequency-domain processing

After windowing, the data matrix is converted into the frequency domain using
an FFT, doing the equivalent of the DFT defined as

$$A_k = \sum_{{m=0}}^{{n-1}}
a_m \exp\left\\{{-2\pi i{{mk \over n}}\right\\}} \qquad k = 0,\ldots,n-1$$

The data matrix is then converted to pseudo-power by taking the square of the
magnitude of each complex sample individually, allowing power statistics to be
taken.

## Applying detector

Next, the M4S (min, max, mean, median, and sample) detector is applied to the
data matrix. The input to the detector is a matrix of size ${nffts} \times
{fft_size}$, and the output matrix is size $5 \times {fft_size}$, with the
first row representing the min of each _column_, the second row representing
the _max_ of each column, and so "sample" detector simple chooses one of the
{nffts} FFTs at random.

## Power conversion

To finish the power conversion, the samples are divided by the characteristic
impedance (50 ohms). The power is then referenced back to the RF power by
dividing further by 2. The powers are normalized to the FFT bin width by
dividing by the length of the FFT and converted to dBm. Finally, an FFT window
correction factor is added to the powers given by

$$ C_{{win}} = 20log \left( \frac{{1}}{{ mean \left( w(n) \right) }} \right)

The resulting matrix is real-valued, 32-bit floats representing dBm.

"""

import logging
from enum import Enum

import numpy as np
from django.core.files.base import ContentFile
from sigmf.sigmffile import SigMFFile

from actions.utils import get_fft_window, get_fft_window_correction
from capabilities import capabilities
from hardware import sdr
from sensor import settings, utils
from status.utils import get_location

from .base import Action

logger = logging.getLogger(__name__)

GLOBAL_INFO = {
    "core:datatype": "rf32_le",  # 32-bit float, Little Endian
    "core:version": "0.0.2",
}


class M4sDetector(Enum):
    min = 1
    max = 2
    mean = 3
    median = 4
    sample = 5


def m4s_detector(array):
    """Take min, max, mean, median, and random sample of n-dimensional array.

    Detector is applied along each column.

    :param array: an (m x n) array of real frequency-domain linear power values
    :returns: a (5 x n) in the order min, max, mean, median, sample in the case
              that `detector` is `m4s`, otherwise a (1 x n) array

    """
    amin = np.min(array, axis=0)
    amax = np.max(array, axis=0)
    mean = np.mean(array, axis=0)
    median = np.median(array, axis=0)
    random_sample = array[np.random.randint(0, array.shape[0], 1)][0]
    m4s = np.array([amin, amax, mean, median, random_sample], dtype=np.float32)

    return m4s


class SingleFrequencyFftAcquisition(Action):
    """Perform m4s detection over requested number of single-frequency FFTs.

    :param name: the name of the action
    :param frequency: center frequency in Hz
    :param gain: requested gain in dB
    :param sample_rate: requested sample_rate in Hz
    :param fft_size: number of points in FFT (some 2^n)
    :param nffts: number of consecutive FFTs to pass to detector

    """

    def __init__(self, name, frequency, gain, sample_rate, fft_size, nffts):
        super(SingleFrequencyFftAcquisition, self).__init__()

        self.name = name
        self.frequency = frequency
        self.gain = gain
        self.sample_rate = sample_rate
        self.fft_size = fft_size
        self.nffts = nffts
        self.sdr = sdr  # make instance variable to allow mocking
        self.enbw = None

    def __call__(self, schedule_entry_name, task_id):
        """This is the entrypoint function called by the scheduler."""
        from tasks.models import TaskResult

        # Raises TaskResult.DoesNotExist if no matching task result
        task_result = TaskResult.objects.get(
            schedule_entry__name=schedule_entry_name, task_id=task_id
        )

        self.test_required_components()
        self.configure_sdr()
        data = self.acquire_data()
        m4s_data = self.apply_detector(data)
        sigmf_md = self.build_sigmf_md(task_id)
        self.archive(task_result, m4s_data, sigmf_md)

    def test_required_components(self):
        """Fail acquisition if a required component is not available."""
        self.sdr.connect()
        if not self.sdr.is_available:
            msg = "acquisition failed: SDR required but not available"
            raise RuntimeError(msg)

    def configure_sdr(self):
        self.set_sdr_sample_rate()
        self.set_sdr_frequency()
        self.set_sdr_gain()

    def set_sdr_gain(self):
        self.sdr.radio.gain = self.gain

    def set_sdr_sample_rate(self):
        self.sdr.radio.sample_rate = self.sample_rate
        self.sample_rate = self.sdr.radio.sample_rate

    def set_sdr_frequency(self):
        requested_frequency = self.frequency
        self.sdr.radio.frequency = requested_frequency
        self.frequency = self.sdr.radio.frequency

    def acquire_data(self):
        msg = "Acquiring {} FFTs at {} MHz"
        logger.debug(msg.format(self.nffts, self.frequency / 1e6))

        # Drop ~10 ms of samples
        nskip = int(0.01 * self.sample_rate)

        data = self.sdr.radio.acquire_samples(self.nffts * self.fft_size, nskip=nskip)
        data.resize((self.nffts, self.fft_size))

        return data

    def build_sigmf_md(self, task_id):
        logger.debug("Building SigMF metadata file")

        # Use the radio's actual reported sample rate instead of requested rate
        sample_rate = self.sdr.radio.sample_rate

        sigmf_md = SigMFFile()
        sigmf_md.set_global_info(GLOBAL_INFO)
        sigmf_md.set_global_field("core:sample_rate", sample_rate)

        sensor_def = capabilities["sensor_definition"]
        sensor_def["id"] = settings.FQDN
        sigmf_md.set_global_field("ntia-sensor:sensor", sensor_def)

        action_def = {
            "name": self.name,
            "description": self.description,
            "type": ["FrequencyDomain"],
        }

        sigmf_md.set_global_field("ntia-scos:action", action_def)
        sigmf_md.set_global_field("ntia-scos:task_id", task_id)

        capture_md = {
            "core:frequency": self.frequency,
            "core:datetime": utils.get_datetime_str_now(),
        }

        sigmf_md.add_capture(start_index=0, metadata=capture_md)

        location = get_location()

        for i, detector in enumerate(M4sDetector):
            frequency_domain_detection_md = {
                "ntia-core:annotation_type": "FrequencyDomainDetection",
                "ntia-algorithm:number_of_samples_in_fft": self.fft_size,
                "ntia-algorithm:window": "flattop",
                "ntia-algorithm:equivalent_noise_bandwidth": self.enbw,
                "ntia-algorithm:detector": detector.name + "_power",
                "ntia-algorithm:number_of_ffts": self.nffts,
                "ntia-algorithm:units": "dBm",
                "ntia-algorithm:reference": "not referenced",
            }

            if location:
                frequency_domain_detection_md["core:latitude"] = str(location.latitude)
                frequency_domain_detection_md["core:longitude"] = str(
                    location.longitude
                )

            sigmf_md.add_annotation(
                start_index=(i * self.fft_size),
                length=self.fft_size,
                metadata=frequency_domain_detection_md,
            )

        return sigmf_md

    def apply_detector(self, data):
        """Take FFT of data, apply detector, and translate watts to dBm."""
        logger.debug("Applying detector")

        # Get the fft window and its amplitude/energy correction factors
        fft_window = get_fft_window("Flat Top", self.fft_size)
        fft_window_acf = get_fft_window_correction(fft_window, "amplitude")
        fft_window_ecf = get_fft_window_correction(fft_window, "energy")
        fft_window_enbw = (fft_window_acf / fft_window_ecf) ** 2

        # Calculate the equivalent noise bandwidth of the bins
        self.enbw = self.sdr.radio.sensor_calibration_data["enbw_sensor"]
        self.enbw /= self.fft_size * fft_window_enbw

        # Apply the FFT window
        data = data * fft_window

        # Take and shift the fft (center fc)
        complex_fft = np.fft.fft(data)
        complex_fft = np.fft.fftshift(complex_fft)

        # Convert to pseudo-power (full power conversion will occur after detector)
        power_fft = np.abs(complex_fft)
        power_fft = np.square(power_fft)

        # Run the M4S detector
        power_fft_m4s = m4s_detector(power_fft)

        # If testing, don't flood output with divide-by-zero warnings from np.log10
        if settings.RUNNING_TESTS:
            np_error_settings_savepoint = np.seterr(divide="ignore")

        # Use impedance to finish power conversion and convert to dBm
        impedance_factor = -10 * np.log10(50)
        power_fft_m4s = 10 * np.log10(power_fft_m4s) + impedance_factor + 30
        power_fft_m4s -= 3  # Account for double sided FFT

        # If altered, restore numpy error settings
        if settings.RUNNING_TESTS:
            np.seterr(**np_error_settings_savepoint)

        # Normalize the FFT
        fft_normalization_factor = -20 * np.log10(self.fft_size)
        power_fft_m4s += fft_normalization_factor

        # Apply the window's amplitude correction factor
        window_correction = 20 * np.log10(fft_window_acf)
        power_fft_m4s += window_correction

        return power_fft_m4s

    def archive(self, task_result, m4s_data, sigmf_md):
        from tasks.models import Acquisition

        logger.debug("Storing acquisition in database")

        name = (
            task_result.schedule_entry.name
            + "_"
            + str(task_result.task_id)
            + ".sigmf-data"
        )

        acquisition = Acquisition(task_result=task_result, metadata=sigmf_md._metadata)
        acquisition.data.save(name, ContentFile(m4s_data))
        acquisition.save()
        logger.debug("Saved new file at {}".format(acquisition.data.path))

    @property
    def description(self):
        defs = {
            "name": self.name,
            "frequency": self.frequency / 1e6,
            "sample_rate": self.sample_rate / 1e6,
            "fft_size": self.fft_size,
            "nffts": self.nffts,
            "gain": self.gain,
        }

        # __doc__ refers to the module docstring at the top of the file
        return __doc__.format(**defs)
