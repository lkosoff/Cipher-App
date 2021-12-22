import numpy as np
from PIL import Image


class Img:
    def __init__(self, filename):
        img = Image.open(filename)
        self.img = img
        originalPixels = img.getdata()
        self.width, self.height = img.size
        self.pixels = [[r, g, b] for (r, g, b) in originalPixels]

    #gets a pixel value

    def getPixel(self, i):
        return self.pixels[i]

    #sets the values of pixel
    def setPixel(self, i, val):
        self.pixels[i] = val

    #shows image. If filename give, saves with that filename
    def show(self, fname=None):
        endPixels = [(r, g, b) for r, g, b in self.pixels]
        newim = Image.new(self.img.mode, self.img.size, color=None)
        newim.putdata(endPixels)

        if fname:
            newim.save(fname)
        else:
            newim.show()

    #encodes a 3 bit long message
    def encodePixel(self, index, bit):
        i = int(index/3)  # ith pixel
        j = index % 3   # color from that pixel
        pixels = self.getPixel(i)
        pixels[j] = ((pixels[j] >> 1) << 1) | bit

    def encode(self, message):
        bits = messageToBits(message)
        for i, bit in enumerate(bits):
            self.encodePixel(i, bit)

    def decode(self):
        message = ""
        nullChar = "_"
        offset = 0
        while nullChar not in message:
            # selects the next 8 pixels to convert to strings
            pixels = [self.getPixel(i+offset) for i in range(8)]
            message += pixelToMessage(pixels)
            offset += 8

        cleanMessage = (message.split(nullChar, 1))[0]
        return cleanMessage


# converts number into 8 bits
def numToByte(num):
    bits = []
    for _ in range(8):
        bits = [num % 2] + bits
        num = int(num/2)
    return bits

# converts 8 bits into a number


def byteToNum(byte):
    num = 0
    multi = 128
    for b in byte:
        num += multi * b
        multi /= 2

    return int(num)

#converts message into array of 1's and 0's


def messageToBits(message):
    message += "_"  # null terminating character

    bits = [numToByte(ord(letter)) for letter in message]
    result = np.reshape(bits, (np.size(bits), ))

    return result

#converts a pixel into a length 3 array of 1's and 0's


def pixelToBits(pixel):
    return [pixel[0] % 2, pixel[1] % 2, pixel[2] % 2]

#converst a list of pixels to a message. pixelList is always a list of 8 pixels


def pixelToMessage(pixelList):
    bits = [pixelToBits(p) for p in pixelList]
    # group pixels into a list of "bytes"
    byteList = np.reshape(bits, (int(np.size(bits)/8), 8))
    # convert list of "bytes" into characters
    message = "".join([chr(byteToNum(byte)) for byte in byteList])
    return message


def encodeImage(fname, saveName, mes):
    img = Img(fname)
    img.encode(mes)
    img.show(saveName)


def decodeImage(fname):
    img = Img(fname)
    result = img.decode()
    return result


def main():
    inp = input("Encode(1) or Decode(2)?: ")
    if inp.startswith(("e", "1", "E")):
        fname = input("Filename: ")
        mes = input("Message:  ")
        newfile = input("New filename (use '.png'): ")
        encodeImage(fname, newfile, mes)

    if inp.startswith(("d", "2", "D")):
        fname = input("Filename: ")
        decodeImage(fname)


if __name__ == "__main__":
    main()
