import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import welch

from iir import IIR

fs = 250
num_channel = 2
length = 500

iir_filter = IIR(
    num_channel = num_channel,
    sampling_frequency= fs
)
iir_filter.add_filter(8, (45,55),'bandstop')
iir_filter.add_filter(8, (2,40),'bandpass')

print('Object Representation')
print(iir_filter)

signal_band = [
    (8,5),
    (50,20),
    (80,5)
]
bias = 50 * np.arange(num_channel) + 500

times = np.arange(length)/fs
labels = [f'CH{num+1}' for num in range(num_channel)]
signals = np.zeros((length,num_channel)) + bias
for freq,amp in signal_band:
    signals += np.expand_dims(amp*np.sin(2*np.pi*freq*times),axis=-1)
noises = np.random.randint(0,1000,signals.shape)/500
signals += noises


plt.subplot(2,2,1)
plt.xlabel('Times (s)')
plt.ylabel('Amplitude')
plt.plot(times,signals)
plt.legend(labels,loc=1)

plt.subplot(2,2,2)
filtered = iir_filter.filter(signals)
plt.xlabel('Times (s)')
plt.ylabel('Amplitude')
plt.plot(times,filtered)
plt.legend(labels,loc=1)

plt.subplot(2,2,3)
bins,power = welch(signals.T,fs=fs,nperseg=240,noverlap=200,nfft=500)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.plot(bins,20*np.log10(power.T))
plt.legend(labels,loc=1)

plt.subplot(2,2,4)
bins,power = welch(filtered.T,fs=fs,nperseg=240,noverlap=200,nfft=500)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.plot(bins,20*np.log10(power.T))
plt.legend(labels,loc=1)

plt.tight_layout()
plt.show()