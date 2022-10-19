from random import random
import numpy as np


class Hamming:
    """The class that contains all functionality for encoding, 
    decoding, and error correcting a random message of any given lenth"""

    def __init__(self, size, errPercent = 0.5):
        """Init:
            Params:
            size: int - The size of the message the user wants to create
            errPercent: float(0-1) - The percentage chance that there will be an error in the created message"""
        # Class variables:
        self.dataBits = size
        self.errPercent = errPercent
        self.msg = []
        # Create random message of length size
        self.createMsg()
        
        # Calculate the number of parity and data bits required
        self.parityBits = self.getParityBits()
        # Total number of bits in the encoded message
        self.totalBits = 2 ** self.parityBits - 1

        # The code generator matrix for the hamming code
        self.G = self.createGen()
        # The parity check matrix for the hamming code
        self.H = self.createCheck()
        #Encode the message
        self.encoded = self.encode()
        # Set a random error in the message based on % chance there is one
        self.errorEncoded = []
        self.setError()
        # Select what row is required from the parity check matrix
        self.P = []
        self.getErrLocation()
        # Correct the matrix, this runs no matter what, but will return the same matrix if there is no error
        self.corrected = []
        self.correctError()
        # Create decoding matrix
        self.R = []
        self.createRecv()
        # Decode the message
        self.decoded = self.decode()

    def getParityBits(self):
        """Gets the number of parity bits, and sets the number of data bits"""
        n = 0
        count = 1
        while n - self.dataBits <= count:
            count += 1
            n = pow(2, count)
        self.dataBits = n - count - 1
        return count

    def createGen(self):
        """Creates the generator matrix for the Hamming code"""
        G = np.zeros((self.totalBits - self.parityBits, self.totalBits), dtype=np.uint) # k x n

        paritySet = set([2 ** i - 1 for i in range(self.parityBits)])
        dataSet = set(range(self.totalBits)) - paritySet

        # fills in parity bit columns of the generator matrix
        for par in paritySet:
            for i, data in enumerate(dataSet):
                if (par + 1) & (data + 1) != 0:
                    G[i][par] = 1

        # fills in data bit columns of the generator matrix
        for i, data in enumerate(dataSet):
            G[i][data] = 1

        return G

    def createCheck(self):
        """Creates the parity check matrix for the Hamming code"""
        paritySet = set([2 ** i - 1 for i in range(self.parityBits)])
        dataSet = set(range(self.totalBits)) - paritySet
        #n = total r = parity
        H = np.zeros((self.totalBits, self.parityBits), dtype=np.uint) # n x r

        # filling in parity bit rows of the parity check matrix
        for data in dataSet:
            for i in range(self.parityBits):
                H[data, i] = int(((data + 1) >> i) & 1)
     
        # filling in data bit rows of the parity check matrix
        for i, par in enumerate(paritySet):
            H[par][i] = 1  
        return H

    def setError(self):
        """If the random number is greater than the chance, set a random error in the message"""
        chance = random()
        self.errorEncoded = self.encode()
        if chance > 1 - self.errPercent:
            spot = int((random() * 100) % len(self.errorEncoded))
            self.errorEncoded[spot] = (self.errorEncoded[spot] + 1) % 2
        

    def createMsg(self):
        """Creates a message of declared length"""
        for _ in range(self.dataBits):
            # Add a random bit to each point in the msg. This creates the original message based off a size
            rnd = random()
            self.msg.append(int((rnd * 100) % 2))

    def encode(self):
        """Encodes the message using the code generator matrix G"""
        while len(self.msg) < self.dataBits:
            self.msg.append(0)
        return np.dot(self.msg, self.G) % 2

    def getRow(self, row):
        """Searches for a row in the parity-check matrix and returns its index.
           Returns -1 if not found."""
        try:
            i = np.where(np.all(self.H == row, axis=1))[0][0]
            self.P = self.H[i]
            return np.where(np.all(self.H == row, axis=1))[0][0]
        except IndexError:
            return -1

    def getErrLocation(self):
        """Returns the location of an error
           Returns -1 if there is no error"""
        return self.getRow(np.dot(self.errorEncoded, self.H) % 2)
        
    def correctError(self):
        """Grabs the location of the error. If there is an error, it flips the bit at the found location"""
        errLoc = self.getErrLocation()
        ar = np.array(self.errorEncoded)
        if errLoc:
            ar[errLoc] = (ar[errLoc] + 1) % 2
        self.corrected = ar

    def createRecv(self):
        """Creates the decoding matrix for the Hamming code"""
        G = np.zeros((self.totalBits - self.parityBits, self.totalBits), dtype=np.uint) # k x n
        P = [2 ** i - 1 for i in range(self.parityBits)]
        ran = 0
        # Loop through all rows
        for i in range(len(G)):
            # Loop through all columns
            for j in range(len(G[0])):
                # If j is greater than where the previous loop got to, keep going
                if j > ran:
                    # Makes sure the column isn't a parity column
                    if j not in P:
                        G[i][j] = 1
                        ran = j
                        break     
        # Return the transpose of the matrix for formatting purposes     
        self.R = G.transpose()

    def decode(self):
        """Decodes the matrix using the R matrix and returns the original message"""
        return np.dot(self.corrected, self.R) 
        


    def print(self):
        """Helper function for pretty formatting"""
        print("Message          : " + str(np.array(self.msg)))
        print("Send Vector      : " + str(self.encoded))
        print("Recieved Message : " + str(self.errorEncoded))
        print("Parity Check     : " + str(self.P))
        print("Corrected Message: " + str(self.corrected))
        print("Decoded Message  : " + str(self.decoded))
        


def getInput():
    """Gets the user's input for number of data bits in the message"""
    return input("Enter number of databits: ")


if __name__ == "__main__":
    inp = 0
    # Loop to make sure the input is an integer
    while True:
        try:
            inp = int(getInput())
            break
        except ValueError:
            print("Please ensure input is an integer!")
            continue
    # Create the hamming object, and all the requred information about it
    ham = Hamming(inp, errPercent = 0.0)
    ham.print()

