from math import log
from random import random


class bit:
    def __init__(self, loc):
        self.bit = False
        self.location = loc
        self.parity = self.isParity()

    def isParity(self):
        if self.location == 1:
            return True
        val = log(self.location, 2)
        return val.is_integer()

    def set(self, val: bool):
        self.bit = val


class Hamming:
    def __init__(self, size):
        self.dataBits = size
        self.parityBits = self.getParityBits()
        self.totalBits = self.dataBits + self.parityBits
        self.parityMap = self.makeParityMap()
        self.G = []
        self.H = []
        self.R = []
        self.msg = []
        self.create()
        self.createMatrices()

    def getParityBits(self):
        n = 0
        count = 1
        while n <= self.dataBits:
            count += 1
            n = pow(2, count)
        return count

    def makeParityMap(self):
        bitMap = [[False for y in range(self.totalBits)] for x in range(self.parityBits)]
        for i in range(self.parityBits):
            count = 0
            start = False
            for j in range(self.totalBits):
                if j >= i:
                    if bit(j+1).parity:
                        start = True
                    if start:
                        if count <= i + 1:
                            count += 1
                            bitMap[i][j] = True
                        else:
                            count = 0
        print(bitMap)
        return bitMap

    # This function creates the G, H, and R matrices for use by the algorithm
    def createMatrices(self):
        for i in range(self.totalBits):
            self.G.append(bit(i + 1))
            print(self.G[i].parity)

    # Creates the random bits of declared size that determines our starting message
    def create(self):
        for i in range(self.dataBits):
            # Add a random bit to each point in the msg. This creates the original message based off a size
            rnd = random()
            self.msg.append(int((rnd * 100) % 2))


def getInput():
    return input("Enter the number of databits: ")


if __name__ == "__main__":
    inp = 0
    while True:
        try:
            inp = int(getInput())
            break
        except ValueError:
            print("Please ensure input is an integer!")
            continue

    ham = Hamming(inp)
