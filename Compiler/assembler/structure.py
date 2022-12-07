FORMAT_LIB = {
    "$": "HEX",
    "%": "BIN",
    "O": "OCT",
    "<": "LO",
    ">": "HI"
}
INSTR_LIB = {
    "ADC": {
        "im": "69",
        "zp": "65",
        "zpx": "75",
        "ab": "6D",
        "abx": "7D",
        "aby": "79",
        "inx": "61",
        "iny": "71",
    },
    "AND": {
        "im": "29",
        "zp": "25",
        "zpx": "35",
        "ab": "2D",
        "abx": "3D",
        "aby": "39",
        "inx": "21",
        "iny": "31",
    },
    "ASL": {
        "acc": "0A",
        "zp": "06",
        "zpx": "16",
        "ab": "0E",
        "abx": "1E"
    },
    "BCC": {
        "rel": "90"
    },
    "BCS": {
        "rel": "B0"
    },
    "BEQ": {
        "rel": "F0"
    },
    "BIT": {
        "zp": "24",
        "ab": "2C"
    },
    "BMI": {
        "rel": "30"
    },
    "BNE": {
        "rel": "D0"
    },
    "BPL": {
        "rel": "10"
    },
    "BRK": {
        "imp": "00"
    },
    "BVC": {
        "rel": "50"
    },
    "BVS": {
        "rel": "70"
    },
    "CLC": {
        "imp": "18"
    },
    "CLD": {
        "imp": "D8"
    },
    "CLI": {
        "imp": "58"
    },
    "CLV": {
        "imp": "B8"
    },
    "CMP": {
        "im": "C9",
        "zp": "C5",
        "zpx": "D5",
        "ab": "CD",
        "abx": "DD",
        "aby": "D9",
        "inx": "C1",
        "iny": "D1",
    },
    "CPX": {
        "im": "E0",
        "zp": "E4",
        "ab": "EC"
    },
    "CPY": {
        "im": "C0",
        "zp": "C4",
        "ab": "CC"
    },
    "DEC": {
        "zp": "C6",
        "zpx": "D6",
        "ab": "CE",
        "abx": "DE"
    },
    "DEX": {
        "imp": "CA",
    },
    "DEY": {
        "imp": "88",
    },
    "EOR": {
        "im": "49",
        "zp": "45",
        "zpx": "55",
        "ab": "4D",
        "abx": "5D",
        "aby": "59",
        "inx": "41",
        "iny": "51",
    },
    "INC": {
        "zp": "E6",
        "zpx": "F6",
        "ab": "EE",
        "abx": "FE"
    },
    "INX": {
        "imp": "E8",
    },
    "INY": {
        "imp": "C8",
    },
    "JMP": {
        "ab": "4C",
        "in": "6C"
    },
    "JSR": {
        "ab": "20"
    },
    "LDA": {
        "im": "A9",
        "zp": "A5",
        "zpx": "B5",
        "ab": "AD",
        "abx": "BD",
        "aby": "B9",
        "inx": "A1",
        "iny": "B1",
    },
    "LDX": {
        "im": "A2",
        "zp": "A6",
        "zpy": "B6",
        "ab": "AE",
        "aby": "BE",
    },
    "LDY": {
        "im": "A0",
        "zp": "A4",
        "zpy": "B4",
        "ab": "AC",
        "aby": "BC",
    },
    "LSR": {
        "acc": "4A",
        "zp": "46",
        "zpx": "56",
        "ab": "4E",
        "abx": "5E"
    },
    "NOP": {
        "imp": "EA"
    },
    "ORA": {
        "im": "09",
        "zp": "05",
        "zpx": "15",
        "ab": "0D",
        "abx": "1D",
        "aby": "19",
        "inx": "01",
        "iny": "11",
    },
    "PHA": {
        "imp": "48"
    },
    "PHP": {
        "imp": "08"
    },
    "PLA": {
        "imp": "68"
    },
    "PLP": {
        "imp": "28"
    },
    "ROL": {
        "acc": "2A",
        "zp": "26",
        "zpx": "36",
        "ab": "2E",
        "abx": "3E"
    },
    "ROR": {
        "acc": "6A",
        "zp": "66",
        "zpx": "76",
        "ab": "6E",
        "abx": "7E"
    },
    "RTI": {
        "imp": "40"
    },
    "RTS": {
        "imp": "60"
    },
    "SBC": {
        "im": "E9",
        "zp": "E5",
        "zpx": "F5",
        "ab": "ED",
        "abx": "FD",
        "aby": "F9",
        "inx": "E1",
        "iny": "F1",
    },
    "SEC": {
        "imp": "38"
    },
    "SED": {
        "imp": "F8"
    },
    "SEI": {
        "imp": "78"
    },
    "STA": {
        "zp": "85",
        "zpx": "95",
        "ab": "8D",
        "abx": "9D",
        "aby": "99",
        "inx": "81",
        "iny": "91",
    },
    "STX": {
        "zp": "86",
        "zpy": "96",
        "ab": "8E",
    },
    "STY": {
        "zp": "84",
        "zpy": "94",
        "ab": "8C",
    },
    "TAX": {
        "imp": "AA"
    },
    "TAY": {
        "imp": "A8"
    },
    "TSX": {
        "imp": "BA"
    },
    "TXA": {
        "imp": "8A"
    },
    "TXS": {
        "imp": "9A"
    },
    "TYA": {
        "imp": "98"
    },
}


def isBranch(instr):
    if instr[0] != "B":
        return False
    if instr == "BIT" or instr == "BRK":
        return False
    return True


class File:
    def __init__(self, fileContent):
        self.content = fileContent
        self.compiledContent = []
        self.labels = {}
        self.addr = int("0000", base=16)
        for i in fileContent:
            self.compile(i)

    def compile(self, lin):
        lin = lin.strip("\n")
        lin = lin.ljust(79, " ")

        if lin[0] == "*":
            return True, "\n"
        label = ""
        for letter in range(0, 9):
            label += lin[letter]
        # print("Label: " + label)
        label = label.strip()
        if len(label) > 0:
            # We have a Label! Set the address
            self.labels[label] = self.addr

        instr = ""
        for letter in range(9, 14):
            instr += lin[letter]
        # print("Instruction: " + instr)

        op = ""
        format = ""
        immediate = False
        for letter in range(14, 25):
            if letter == 14 or letter == 15:
                if lin[letter] in FORMAT_LIB:
                    format = FORMAT_LIB[lin[letter]]
                elif lin[letter] == "#":
                    immediate = True
                else:
                    format = "AL"
                    op += lin[letter]
            else:
                op += lin[letter]

        # print("Format: " + format)
        # print("Operand: " + op)

        hexx = self.getHex(instr, op, format, immediate)
        op = hexx[2].split(",")[0]
        op = op.strip()

        if hexx[0]:
            print("*****************************")
            print(hex(self.addr) + " " + str(hexx[1]) + " " + str(op))
            hexLen = len(hexx[1]) + len(op)
            hexLen = int(hexLen / 2)
            self.addr += int(str(hexLen), base=16)
            print("HexLen: " + str(hexLen))
            print("*****************************\n")
        return True, ""

    def getHex(self, instr, op, format, immediate):
        hexCode = ""
        mode = "imp"
        instr = instr.strip()
        op = op.strip()
        preCom = op.split(",")[0]
        if instr == 'ORG':
            t = int(op, base=16)
            self.addr = t
            return False, "", ""
        elif instr == "CHK":
            # Insert Checksum
            return False, "", ""
        elif instr == "END":
            return False, "", ""
        elif instr == "EQU":
            # Set label = Expression
            return False, "", ""
        elif isBranch(instr):
            # Get addr of Branch
            mode = "rel"
            op = hex(self.labels[op])

        else:
            if immediate:
                mode = "im"
            elif op == "":
                mode = "imp"
            elif len(preCom) <= 2:
                mode = "zp"
                if ",X" in op:
                    mode = "zpx"
                elif ",Y" in op:
                    mode = "zpy"
            elif len(preCom) > 2:
                mode = "ab"
                if ",X" in op:
                    mode = "abx"
                elif ",Y" in op:
                    mode = "aby"
            elif "(" in op:
                if ",X" in op:
                    mode = "inx"
                elif ",Y" in op:
                    mode = "iny"
            elif format == "AL":
                mode = "imp"
        # print("Mode: " + instr.strip() + " " + mode.strip())

        hexCode = INSTR_LIB[instr.strip()][mode.strip()]

        # print("Hex code: " + hexCode)
        return True, hexCode, op

    def __str__(self):
        return str(self.line) + "\t" + self.content
