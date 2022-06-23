Real-time multi-channel filter in Python
=============================

Real-time filter uses the scipy `sosfilt` implementation to achieve the fast computational speed and high stability. The filter is capable of sample by sample multi-channel filtering and able to switch between raw mode and filter mode interchangably.


Import
------

import IIR filter use the following import:

```python
from iir import IIR
```

Create an instance
------------------

The constructor takes the `num_channels` and `sampling_frequency` as an input parameters:

```python
iir_filter = IIR(
    num_channels=4,
    sampling_frequency=256 #Hz
)
```

Building pipeline
-----------------

Filter can be cascading by using the `add_filter` method. By default, the method use the butterworth filter which uses the same parameter as scipy `butter` method:

```python
# Add 6th order butterworth bandstop filter with cutoff at 45-55Hz
iir_filter.add_filter(
    order=6, 
    cutoff=(45,55),
    filter_type='bandstop'
)
# Add 2th order butterworth highpass filter with cutoff at 30Hz
iir_filter.add_filter(
    order=2, 
    cutoff=30,
    filter_type='lowpass'
)
```

For other types of filter, using scipy `iirfilter` method to create sos coefficient array and add to the IIR filter using `add_sos` method.

```python
# Build your own filter
sos_coefficient = scipy.signal.iirfilter(N=17, Wn=[50, 200], 
    rs=60, btype='band', analog=False, ftype='cheby2', fs=2000,
    output='sos')

iir_filter.add_sos(
    sos=sos_coefficient, 
)
```
Filtering
---------
The samples matrix is [samples x channels].
```python
raw_samples = [
    [CH1[0],CH2[0]],
    [CH1[1],CH2[1]],
    [CH1[2],CH2[2]],
    [CH1[3],CH2[3]],
    ...
]
```
We can throw our raw signals directly into filter method.
```python
filt_samples = iir_filter.filter(raw_samples)
```

Raw mode
---------
Using `set_raw_mode` to bypass signal from filter.
```python
iir_filter.set_raw_mode(True)
```
 This is useful when you want to observe the raw signal. Without removing all codes
```python
raw_samples = iir_filter.filter(raw_samples)
```

Acknowledgement
---------------
This project is inspired by [py-iir-filter](https://github.com/berndporr/py-iir-filter) repository of [@berndporr](https://github.com/berndporr)