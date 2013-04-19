import numpy
import math
import operator

# Methods common to both the transmitter and receiver.
def hamming(s1,s2):
    # Given two binary vectors s1 and s2 (possibly of different 
    # lengths), first truncate the longer vector (to equalize 
    # the vector lengths) and then find the hamming distance
    # between the two. Also compute the bit error rate  .
    # BER = (# bits in error)/(# total bits )
    hamming_d = 0
    s2 = s2[:len(s1)]
    s1 = s1[:len(s2)]
    i = 0
    for val in s1:
    	# Counts number of positions where the vectors s1 and s2 vary
    	if s2[i]!=val:
    		hamming_d+=1
    	i += 1
    ber = hamming_d/float(len(s1))
    return hamming_d, ber
