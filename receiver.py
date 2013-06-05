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

        center = self.spb/2
        bound = self.spb/4
        energy_offset=-1
        i = 0
        for i in range(len(demod_samples)):
            centerAverage = numpy.average(demod_samples[i+self.spb/4:i+3*self.spb/4])
            if centerAverage > (thresh+one)/2:
                energy_offset=i
                break

        if energy_offset < 0:
            print '*** ERROR: Could not detect any ones (so no preamble). ***'
            print '\tIncrease volume / turn on mic?'
            print '\tOr is there some other synchronization bug? ***'
            sys.exit(1)

        preamble = numpy.array([1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1])
        preamble_length=len(preamble)
        samples = numpy.zeros(preamble_length*self.spb)
        counter = 0

        for k in range(preamble_length):
            if preamble[k]==1:
                valToFill=one
            else:
                valToFill=0.0
            for l in range(self.spb):
                samples[k*self.spb+l]=valToFill

        dotProducts=numpy.zeros(3*len(samples))
        for i in range(3*len(samples)):
            demodSubset=demod_samples[energy_offset+i:energy_offset+i+len(samples)]
            subsetNorm = numpy.linalg.norm(demodSubset)
            dotProducts[i]=numpy.dot(demodSubset[0:len(demodSubset)-1],samples[0:len(demodSubset)-1])
            dotProducts[i]=dotProducts[i]/subsetNorm

        preamble_offset= numpy.argmax(dotProducts)

        print 'Energy offset, followed by preamble offset'
        print energy_offset
        print preamble_offset

        return preamble_offset+energy_offset
        
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

        preamble = numpy.array([1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1])
        preamble_length=len(preamble)
        midpoints = numpy.zeros(preamble_length)
        zeros = numpy.zeros(9)
        zerosIndex = 0
        ones = numpy.zeros(15)
        onesIndex = 0

        for i in range(preamble_length):
            midpoints[i] = numpy.average(demod_samples[preamble_start+i*self.spb+self.spb/4: preamble_start+i*self.spb+self.spb*3/4])
        for k in range(preamble_length):
            if preamble[k] == 0:
                zeros[zerosIndex] = midpoints[k]
                zerosIndex+=1
            else:
                ones[onesIndex] = midpoints[k]
                onesIndex+=1


        onesAverage = numpy.average(ones)
        zerosAverage = numpy.average(zeros)

        print onesAverage

        print zerosAverage

        newThresh = (onesAverage+zerosAverage)/2

        print newThresh

        checkedBits = numpy.zeros(preamble_length)
        for j in range(preamble_length):
            if midpoints[j]>newThresh:
                checkedBits[j] = 1
            else: 
                checkedBits[j] = 0

        flag = 0

        for p in range(preamble_length):
            if preamble[p] != checkedBits[p]:
                flag = 1
            if flag == 1:
                print '*** ERROR: Preamble decoded incorrectly. ***'
                print checkedBits
                print preamble
                sys.exit(1)
        data_bits = numpy.zeros(int((len(demod_samples)-preamble_start-(preamble_length))/self.spb),int)
        index = preamble_start+((preamble_length))*self.spb
        i = 0
        while index <= len(demod_samples):
            start = index+self.spb/4
            stop = index+3*self.spb/4
            avg = numpy.average(demod_samples[start:stop])
            if avg<newThresh:
                data_bits[i] = 0
                i+=1
            else:
                data_bits[i] = 1
                i+=1
            index+=self.spb




        return data_bits # without preamble

    def demodulate(self, samples):
        return common.demodulate(self.fc, self.samplerate, samples)
