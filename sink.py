# audiocom library: Source and sink functions
import common_srcsink
import Image
from graphs import *
import random
import numpy

class Sink:
    def __init__(self):
        # no initialization required for sink 
        print 'Sink:'

    def process(self, recd_bits):
        source, size = self.read_header(recd_bits)
        # Truncate recd_bits to get rid of header
        rcd_payload = numpy.array([])
        rcd_payload = recd_bits[20:]
        rcd_payload= rcd_payload[:int(size,2)]
        # Calls corresponding process based on srctype
        if source == '000':
            msg = self.bits2text(rcd_payload)
        elif source == '001':
            self.image_from_bits(rcd_payload, "rcd-img.png")
            msg = 'Image received'
        elif source == '111':
            msg = 'Monotone'
        else:
            msg = 'Sorry, unrecognized sourcetype: ' + source
        print msg
        return rcd_payload

    def bits2text(self, bits):
        # valArray will contain decimal representations of bytes
        valArray = [None]*(len(bits)/8)
        # charArray will contain the characters in the txt file
        charArray = [None]*(len(bits)/8)
        i = 0
        strVal = ""
        # Groups bits into bytes
        byteArray=numpy.reshape(bits, (-1,8))
        # Creates a string representation of every byte 
        for bA in byteArray:
            for val in bA:
                strVal = strVal + str(val)
            valArray[i] = strVal
            i += 1
            strVal = ""   
        # Creates a character representation of every byte     
        i = 0
        for vA in valArray:
            intVal = int(vA, 2)
            charVal = chr(intVal)
            charArray[i]=charVal
            i+=1
        # Appends characters to reform text
        text=""
        for ch in charArray:
            text+=ch
        # Writes text to test file for debugging purposes
        myfile = open('test.txt','w')
        myfile.write(text)
        myfile.close()        
        return text

    def image_from_bits(self, bits, filename): 
        stringBins = []
        decimals = []
        # Groups bits into bytes
        byteArray=numpy.reshape(bits, (-1,8))
        # Creates a string representation of every byte
        for bA in byteArray:
            string = ""
            for k in bA:
                string += str(k)
            stringBins.append(string)
        # Creates pixel vals from string representations of bytes
        for v in stringBins:
            decimals.append(int(v, 2))
        # Creates a numpy array of ints
        numpyDec = numpy.array(decimals)
        # Standard size of image file
        dimensions = (32, 32)
        # Creates a grayscale image from bits received
        im = Image.new("L", dimensions)
        im.putdata(numpyDec)
        # Save image as filename
        im.save(filename)       
        pass 

    def read_header(self, header_bits): 
        payload_length = ""
        # Creates header from first 20 bits
        header = header_bits[:20]
        # Decodes srctype
        srctype = str(header[1]) + str(header[2]) + str(header[3])
        # Decodes payload_length
        i=4
        while i<20:
            payload_length+=str(header[i])
            i+=1
        print '\tRecd header: ', header
        print '\tLength from header: ', payload_length
        print '\tSource type: ', srctype
        return srctype, payload_length