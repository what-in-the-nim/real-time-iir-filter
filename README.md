Real-time multi-channel filter in Python
=============================

Real-time filter uses the numpy sosfilt implementation to achieve the fast computational speed and high stability. The filter is capable of sample by sample multi-channel filtering.


Import
======

For IIR filter use the following import:

```python
from iir import IIR
```

For FIR filter use the following import:

```python
from fir import FIR
```

Create an instance
==================

The constructor takes the num_channels and sampling_frequency as an input argument:

```python
iir_filter = IIR(
    num_channels=4,
    sampling_frequency=256
)
```

The constructor may takes no argument, but needs to be setup before using.

```python
iir_filter = IIR()
iir_filter.set_num_channels(4)
iir_filter.set_sampling_frequency(256)
```

Building filter
===============

Filter can be cascading by using the add_filter method:

```python
iir_filter.add_filter(
    N=6, 
    Wn=(45,55),
    btypes='bandstop'
)
```

Filtering
=========
The samples matrix is Samples x Channels.
```python
samples: list[list[int|float]] = [
    [ch_1[0],ch_2[0],ch_3[0],ch_4[0]],
    [ch_1[1],ch_2[1],ch_3[1],ch_4[1]],
    [ch_1[2],ch_2[2],ch_3[2],ch_4[2]],
    [ch_1[3],ch_2[3],ch_3[3],ch_4[3]],
    ...
]
```
We can throw our raw signals directly into filter method.
```python
sample = iir_filter.filter(samples)
```
