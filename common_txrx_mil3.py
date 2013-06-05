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
  # cosFunction = numpy.zeros(len(samples))
  # sinFunction = numpy.zeros(len(samples))
  demodSamples = numpy.zeros(len(samples))
  complexSamples = numpy.zeros(len(demodSamples), "complex")

  for i in range(len(samples)):
    # cosFunction[i] = math.cos(2*math.pi*fc/samplerate*i)
    # sinFunction[i] = math.sin(2*math.pi*fc/samplerate*i)
    complexSamples[i] = samples[i]*cmath.exp(2*math.pi*fc/samplerate*cmath.sqrt(-1)*i)

  complexSamples=lpfilter(complexSamples, math.pi*fc/samplerate)
  # cosFunction=lpfilter(cosFunction, math.pi*fc/samplerate)
  # sinFunction=lpfilter(sinFunction, math.pi*fc/samplerate)

  for k in range(len(samples)):
    #demodSamples[k] = abs(cmath.sqrt((sinFunction[k]*samples[k])**2+(cosFunction[k]*samples[k])**2))
    demodSamples[k] = abs(cmath.sqrt(complexSamples[k].real**2+complexSamples[k].imag**2))

  return demodSamples

def lpfilter(samples_in, omega_cut):
  '''
  A low-pass filter of frequency omega_cut.
  '''
  print "I'm in the low pass filter!!!!!" 

  # set the filter unit sample response
  L = 50
  filteredOutput = numpy.zeros(len(samples_in), "complex")
  h = numpy.zeros(2*L+1)
  
  for i in range(len(h)):
    n=i-L
    if n !=0:
      h[i] = math.sin(omega_cut*n)/(math.pi*n)
    else:
      h[i] = float(omega_cut)/math.pi

  #multsamples = numpy.zeros(len(samples_in)+2*L-1, "complex")
  multsamples = numpy.zeros(len(samples_in)+2*L+1, 'complex')

  for t in range(L, len(samples_in)+L):
    multsamples[t] = samples_in[t-L]#*cmath.exp(2*omega_cut*cmath.sqrt(-1)*(t-L))


  print len(h)
  print len(multsamples[148510:148510+len(h)])
  for n in range(len(filteredOutput)):
    filteredOutput[n] = numpy.dot(h, multsamples[n:n+len(h)])


  # multsamples = numpy.zeros(len(samples_in)+2*L, "complex")

  # for y in range(L,len(multsamples)-L):
  #   multsamples[y] = samples_in[y-L]*cmath.exp(2*omega_cut*cmath.sqrt(-1)*(y-L))

  # for n in range(len(filteredOutput)):
  #   filteredOutput[n]=numpy.dot(multsamples[n:n+2*L+1],h)


  return filteredOutput

