import sys

from assembler.scratch import scratch
from assembler.try4 import Code
from structure import File


def main():
    fileName = sys.argv[1]
    l = []
    with open(fileName, mode="r") as file:
        inc = 0
        while True:
            inc += 1
            f = file.readline()
            if not f:
                break
            l.append(f)
    # fil = File(l)
    Code(l)


if __name__ == "__main__":
    main()
