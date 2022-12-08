import re

symbols = {}


class Code:
    def __init__(self, lineList):
        self.lineList = lineList
        self.compLines = self.getAddresses()
        self.compileLines()

    def getAddresses(self):
        pc = int("8000", base=16)
        count = 1
        lines = []
        for i in self.lineList:
            line = self.Line(i, pc, count)
            if i[0] != "*":
                if line.label != "":
                    if line.label in symbols.keys():
                        print("Duplicate Symbol in line: " + str(count))
                    elif line.instr == "EQU":
                        symbols[line.label] = {'addr': pc, 'val': line.op}
                    else:
                        symbols[line.label] = {'addr': pc, 'val': ""}
                if line.instr == "ORG":
                    pc = int(re.sub(r'\W+', '', line.op.split(",")[0]), base=16)
                elif line.instr == "CHK":
                    pc += 1
                elif not isPseudoInstr(line.instr):
                    pc += line.getHexLen()
            count += 1
            lines.append(line)
        print(str(symbols))
        return lines

    def compileLines(self):
        for i in self.compLines:
            if not i.isComment:
                i.getInstrCode()
                i.getOpCode()
            print(str(i))

    class Line:
        def __init__(self, lineStr, addr, lineNum):
            self.opCode = ""
            self.instrCode = ""
            self.isComment = False
            if lineStr[0] == "*":
                self.isComment = True
            self.lineStr = lineStr
            self.addr = addr
            self.lineNum = lineNum
            self.label = lineStr[0:8].strip()
            self.instr = lineStr[9:13].strip()
            self.op = lineStr[14:24].strip()

        def getHexLen(self):
            instrLen = 1
            opLen = 0

            if isJump(self.instr):
                opLen = 2
                # Perform more error checks here
            elif isBranch(self.instr):
                opLen = 1
                # Perform more error checks here
            else:
                opList = re.findall(r'[+-/*!.&#$%]|\w+|\W+', self.op)
                opCode = ""
                next = ""
                for item in opList:
                    # Calculate arithmatic here
                    # Get value in hex and get length
                    check = item

                    tmp = symbols.get(item)
                    if tmp:
                        if isBranch(self.instr):
                            check = str(tmp["addr"])
                        else:
                            check = str(tmp["val"])
                    if item == "*":
                        opCode += self.addr
                    elif next == "hex":
                        next = ""
                        opCode += hex(int(check, base=16))[2:]
                    elif next == "bin":
                        next = ""
                        opCode += hex(int(check, base=2))[2:]
                    elif check == "$":
                        next = "hex"
                    elif item == "%":
                        next = "bin"
                    elif re.match(r'[0-9]+', check):
                        opCode += hex(int(check))[2:]
                if self.op != "":
                    opCode = formatHex(opCode)
                opLen = int(len(opCode) / 2)
            return instrLen + opLen

        def __str__(self):
            if self.lineStr[0] == "*":
                formattedStr = "{h:>7}{c:<3} {o:<5}{n:>3}  ".format(h="", c="",
                                                                    o="",
                                                                    n=self.lineNum)
            else:
                formattedStr = "{h:>5}: {c:<3} {o:<5}{n:>3}  ".format(h=hex(self.addr)[2:].upper(), c=self.instrCode,
                                                                      o=self.opCode,
                                                                      n=self.lineNum)
            return formattedStr + self.lineStr.strip("\n")

        def getInstrCode(self):
            mode = self.getAddressingMode()
            if not isPseudoInstr(self.instr):
                instrCode = INSTR_LIB[self.instr][mode]
                self.instrCode = instrCode

        def getOpCode(self):
            opList = re.findall(r'[+-/*!.&#$%]|\w+|\W+', self.op)
            opCode = ""
            next = ""
            for item in opList:
                # Calculate arithmatic here
                # Get value in hex and get length
                check = item

                tmp = symbols.get(item)
                if tmp:
                    if isBranch(self.instr):
                        check = str(tmp["addr"])
                    else:
                        check = str(tmp["val"])
                if item == "*":
                    opCode += self.addr
                elif next == "hex":
                    next = ""
                    opCode += hex(int(check, base=16))[2:]
                elif next == "bin":
                    next = ""
                    opCode += hex(int(check, base=2))[2:]
                elif check == "$":
                    next = "hex"
                elif item == "%":
                    next = "bin"
                elif re.match(r'[0-9]+', check):
                    opCode += hex(int(check))[2:]

            if isBranch(self.instr):
                if int(opCode, base=16) > self.addr:
                    # Branch to later
                    addr = self.addr - int(opCode, base=16)
                    addr = hex(int("00", base=16) + addr)
                else:
                    addr = int(opCode, base=16) - self.addr - 1
                    addr = hex(int("FF", base=16) + addr)

                opCode = addr[2:].upper()

            if self.op != "":
                opCode = formatHex(opCode)
            self.opCode = opCode.upper()

        def getAddressingMode(self):
            addrRegex = [
                ("acc", r'[A]{1}'),
                ("im", r'#[A-Z|a-z|0-9]{2}'),
                ("ab", r'[A-Z|a-z|0-9]{4}'),
                ("abx", r'[A-Z|a-z|0-9]{4}' + r',X'),
                ("aby", r'[A-Z|a-z|0-9]{4}' + r',Y'),
                ("zp", r'[\+\-\/\*\!\.\&\#\$\%][A-Z|a-z|0-9]{2}'),
                ("zpx", r'[\+\-\/\*\!\.\&\#\$\%][A-Z|a-z|0-9]{2}' + r',X'),
                ("zpy", r'[\+\-\/\*\!\.\&\#\$\%][A-Z|a-z|0-9]{2}' + r',Y'),
                ("inx", r'\([A-Z|a-z|0-9]{2},X\)'),
                ("iny", r'\([A-Z|a-z|0-9]{2}\),Y'),
                ("in", r'\([A-Z|a-z|0-9]{4}\)'),
                ("rel", r'/[A-Z|a-z|0-9]{2}/gm')
            ]
            if self.instr != "":
                if not isPseudoInstr(self.instr):
                    options = INSTR_LIB[self.instr]
                    # print(str(options) + " " + self.op)
                    mode = "imp"
                    if self.op == "":
                        mode = "imp"
                    for type, reg in addrRegex:
                        result = re.match(reg, self.op)
                        if result:
                            mode = type
                    if "#" in self.op:
                        mode = "im"
                    if len(options) == 1:
                        if "in" not in mode:
                            mode, = options.keys()
                    return mode
            return "imp"


def isJump(instr):
    jmpList = ["JSR", "JMP"]
    if instr in jmpList:
        return True
    else:
        return False


def isBranch(instr):
    brList = ["BCC", "BCS", "BEQ", "BIT", "BMI", "BNE", "BPL", "BVC", "BVS"]
    if instr in brList:
        return True
    else:
        return False


def isPseudoInstr(instr):
    pseudoList = ["CHK", "END", "EQU", "ORG"]
    if instr in pseudoList:
        return True
    else:
        return False


def formatHex(opCode):
    ret = opCode
    if len(opCode) < 2:
        ret = opCode.rjust(2, "0")
    if len(opCode) > 2:
        opCode = opCode.rjust(4, "0")
    if len(opCode) == 4:
        ret = opCode[2] + opCode[3] + " " + opCode[0] + opCode[1]

    # print(ret)
    return ret


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
    'BVC': {
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
