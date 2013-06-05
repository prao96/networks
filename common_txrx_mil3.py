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

  for p in range(len(samples)):
    cosFunction[p] = math.cos(fc*2*math.pi/samplerate*p)

  for k in range(len(samples)):
    modulatedSamples[k] = cosFunction[k]*samples[k]

  return modulatedSamples

def demodulate(fc, samplerate, samples):
  '''
  A demodulator that performs quadrature demodulation
  '''
  cosFunction = numpy.zeros(len(samples))
  sinFunction = numpy.zeros(len(samples))
  demodSamples = numpy.zeros(len(samples))

  for i in range(len(samples)):
    cosFunction[i] = math.cos(2*math.pi*fc/samplerate*i)
    sinFunction[i] = math.sin(2*math.pi*fc/samplerate*i)

  for k in range(len(samples)):
    demodSamples[k] = math.sqrt((sinFunction[k]*samples[k])**2+(cosFunction[k]*samples[k])**2)

  return demodSamples

def lpfilter(samples_in, omega_cut):
  '''
  A low-pass filter of frequency omega_cut.
  '''
  # set the filter unit sample response
  L = 50
  filteredOutput = numpy.zeros(len(samples_in), "complex")
  h = numpy.zeros(2*L+1)
  
  for i in range(len(h)):
    n=i-L
    h[i] = math.sin(omega_cut*n)/(math.pi*n)
  h[L+1] = float(omega_cut)/math.pi

  lpsamples = numpy.zeros(len(samples_in), "complex")

  for y in range(len(lpsamples)):
    multsamples[y] = samples_in[y]*exp(2*omega_cut*cmath.sqrt(-1)*y)



  for n in range(len(multsamples)):
    sum=0
    for k in range(-L,L):
      if n-k<0:
        val=0
      else:
        val=multsamples[n-k]
      sum=sum+h[n]*val
    filteredOutput[n]=sum
      
  print filteredOutput

  # for n in range(-L, 0):
  #   filteredOutput[n] = numpy.dot(h, lpsamples[n+L:n+2*L])

  # for n in range(0, L):
  #   filteredOutput[n] = numpy.dot(h, lpsamples[n-L:n+L])

  # print filteredOutput





















  # for n in range(len(filteredOutput)):
  #   for l in range(-L, L):
  #     filteredOutput[n] = filteredOutput[n] + h[l+L]*lpsamples[n-(L+l)]
  #   filteredOutput[n]=abs(filteredOutput[n])

  return filteredOutput

