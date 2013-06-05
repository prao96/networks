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
  center1 = 0.0
  center2 = 0.0
  while center1 == center2:
    center1 = random.uniform(min(demod_samples), max(demod_samples))
    center2 = random.uniform(min(demod_samples), max(demod_samples))
  flag=0
  cluster1 = numpy.zeros(len(demod_samples))
  cluster2 = numpy.zeros(len(demod_samples))

  while flag==0:
    m, k = 0, 0
    for i in range(0,len(demod_samples)-1):
      if abs(demod_samples[i]-center1) > abs(demod_samples[i]-center2):
        cluster2[m] = demod_samples[i]
        m+=1
      else:
        cluster1[k] = demod_samples[i]
        k+=1

    old1=center1
    old2=center2
    center1 = numpy.average(cluster1[0:k-1])
    center2 = numpy.average(cluster2[0:m-1])
    if (old1==center1) & (old2==center2):
      flag=1

  one = old1
  zero = old2
  thresh = (zero+one)/2

 
  # insert code to associate the higher of the two centers 
  # with one and the lower with zero
  
  print "Threshold for 1:"
  print one
  print " Threshold for 0:"
  print zero
  print thresh

  # insert code to compute thresh
  return one, zero, thresh

    
