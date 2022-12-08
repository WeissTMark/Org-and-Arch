import sys
from assembler import Code


def generateObjectFile(fileName, objectCode):
    with open(fileName, mode="w") as file:
        file.write(objectCode)


def assembleFile(fileName):
    l = []
    with open(fileName, mode="r") as file:
        inc = 0
        while True:
            inc += 1
            f = file.readline()
            if not f:
                break
            l.append(f)
    c = Code(l)
    return c.getObjectCode()


if __name__ == "__main__":
    fileDir = sys.argv[1]
    fileDir = fileDir[0:-2]
    fileName = '{dir}.{form}'.format(dir=fileDir, form="s")
    objectCode = assembleFile(fileName)
    outName = '{dir}.{form}'.format(dir=fileDir, form="o")
    generateObjectFile(outName, objectCode)
