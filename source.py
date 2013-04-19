# audiocom library: Source and sink functions
import common_srcsink as common
import Image
from graphs import *
import random
import numpy


class Source:
	def __init__(self, monotone, filename=None):
		# The initialization procedure of source object
		self.monotone = monotone
		self.fname = filename
		print 'Source: '

	def process(self):
		# Form the databits, from the filename 
		if self.fname is not None:
			databits= numpy.array([])
			if self.fname.endswith('.png') or self.fname.endswith('.PNG'):
				databits = self.bits_from_image(self.fname)
			else:
				databits = self.text2bits(self.fname)
			length = len(databits)  
			header = self.get_header(length, '1')
		else:
			# Creates an array of bits for sending monotone
			databits = numpy.ones(1000)
			length = len(databits) 
			header = self.get_header(length, '0')
		# payload now has data bits of file
		payload = databits
		# databits now has header appended to payload
		databits = numpy.concatenate([header, payload])
		return payload, databits

	def text2bits(self, filename):
		binVals = []
		endArray = []
		f = open(filename, "r")
		while 1: 
			line = f.readline()
			if not line:
				break
			else:
				# newValues holds ascii vals for chars in txt file
				newValues = [ord(c) for c in line]
		# Converts ascii vals into bin vals
		i = 0
		for v in newValues:
			intV = int(v)
			newValues[i] = bin(intV)[2:].zfill(8)
			i+=1
		# Converts string representations of bin vals into int representations
		for v in newValues:
			for c in v:
				endArray.append(int(c))
		# Converts int array into numpy int array
		bits = numpy.array(endArray)	
		return bits

	def bits_from_image(self, filename):
		binPix = []
		bitsCopy = [] 
		im = Image.open(filename)
		im = im.convert("L")
		pixelValues = list(im.getdata())
		# Converts pixel vals into binary strings of standard length 8
		for v in pixelValues:
			binPix.append(bin(v)[2:].zfill(8))
		# Creates an array of bits represented as strings
		flatVals = [val for sub in binPix for val in sub]
		# Converts string representations of bits into int representations
		bitsCopy=[int(s) for s in flatVals]
		# Converts int array into numpy int array
		bits = numpy.array(bitsCopy)
		return bits

	def get_header(self, payload_length, srctype): 		
		headerArray = []
		size = bin(payload_length)[2:].zfill(16)
		if self.fname is not None:
			# Encodes header depending on srctype and size of file
			# '000' -> txt, '001' -> png, '111' -> monotone
			if self.fname.endswith('.png') or self.fname.endswith('.PNG'):
				headerString = srctype + "001" + str(size)
			else:
				headerString = srctype + "000" + str(size)   
		else:
			headerString = srctype + "111" + str(size)
		# Converts string representation of header into a numpy int array
		headerArray = [int(s) for s in headerString]
		header = numpy.array(headerArray)
		return header


