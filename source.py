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

		f = open(filename, "r")
		binVals = []
		while 1: 
			line = f.readline()
			if not line:
				break
			else:
				newValues = [ord(c) for c in line]
			i = 0
			for v in newValues:
				intV = int(v)
				newValues[i] = bin(intV)[2:].zfill(8)
				i+=1

		endArray = []
		for v in newValues:
			for c in v:
				endArray.append(int(c))

		bits = numpy.array(endArray)
		print bits

	
		return bits

	def bits_from_image(self, filename):
		binPix = []
		bitsCopy = [] 
		im = Image.open(filename)
		pixelValues = list(im.getdata())
		flatPix = [val for subPV in pixelValues for val in subPV]
		for v in flatPix:
			binPix.append(bin(v)[2:].zfill(8))
		flatVals = [val for sub in binPix for val in sub]
		bitsCopy=[int(s) for s in flatVals]
		bits = numpy.array(bitsCopy)
		return bits

	def get_header(self, payload_length, srctype): 
		headerArray = []
		#print payload_length
		size = bin(payload_length)[2:].zfill(16)
		if self.fname is not None:
			if self.fname.endswith('.png') or self.fname.endswith('.PNG'):
				headerString = srctype + "001" + str(size)
			else:
				headerString = srctype + "000" + str(size)   
		else:
			headerString = srctype + "111" + str(size)
		headerArray = [int(s) for s in headerString]
		header = numpy.array(headerArray)
		print header
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
			header = self.get_header(length, '1')
		else:
			databits = numpy.ones(1000)
			length = len(databits)
			#header should return a numpy array
			header = self.get_header(length, '0')
		payload = databits
		databits = numpy.concatenate([header,databits])
		print databits
		return payload, databits
