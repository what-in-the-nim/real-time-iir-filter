from dataclasses import dataclass, field
from scipy import signal
from typing import Union, Sequence
import numpy as np


@dataclass
class IIR:
    """
    IIR multi-channel filter
    """
    num_channel: int
    sampling_frequency: int

    raw_enabled: bool = field(default=True, repr=False)
    filter_dict: dict[str,dict] = field(init=False, default_factory=dict)
    coeffs : list[tuple] = field(init=False,repr=False, default_factory=list)
    past_zi: list[np.ndarray] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.past_zi = None

    @property
    def total_filter(self) -> int:
        return len(self.coeffs)

    def _init_zi(self, signals: Union[list,np.ndarray]) -> None:
        """
        Initialize initial condition for first sample to reduce transient-state time of signals

        :param signals: Two dimensional matrix of [samples x channels]
        :type signals: List or numpy array
        """
        self.past_zi = list()
        first_sample = signals[...,0]

        #Change dimension to match initial_zi dimension
        first_sample = np.expand_dims(np.expand_dims(first_sample,axis=-1),axis=0)

        for coeff in self.coeffs:
            initial_zi = signal.sosfilt_zi(coeff)
            initial_zi = np.repeat(np.expand_dims(
                initial_zi, axis=1), self.num_channel, axis=1)
            initial_zi *= first_sample
            self.past_zi.append(initial_zi)

    def _add_filter_dict(self, order: int, cutoff: Union[Sequence,int,float], filter_type: str) -> None:
        """
        Add filter details into filter dict

        :param int order: An order of filter.
        :param Sequence|int|float cutoff: A critical frequency of the filter.
        :param str filter_type: Filter type can be 'lowpass', 'highpass', 'bandstop' and 'bandpass'.
        """
        filter_details = {
            'type'  : filter_type,
            'order' : order,
            'cutoff' : cutoff
        }
        filter_name = f'filter_{self.total_filter}'
        self.filter_dict[filter_name] = filter_details

    def set_raw_enabled(self,state: bool) -> None:
        self.raw_enabled = state

    def add_filter(self, order: int, cutoff: Union[Sequence,int,float], filter_type: str) -> None:
        """
        Add filter into cascading pipeline

        :param int order: An order of filter.
        :param Sequence|int|float cutoff: A critical frequency of the filter.
        :param str filter_type: Filter type can be 'lowpass', 'highpass', 'bandstop' and 'bandpass'.
        """

        new_filter_coeff = signal.butter(
            order, cutoff, filter_type, output='sos', fs=self.sampling_frequency)
  
        self.coeffs.append(new_filter_coeff)
        self._add_filter_dict(order,cutoff,filter_type)

    def add_sos(self,sos: np.ndarray) -> None:
        """
        Add sos filter into cascading pipeline

        :param ndarray sos: A filter coefficient.
        """
        self.coeffs.append(sos)
        #TODO add filter details


    def filter(self, raw_signal: Union[list,np.ndarray]) -> np.ndarray:
        """
        Filter a sequence of multi-channel samples

        :param raw_signal: Two dimensional matrix of [samples x channels]
        :type raw_signal: List or numpy array
        :return np.ndarray
        """
        if isinstance(raw_signal,list):
            filt_signal = np.array(list(zip(*raw_signal)))
        elif isinstance(raw_signal,np.ndarray):
            filt_signal = raw_signal.T

        if not self.raw_enabled:
            return filt_signal.T

        if self.past_zi is None:
            self._init_zi(filt_signal)

        for index,(sos,past_zi) in enumerate(zip(self.coeffs,self.past_zi)):
            filt_signal, zi = signal.sosfilt(sos, filt_signal, zi=past_zi)
            self.past_zi[index] = zi
        
        filtered = filt_signal.T
        return filtered