import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import welch
from typing import Sequence

from iir import IIR


def signal_generator(signal_band: Sequence[tuple], shape: tuple, fs: int) -> tuple[np.ndarray]:
    """Generate signals from a certain frequency and amplitude. Shape must be (samples, channels)"""
    times = times = np.arange(length)/fs
    signals = np.zeros(shape)

    for freq, amp in signal_band:
        signal = amp*np.sin(2*np.pi*freq*times)
        signals += np.expand_dims(signal, axis=-1)

    noises = np.random.randint(0, 1000, shape)/500
    signals += noises
    return times, signals


# Constant
fs = 250
length = 500
num_channel = 2

# Creating IIR instance
iir_filter = IIR(
    num_channel=num_channel,
    sampling_frequency=fs
)
iir_filter.add_filter(order=6, cutoff=(45, 55), filter_type='bandstop')
iir_filter.add_filter(order=2, cutoff=30, filter_type='lowpass')
iir_filter.add_filter(order=4, cutoff=3, filter_type='highpass')

# Signal generation
signal_band = [
    (0.01, 200),
    (8, 5),
    (50, 20),
    (80, 5)
]

times, signals = signal_generator(
    signal_band, shape=(length, num_channel), fs=fs)

# Input as numpy array
filtered = iir_filter.filter(signals)
# Input as list
filtered = iir_filter.filter(signals.tolist())

# Plotting
labels = [f'CH{num+1}' for num in range(num_channel)]

plt.subplot(2, 2, 1)
plt.xlabel('Times (s)')
plt.ylabel('Amplitude')
plt.plot(times, signals)
plt.legend(labels, loc=1)

plt.subplot(2, 2, 2)
plt.xlabel('Times (s)')
plt.ylabel('Amplitude')
plt.plot(times, filtered)
plt.legend(labels, loc=1)

plt.subplot(2, 2, 3)
bins, power = welch(signals.T, fs=fs, nperseg=240, noverlap=200, nfft=500)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.plot(bins, 20*np.log10(power.T))
plt.legend(labels, loc=1)

plt.subplot(2, 2, 4)
bins, power = welch(filtered.T, fs=fs, nperseg=240, noverlap=200, nfft=500)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.plot(bins, 20*np.log10(power.T))
plt.legend(labels, loc=1)

plt.tight_layout()
plt.show()
