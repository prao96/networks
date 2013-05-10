import sys
import math
import numpy
import scipy.cluster.vq
import common_txrx as common
from numpy import linalg as LA
import receiver_mil3

class Receiver:
    def __init__(self, carrier_freq, samplerate, spb):
        '''
        The physical-layer receive function, which processes the
        received samples by detecting the preamble and then
        demodulating the samples from the start of the preamble 
        sequence. Returns the sequence of received bits (after
        demapping)
        '''
        self.fc = carrier_freq
        self.samplerate = samplerate
        self.spb = spb 
        print 'Receiver: '

    def detect_threshold(self, demod_samples):
        '''
        Calls the detect_threshold function in another module.
        No need to touch this.
        ''' 
        return receiver_mil3.detect_threshold(demod_samples)
 
    def detect_preamble(self, demod_samples, thresh, one):
        '''
        Find the sample corresp. to the first reliable bit "1"; this step 
        is crucial to a proper and correct synchronization w/ the xmitter.
        '''

        '''
        First, find the first sample index where you detect energy based on the
        moving average method described in the milestone 2 description.
        '''
        # Fill in your implementation of the high-energy
        center=self.spb/2
        bound=round(self.spb/4,0)
        k=0
        sum=0
        avg=0
        energy_offset=0
        while k<len(demod_samples)-self.spb:
            for x in range(int(center-bound),int(center+bound)):
                sum+=demod_samples[x]
            avg=sum/(self.spb/2)
            if avg>(one+thresh)/2:
                energy_offset=int(k+center)
                break
            else:
                k+=1
            sum=0
            avg=0


        if k==len(demod_samples)-self.spb-1:
            energy_offset=-1

        if energy_offset < 0:
            print '*** ERROR: Could not detect any ones (so no preamble). ***'
            print '\tIncrease volume / turn on mic?'
            print '\tOr is there some other synchronization bug? ***'
            sys.exit(1)

        '''
        Then, starting from the demod_samples[offset], find the sample index where
        the cross-correlation between the signal samples and the preamble 
        samples is the highest. 
        '''
        # Fill in your implementation of the cross-correlation check procedure
        preamble = numpy.array([1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1])
        samples = numpy.zeros(len(preamble)*self.spb)
        counter = 0
        k=0
        for i in preamble:
            if i == 0:
                valToFill = 0
            elif i == 1:
                valToFill = 9
            while counter<self.spb:
                samples[k] = valToFill
                k+=1
                counter+=1
            counter = 0

        numSamples = len(samples)
        demodSubset = numpy.zeros(numSamples)
        dotProducts=numpy.zeros(3*len(samples))
        index=0
        for i in range(energy_offset,energy_offset+3*len(samples)):
            demodSubset=demod_samples[i:i+numSamples].copy()
            dotProducts[index]=numpy.dot(samples,demodSubset)
            index+=1


        
        preamble_offset = numpy.argmax(dotProducts) 
        
        '''
        [preamble_offset] is the additional amount of offset starting from [offset],
        (not a absolute index reference by [0]). 
        Note that the final return value is [offset + pre_offset]
        '''

        return energy_offset + preamble_offset
        
    def demap_and_check(self, demod_samples, preamble_start):
        '''
        Demap the demod_samples (starting from [preamble_start]) into bits.
        1. Calculate the average values of midpoints of each [spb] samples
           and match it with the known preamble bit values.
        2. Use the average values and bit values of the preamble samples from (1)
           to calculate the new [thresh], [one], [zero]
        3. Demap the average values from (1) with the new three values from (2)
        4. Check whether the first [preamble_length] bits of (3) are equal to
           the preamble. If it is proceed, if not terminate the program. 
        Output is the array of data_bits (bits without preamble)
        '''

        # Fill in your implementation
        preamble = numpy.array([1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1])
        preambleCheckSamples = numpy.zeros(24)
        preambleCheck = numpy.zeros(24)
        i = 0
        while i<24:
            preambleCheckSamples[i]=demod_samples[preamble_start+i*self.spb]
        i=0
        while i<24:
            




        return data_bits # without preamble

    def demodulate(self, samples):
        return common.demodulate(self.fc, self.samplerate, samples)
