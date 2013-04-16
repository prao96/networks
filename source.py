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
		binvals = []
		while 1:
			line = file.readline()
			if not line:
				break
			else:
				#str is an ascii string of characters
				newValues = [ord(c) for c in line]
				i=0
				for v in newValues:
					newValues[i]=[int(x) for x in list('{0:0b}'.format(8))]
					i+=1
				values+=newValues
		i=0
		for k in values:
			binvals.append(list(k))
			i +=1
		bits = numpy.array(binvals)
		bits = numpy.ravel(bits)
		print bits
		return bits

	def bits_from_image(self, filename):
		file = open(filename)
		image = file
		image_64 = base64.encodestring(open(image, "l").read())
		str = binascii.a2b_base64(image_64)
		bits = binascii.a2b_qp(str)
		length = len(bits)
		header = get_header(self, length, '01')
		bits = binascii.a2b_qp(header + str)
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
				databits = self.bits_from_image(self, self.fname)
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
