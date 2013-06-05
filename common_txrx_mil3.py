import numpy
import math
import operator
import cmath

# Methods common to both the transmitter and receiver
def modulate(fc, samplerate, samples):
  '''
  A modulator that multiplies samples with a local carrier 
  of frequency fc, sampled at samplerate
  '''
  cosFunction = numpy.zeros(len(samples))
  modulatedSamples = numpy.zeros(len(samples))

  for i in range(len(samples)):
    cosFunction[i] = math.cos(fc*2*math.pi/samplerate*i)

  for k in range(len(samples)):
    modulatedSamples[k] = cosFunction[k]*samples[k]

  return modulatedSamples

def demodulate(fc, samplerate, samples):
  '''
  A demodulator that performs quadrature demodulation
  '''
  complexExp = numpy.zeros(len(samples))
  demodSamples = numpy.zeros(len(samples))

  for i in range(len(samples)):
    complexExp[i] = math.cos(2*math.pi*fc/samplerate*i)

  for k in range(len(samples)):
    demodSamples[k] = complexExp[k]*samples[k]

  return demodSamples

def lpfilter(samples_in, omega_cut):
  '''
  A low-pass filter of frequency omega_cut.
  '''
  # set the filter unit sample response
  L = 50
  filteredOutput = numpy.zeros(len(samples_in))
  h = numpy.zeros(2*L+1)
  
  for i in range(0, len(h)):
    h[i] = math.sin(omega_cut*(i-L))/(math.pi*(i-L))
  h[L+1] = omega_cut/math.pi

  for n in range(0, len(filteredOutput)):
    for l in range(-L, L):
      filteredOutput[n] = filteredOutput[n] + h[l+L]*samples[n-(L+l)]
    filteredOutput[n] = math.abs(filteredOutput[n])
  # compute the demodulated samples
  return filteredOutput

