# audiocom library: Source and sink functions
import common_srcsink
import Image
from graphs import *
import binascii
import random
import numpy


class Sink:
    def __init__(self):
        # no initialization required for sink 
        print 'Sink:'

    def process(self, recd_bits):
        source, size = self.read_header(recd_bits)
        #truncate recd_bits to get rid of header
        rcd_payload = recd_bits[20:]
        #sed rcd_payload to the truncated array
        if source == '000':
            msg = self.bits2text(rcd_payload)
        elif source == '001':
            self.image_from_bits(rcd_payload, "rcdImage.png")
            msg = 'Image received'
        elif source == '111':
            msg = 'monotone'
        else:
            msg = 'unrecognizeed sourcetype: '+source
        print msg


        # Process the recd_bits to form the original transmitted
        # file. 
        # Here recd_bits is the array of bits that was 
        # passed on from the receiver. You can assume, that this 
        # array starts with the header bits (the preamble has 
        # been detected and removed). However, the length of 
        # this array could be arbitrary. Make sure you truncate 
        # it (based on the payload length as mentioned in 
        # header) before converting into a file.
        
        # If its an image, save it as "rcd-image.png"
        # If its a text, just print out the text
        
        # Return the received payload for comparison purposes
        return rcd_payload

    def bits2text(self, bits):
        # Convert the received payload to text (string)

        #every eight is a byte, group into array of length 8 arrays
        #convert each byte-array into an ascii char
        #push chars together to make string
        #save txt file
        return  text

    def image_from_bits(self, bits,filename):
        # Convert the received payload to an image and save it
        # No return value required .

        #every eight is a one
        #ones into pairs
        #convert to decimal
        #pairs into pixels
        #use Image class to save image
        pass 

    def read_header(self, header_bits): 
        # Given the header bits, compute the payload length
        # and source type (compatible with get_header on source)
        print header_bits
        header=numpy.zeros(20, dtype=numpy.int)
        payload_length = ""
        i = 0
        while i<20:
            header[i] = numpy.trunc(header_bits[i])
            i+=1
        print header
        srctype = str(header[1]) + str(header[2]) + str(header[3])
        print srctype

        i=4
        while i<20:
            payload_length+=str(header[i])
            i+=1


        print '\tRecd header: ', header
        print '\tLength from header: ', payload_length
        print '\tSource type: ', srctype
        return srctype, payload_length