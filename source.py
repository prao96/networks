# audiocom library: Source and sink functions
import common_srcsink as common
import Image
from graphs import *
import binascii
import random
import base64


class Source:
    def __init__(self, monotone, filename=None):
        # The initialization procedure of source object
        self.monotone = monotone
        self.fname = filename
        print 'Source: '

    def process(self):
            # Form the databits, from the filename 
            if self.fname is not None:
                if self.fname.endswith('.png') or self.fname.endswith('.PNG'):
                   databits = bits_from_image(self, self.fname)
                else:           
                    databits = text2bits(self, self.fname)  
				    length = len(databits)               
            else:               
                databits = np.ones(1000)
			    header = get_header(self, len(databits), '1')
			    databits = binascii.a2b_qp(header) + databits
            return payload, databits

    def text2bits(self, filename):
		file = open(filename)
		while 1:
        # Form the databits, from the filename 
        if self.fname is not None:
            if self.fname.endswith('.png') or self.fname.endswith('.PNG'):
                databits = bits_from_image(self, self.fname)
            else:           
                databits = text2bits(self, self.fname)  
                length = len(databits)               
        else:               
            databits = np.ones(1000)
            header = get_header(self, len(databits), '1')
            databits = binascii.a2b_qp(header) + databits
        return payload, databits

    def text2bits(self, filename):
        file = open(filename)
        while 1:
			line = file.readline()
    			if not line:
        			break
    			else:
				    str = binascii.a2b_uu(line)
				    bits = binascii.a2b_qp(str)
		            length = len(bits)
		            header = get_header(self, length, '01')
		            bits = binascii.a2b_qp(header + str)
				str = binascii.a2b_uu(line)
				bits = binascii.a2b_qp(str)
		length = len(bits)
		header = get_header(self, length, '01')
		bits = binascii.a2b_qp(header + str)
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
