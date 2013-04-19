# audiocom library: Source and sink functions
import common_srcsink
import Image
import ImageDraw
from graphs import *
import binascii
import random
import numpy
from scipy.misc import toimage


class Sink:
    def __init__(self):
        # no initialization required for sink 
        print 'Sink:'

    def process(self, recd_bits):
        source, size = self.read_header(recd_bits)
        #truncate recd_bits to get rid of header
        rcd_payload = numpy.array([])
        rcd_payload = recd_bits[20:]
        rcd_payload= rcd_payload[:int(size,2)]
        #sed rcd_payload to the truncated array
        if source == '000':
            msg = self.bits2text(rcd_payload)
        elif source == '001':
            self.image_from_bits(rcd_payload, "rcdImage.png")
            msg = 'Image received'
        elif source == '111':
            msg = 'monotone'
        else:
            msg = 'unrecognizeed sourcetype: ' + source
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
        byteArray=numpy.reshape(bits, (-1,8))
        valArray = [None]*(len(bits)/8)
        i = 0
        strVal = ""

        for bA in byteArray:
            for val in bA:
                strVal = strVal + str(val)
                #print strVal
            valArray[i] = strVal
            i += 1
            strVal = ""


        charArray = [None]*(len(bits)/8)
        i = 0
        for vA in valArray:
            intVal = int(vA, 2)
            charVal = chr(intVal)
            charArray[i]=charVal
            i+=1

        text=""
        for ch in charArray:
            text+=ch
        print text

        myfile = open('test.txt','w')
        myfile.write(text)
        myfile.close()
        
        return text

    def image_from_bits(self, bits, filename):
       
        # make every eight bits into a byte
        #bits = bits[]
        byteArray=numpy.reshape(bits, (-1,8))
        # group bytes into one array of multiple arrays of length 8
        stringBins = []
        decimals = []
        pixelPairs = []


        for bA in byteArray:
            string = ""
            for k in bA:
                string += str(k)
            stringBins.append(string)

        for v in stringBins:
            decimals.append(int(v, 2))


        #pixelPairs = numpy.reshape(numpy.array(decimals), (-1, 2))

        numpyDec = numpy.array(decimals)
        dimension = 32
        #im = Image.fromarray(numpyPairs)
        im = Image.new("L", (dimension, dimension))
        im.putdata(numpyDec)
        im.save(filename)
        im.show()

       
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
        print payload_length


        print '\tRecd header: ', header
        print '\tLength from header: ', payload_length
        print '\tSource type: ', srctype
        return srctype, payload_length