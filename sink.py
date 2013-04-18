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
        # Convert the received payload to text (string)

        #every eight is a byte, group into array of length 8 arrays
        byteArray=numpy.reshape(bits, (-1,8))
        #convert each byte-array into an ascii char
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

        #print valArray

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
        # while i<byteArray.shape[0]:
        #     for b in byteArray[i,:]:
        #         numpy.append(valArray, valArray[])
        #     i+=1
        # print valArray

        # #text = ""

        # #for c in valArray: 
        #     #text += c

        return  text

    def image_from_bits(self, bits,filename):
       
        # make every eight bits into a byte
        numBytes = numpy.trunc(bits.size/8)
        # group bytes into one array of multiple arrays of length 8
        byteArray = numpy.reshape(bits, (-1,8))
        asciiVals = numpy.array([])
        # for
        for b in byteArray: 
            byteString = ""
            for bit in b: 
                byteString+=str(bit)
            asciiVals.append(int(byteString,2))
        # group ascii values into one array of multiple arrays of length 2 (array of pairs)
        pairs = numpy.reshape(asciiVals, (-1, 2))
        # 2-tuples? 
        # convert pairs into pixel vals
        i = 0
        for p in pairs:
            im.getpixel((p[0],p[1]))
            i+=1

        im = Image.new('L', i) # create the image
        draw = ImageDraw.Draw(im)
        # We need an HttpResponse object with the correct mimetype
        response = HttpResponse(mimetype="image/png")
        # now, we tell the image to save as a PNG to the 
        # provided file-like object
        im.save(response, 'PNG')
        # use Image class to save image

        # not returning any val
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