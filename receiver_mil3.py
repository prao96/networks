import numpy
import math
import operator
import random
import scipy.cluster.vq
import common_txrx as common

def detect_threshold(demod_samples): 
        # Now, we have a bunch of values that, for on-off keying, are
        # either near amplitude 0 or near a positive amplitude
        # (corresp. to bit "1").  Because we don't know the balance of
        # zeroes and ones in the input, we use 2-means clustering to
        # determine the "1" and "0" clusters.  In practice, some
        # systems use a random scrambler to XOR the input to balance
        # the zeroes and ones. We have decided to avoid that degree of
        # complexity in audiocom (for the time being, anyway).

	# initialization
  print demod_samples
  center1 = min(demod_samples)
  center2 = max(demod_samples) 
  cluster1 = numpy.zeros(len(demod_samples))
  cluster2 = numpy.zeros(len(demod_samples))
  m, k = 0, 0

  for i in range(0, len(demod_samples)):
    sumVals = 0
    if abs(demod_samples[i] - center1) > abs(demod_samples[i] - center2):
      cluster2[m] = demod_samples[i]
      center2 = center2*(1-(1/(m+1))) + m*(1/(m+1))
      m+=1
    else: 
      cluster1[k] = demod_samples[i]
      center1 = center1*(1-(1/(k+1))) + k*(1/(k+1))
      k+=1

  zero = center1
  one = center2
  thresh = (one + zero)/2

 
  # insert code to associate the higher of the two centers 
  # with one and the lower with zero
  
  print "Threshold for 1:"
  print one
  print " Threshold for 0:"
  print zero
  print thresh

  # insert code to compute thresh
  return one, zero, thresh

    
