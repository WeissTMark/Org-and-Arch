import sys
from try5 import Code
from structure import File


def main():

    num = input("What file do you want to test: ")
    fileName = '../sample_files/sample_{num}.s'.format(num=num)
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
