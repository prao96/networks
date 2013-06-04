import math
import common_txrx as common
import numpy

class Transmitter:
    def __init__(self, carrier_freq, samplerate, one, spb, silence):
        self.fc = carrier_freq  # in cycles per sec, i.e., Hz
        self.samplerate = samplerate
        self.one = one
        self.spb = spb
        self.silence = silence
        print 'Transmitter: '

    def add_preamble(self, databits):
        '''
        Prepend the array of source bits with silence bits and preamble bits
        The recommended preamble bits is 
        [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1]
        The output should be the concatenation of arrays of
            [silence bits], [preamble bits], and [databits]
        '''
        # Concatenating relevant arrays to form databits_with_preamble
        databits_with_preamble = numpy.zeros(self.silence)
        preamble = numpy.array([1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1])
        databits_with_preamble=numpy.concatenate([databits_with_preamble,preamble])
        databits_with_preamble=numpy.concatenate([databits_with_preamble,databits])
        return databits_with_preamble


    def bits_to_samples(self, databits_with_preamble):
        '''
        Convert each bits into [spb] samples. 
        Sample values for bit '1', '0' should be [one], 0 respectively.
        Output should be an array of samples.
        '''
        # Filling samples array with 0s and 9s, depending on databits_with_preamble
        samples = numpy.zeros(len(databits_with_preamble)*self.spb)
        counter = 0
        k=0
        for i in databits_with_preamble:
            if i == 0:
                valToFill = 0
            elif i == 1:
                valToFill = self.one
            while counter<self.spb:
                samples[k] = valToFill
                k+=1
                counter+=1
            counter = 0
        return samples
        

    def modulate(self, samples):
        '''
        Calls modulation function. No need to touch it.
        '''
        return common.modulate(self.fc, self.samplerate, samples)
