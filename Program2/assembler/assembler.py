import re

symbols = {}
runningOp = ""
objectCode = ""
errorCount = 0


class Code:
    def __init__(self, lineList):
        self.lineList = lineList
        self.compLines = self.getAddresses()
        print("Assembling")
        self.compileLines()
        byteCount = len(runningOp.split(" ")) - 1
        print("--End assembly, " + str(byteCount) + " bytes, Errors: " + str(errorCount))
        symbolTable = {}
        for i in symbols.keys():
            if symbols[i]["val"] == "":
                symbolTable[i] = "$" + hex(symbols[i]["addr"])[2:].upper()
            else:
                symbolTable[i] = symbols[i]["val"]

        alphOrder = sorted(symbolTable.keys(), key=lambda x: x.lower())
        print("Symbol table - alphabetical order:")
        alphStr = ""
        count = 0
        for i in alphOrder:
            if count == 4:
                alphStr += "\n"
                count = 0
            alphStr += "{s:4}{name:<9}={var}".format(s=" ", name=i, var=symbolTable[i])
            count += 1
        print(alphStr)
        numOrder = sorted(symbolTable.keys(), key=lambda x: symbolTable[x].lower())
        print("Symbol table - numerical order:")
        numStr = ""
        count = 0
        for i in numOrder:

            if count == 4:
                numStr += "\n"
                count = 0
            numStr += "{s:4}{name:<9}={var}".format(s=" ", name=i, var=symbolTable[i])
            count += 1
        print(numStr)

    def getObjectCode(self):
        global objectCode
        return objectCode

    def getAddresses(self):
        pc = int("8000", base=16)
        count = 1
        lines = []
        for i in self.lineList:
            if pc > int("ffff", base=16):
                print("Memory Full")
                exit()
            if len(symbols) > 254:
                print("Memory Full")
                exit()
            line = self.Line(i, pc, count)
            if i[0] != "*":
                if line.instr not in INST_LIST:
                    print("Bad opcode in line: " + str(count))
                    exit()
                if line.label != "":
                    if line.label in symbols.keys():
                        global errorCount
                        input("Duplicate Symbol in line: " + str(count))
                        errorCount += 1
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
        return lines

    def compileLines(self):
        for i in self.compLines:
            if not i.isComment:
                if not i.errored:
                    i.compressOpCode()
                if not i.errored:
                    i.getInstrCode()
                if not i.errored:
                    i.getOpCode()
                if not i.errored:
                    i.addRunning()
            print(str(i))

    class Line:
        def __init__(self, lineStr, addr, lineNum):
            self.errored = False
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
            elif self.instr in ["EQU", "ORG", "END"] or self.errored:
                formattedStr = "{h:>7}{c:<3} {o:<5}{n:>3}  ".format(h="", c="",
                                                                    o="",
                                                                    n=self.lineNum)
            else:
                formattedStr = "{h:>5}: {c:<3} {o:<5}{n:>3}  ".format(h=hex(self.addr)[2:].upper(), c=self.instrCode,
                                                                      o=self.opCode,
                                                                      n=self.lineNum)
            return formattedStr + self.lineStr.strip("\n")

        def getInstrCode(self):
            global runningOp
            mode = self.getAddressingMode()
            if self.instr == "CHK":
                codeList = runningOp.split(" ")
                xor = int("00", base=16)
                for i in codeList:
                    if len(i) == 2:
                        xor = xor ^ int(i, base=16)
                self.instrCode = hex(xor)[2:].upper()
            if not isPseudoInstr(self.instr):
                try:
                    instrCode = INSTR_LIB[self.instr][mode]
                    self.instrCode = instrCode
                except KeyError:
                    self.flagErr()
                    input("Bad address mode in line: " + str(self.lineNum))

        def getOpCode(self):
            opCode = self.op.split(",")[0]
            opCode = opCode.replace("#", "")
            opCode = opCode.replace("(", "")
            opCode = opCode.replace(")", "")
            if isBranch(self.instr):
                if int(opCode, base=16) > self.addr:
                    # Branch to later
                    addr = abs(self.addr - int(opCode, base=16)) - 2
                    opCode = hex(int("00", base=16) + addr)[2:].upper()
                else:
                    addr = int(opCode, base=16) - self.addr - 1
                    opCode = hex(int("FF", base=16) + addr)[2:].upper()

            if isPseudoInstr(self.instr):
                self.opCode = ""
                return

            if self.op != "":
                self.opCode = formatHex(opCode)
            else:
                self.opCode = ""

        def getAddressingMode(self):
            addrRegex = [
                ("im", r'#[A-Z|a-z|0-9]{2}'),
                ("ab", r'[A-Z|a-z|0-9]{4}'),
                ("abx", r'[A-Z|a-z|0-9]{4}' + r',X'),
                ("aby", r'[A-Z|a-z|0-9]{4}' + r',Y'),
                ("zp", r'[A-Z|a-z|0-9]{2}'),
                ("zpx", r'[A-Z|a-z|0-9]{2}' + r',X'),
                ("zpy", r'[A-Z|a-z|0-9]{2}' + r',Y'),
                ("inx", r'\([A-Z|a-z|0-9]{2},X\)'),
                ("iny", r'\([A-Z|a-z|0-9]{2}\),Y'),
                ("in", r'\([A-Z|a-z|0-9]{4}\)'),
                ("rel", r'/[A-Z|a-z|0-9]{2}/gm')
            ]
            accList = ["ASL", "LSR", "ROL", "ROR"]
            if self.instr != "":
                if not isPseudoInstr(self.instr):
                    options = INSTR_LIB[self.instr]
                    # print(str(options) + " " + self.op)
                    mode = "im"
                    if self.op == "":
                        mode = "imp"
                        if self.instr in accList:
                            mode = "acc"
                    for type, reg in addrRegex:
                        result = re.fullmatch(reg, self.op)
                        if result:
                            mode = type
                    if "#" in self.op:
                        mode = "im"
                    if len(options) == 1:
                        if "in" not in mode:
                            mode, = options.keys()
                    if isJump(self.instr):
                        if mode == "zp":
                            mode = "ab"
                    return mode
            return "imp"

        def compressOpCode(self):
            trimmedOp = self.op.split(",")
            opList = re.findall(r'[+-/*!.&#$%]|\w+|\W+', trimmedOp[0])
            next = ""
            evalStr = ""
            for i in opList:
                if i == "$":
                    next = "hex"
                    continue
                if i == "%":
                    next = "bin"
                    continue
                if i == "*":
                    evalStr += self.addr

                if next == "hex":
                    evalStr += str(int(i, base=16))
                    next = ""
                    continue
                if next == "bin":
                    evalStr += str(int(i, base=2))
                    next = ""
                    continue

                if i in symbols.keys():
                    # Turn it into the evaluation
                    if isBranch(self.instr):
                        if symbols[i]["val"] != "":
                            self.flagErr()
                            input("Bad branch in line: " + str(self.lineNum))
                        evalStr += str(symbols[i]["addr"])
                    elif isJump(self.instr):
                        content = symbols[i]
                        if content["val"] == "":
                            evalStr += str(content["addr"])
                        else:
                            content = symbols[i]["val"]
                            if content[0] == "$":
                                evalStr += str(int(content[1:], base=16))
                            if content[0] == "%":
                                evalStr += str(int(content[1:], base=2))
                    else:
                        content = symbols[i]["val"]
                        if content[0] == "$":
                            evalStr += str(int(content[1:], base=16))
                        if content[0] == "%":
                            evalStr += str(int(content[1:], base=2))

                else:
                    if isBranch(self.instr):
                        self.flagErr()
                        input("Bad branch in line: " + str(self.lineNum))
                    evalStr += i
            opList = re.findall(r'[+-/*!.&#$%]|\w+|\W+', evalStr)
            result = 0
            prev = None
            imm = False
            ind = False
            nextOp = ""
            for i in opList:
                if i == "#":
                    imm = True
                    continue
                if i == "(" or i == ")":
                    ind = True
                    continue
                elif i in "+-/*!.&":
                    nextOp = i
                    continue

                if nextOp == "+":
                    result = prev + int(i)
                    prev = prev + int(i)
                elif nextOp == "-":
                    result = prev - int(i)
                    prev = prev - int(i)
                elif nextOp == "/":
                    result = int(prev / int(i))
                    prev = int(prev / int(i))
                elif nextOp == "*":
                    result = prev * int(i)
                    prev = prev * int(i)
                elif nextOp == "!":
                    result = prev ^ int(i)
                    prev = prev ^ int(i)
                elif nextOp == ".":
                    result = prev | int(i)
                    prev = prev | int(i)
                elif nextOp == "&":
                    result = prev & int(i)
                    prev = prev & int(i)
                else:
                    if result == 0:
                        result = int(i)
                        prev = int(i)
                    else:
                        prev = int(i)
            ret = hex(result)[2:].upper()
            if len(ret) < 2:
                ret = ret.rjust(2, "0")
            if 2 < len(ret) < 4:
                ret = ret.rjust(4, "0")
            if imm:
                ret = "#" + ret
            if ind:
                ret = "(" + ret
            self.op = ret
            if len(trimmedOp) > 1:
                if trimmedOp[1] == "Y":
                    self.op = ret + ")," + trimmedOp[1]
                else:
                    self.op = ret + "," + trimmedOp[1]
            elif self.op[0] == "(":
                self.op += ")"

            if len(opList) == 0:
                self.op = ""

        def addRunning(self):
            global runningOp
            global objectCode
            if self.instrCode != "":
                runningOp += self.instrCode + " "
            if self.opCode != "":
                runningOp += self.opCode + " "
            if self.instrCode != "":
                objectCode += "{h:>5}: {c:<3} {o:<5}\n".format(h=hex(self.addr)[2:].upper(), c=self.instrCode,
                                                               o=self.opCode)

        def flagErr(self):
            global errorCount
            errorCount += 1
            self.errored = True


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

INST_LIST = ['ADC', 'AND', 'ASL', 'BCC', 'BCS', 'BEQ', 'BIT', 'BMI', 'BNE', 'BPL', 'BRK', 'BVC', 'BVS', 'CLC', 'CLD',
             'CLI', 'CLV', 'CMP', 'CPX', 'CPY', 'DEC', 'DEX', 'DEY', 'EOR', 'INC', 'INX', 'INY', 'JMP', 'JSR', 'LDA',
             'LDX', 'LDY', 'LSR', 'NOP', 'ORA', 'PHA', 'PHP', 'PLA', 'PLP', 'ROL', 'ROR', 'RTI', 'RTS', 'SBC', 'SEC',
             'SED', 'SEI', 'STA', 'STX', 'STY', 'TAX', 'TAY', 'TSX', 'TXA', 'TXS', 'TYA', 'CHK', 'END', 'EQU', 'ORG']
