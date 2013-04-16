# audiocom library: Source and sink functions
import common_srcsink as common
import Image
from graphs import *
import binascii
import random
import base64
import pdb
import numpy


class Source:
	def __init__(self, monotone, filename=None):
		# The initialization procedure of source object
		self.monotone = monotone
		self.fname = filename
		print 'Source: '

	def text2bits(self, filename):
		file = open(filename)
		values = []
		binVals = []
		while 1:
			line = file.readline()
			if not line:
				break
			else:
				newValues = [ord(c) for c in line]
				i=0
				for v in newValues:
					newValues[i]=[int(x) for x in list('{0:0b}'.format(8))]
					i+=1
				values+=newValues
		i=0
		for k in values:
			binVals.append(list(k))
			i +=1
		bits = numpy.array(binVals)
		bits = numpy.ravel(bits)
		#print bits
		return bits

	def bits_from_image(self, filename):
		binPix = []
		binVals = []
		bitsCopy = [] 
		im = Image.open(filename)
		pixelValues = list(im.getdata())
		flatPix = [val for subPV in pixelValues for val in subPV]
		for v in flatPix:
			binPix.append(bin(v)[2:].zfill(8))
		for k in binPix:
			binVals.append(list(k))
		flatVals = [val for sub in binVals for val in sub]
		bitsCopy=[int(s) for s in flatVals]
		bits = numpy.array(bitsCopy)
		#print bitsCopy
		#print bits
		return bits

	def get_header(self, payload_length, srctype): 
		if self.fname is not None:
				if self.fname.endswith('.png') or self.fname.endswith('.PNG'):
					header = srctype + "001" + str(payload_length)
				else:
					header = srctype + "000" + str(payload_length)   
		else:
			header = srctype + "111" + str(payload_length)    
		return header

	def process(self):
		# Form the databits, from the filename 
		#pdb.set_trace()
		if self.fname is not None:
			databits= numpy.array([])
			if self.fname.endswith('.png') or self.fname.endswith('.PNG'):
				#databits is (or should be) a numpy array
				databits = self.bits_from_image(self.fname)
				length = len(databits)
			else:
				databits = self.text2bits(self.fname)  
				length = len(databits)
		else:
			databits = numpy.ones(1000)
			length = len(databits)
			#header should return a numpy array
		header = self.get_header(self, length, '1')
		payload = databits
		databits = numpy.concatentate(header,databits)
		return payload, databits
