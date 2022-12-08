import re

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


def isPseudoInstr(instr):
    pseudoList = ["CHK", "END", "EQU", "ORG"]
    if instr in pseudoList:
        return True
    else:
        return False


class Code:
    def __init__(self, lineList):
        self.lines = lineList
        self.INSTR_LIBRARY = INSTR_LIB
        self.labels = []
        self.labelList = []
        self.varList = []
        self.vars = []
        self.symbols = {}
        self.errors = []
        self.pc = 0x8000
        self.pcStart = 0x8000
        self.allHex = []
        # count = 1
        # countPC = 0x300
        # for l in lineList:
        #     line = Line(l, count, countPC, self.symbols)
        #     if line.isErrored:
        #         print(line.errors[0])
        #     countPC += self.getOpSize(l)
        #     count += 1
        #     print(str(line))
        self.getLabels()

        print(self.labels)
        print(self.vars)

        self.getHex()

        print(self.allHex)

    def getLabels(self):
        pc = 0
        for line in self.lines:

            if line[0] == "*":
                continue
            content = self.breakUp(line)
            if content["instr"] == "ORG":
                self.pc = int(content["opByts"], base=16) - 1
                self.pcStart = self.pc
                pc = int(content["opByts"], base=16)
                continue

            if content["label"] != "":
                if content["instr"] != "EQU":
                    self.labels.append({content["label"]: pc})
                    self.labelList.append(content["label"])
                    self.symbols[content["label"]] = pc
                else:
                    self.vars.append({content["label"]: content["op"]})
                    self.symbols[content["label"]] = content["op"]
                    self.varList.append(content["label"])
            if not isPseudoInstr(content["instr"]):
                # Should inc PC
                branchList = ["BCC", "BCS", "BEQ", "BMI", "BNE", "BPL", "BVC", "BVS"]
                if content["instr"] == "JMP" or content["instr"] == "JSR":
                    opBits = "FFFF"
                elif content["instr"] in branchList:
                    opBits = "FF"
                else:
                    opBits = re.sub(r'\W+', '', content["op"].split(",")[0])

                pc += int(len(opBits) / 2) + 1

    def incPC(self, amount):
        self.pc += amount

    def breakUp(self, line):
        label = line[0:8].strip()
        instr = line[9:13].strip()
        op = line[14:24].strip()
        opBits = re.sub(r'\W+', '', op.split(",")[0])
        bytLen = 1 + int((len(opBits) / 2))
        return {
            "label": label,
            "instr": instr,
            "op": op,
            "opByts": opBits,
            "bitLen": bytLen}

    def getHex(self):
        style = '{hex:>4}: {instr:<2} {op:<5} {num:>3}  '
        styleNoCode = '               {num:>3}  '
        count = 0
        for line in self.lines:
            count += 1
            if line[0] == "*":
                print(styleNoCode.format(num=count) + line.strip("\n"))
                continue
            content = self.breakUp(line)
            if content["instr"] == "CHK":
                chk = self.getCheckSum()
                print(style.format(hex=hex(self.pc)[2:].upper(), instr=chk, op="", num=count) + line.strip("\n"))
                # print("{h:<8}{c:<11}{l:>3}  ".format(h=hex(self.pc), c=chk, l=count) + line.strip("\n"))
                continue
            if isPseudoInstr(content["instr"]):
                print(styleNoCode.format(num=count) + line.strip("\n"))
                # print("{h:<8}{c:<11}{l:>3}  ".format(h="", c="", l=count) + line.strip("\n"))
                continue
            instrHex = self.getInstrHex(content["instr"], content["op"])
            opHex = ""

            if instrHex[1] == "Bad Address":
                print("Bad address mode in line: " + str(count))
                print(styleNoCode.format(num=count) + line.strip("\n"))
                # print("{h:<8}{c:<11}{l:>3}  ".format(h="", c="", l=count) + line.strip("\n"))
                continue
            if instrHex[1] == "Bad Branch":
                content["op"] = "$" + hex(self.pcStart + 1)[2:].upper()
                print("Bad branch at line: " + str(count))

            self.allHex.append(instrHex[0])
            if content["op"] != "":
                opHex = self.getOpHex(content["op"])
                if len(opHex) > 2:
                    opHex = opHex.split(" ")
                    self.allHex.append(opHex[0])
                    self.allHex.append(opHex[1])
                    opHex = " ".join([opHex[0], opHex[1]])
                else:
                    self.allHex.append(opHex)
            self.incPC(int(len(instrHex[0] + opHex) / 2))
            print(style.format(hex=hex(self.pc)[2:].upper(), instr=instrHex[0], op=opHex, num=count) + line.strip("\n"))
            # print("{h:<8}{c:<3}{o:<8}{l:>3}  ".format(h=hex(self.pc)[2:].upper(), c=instrHex[0], o=opHex, l=count) + line.strip("\n"))

    def getInstrHex(self, instr, mode):
        # options = self.INSTR_LIBRARY.get(instr, False)
        ogOp = mode
        if instr in self.INSTR_LIBRARY:
            options = self.INSTR_LIBRARY[instr]
        else:
            return ""
        isLabel = False
        isVar = False
        for label in self.labels:
            # Check for on line math ops here
            key = label.get(mode)
            if key:
                isLabel = True
                mode = key
                break
        for label in self.vars:
            # Check for on line math ops here
            key = label.get(mode)
            if key:
                isVar = True
                mode = key
                break
        if self.isBranch(instr):
            brch = self.checkBranch(ogOp)
            if not brch[0]:
                hex, = options.values()
                return hex, "Bad Branch"

        if self.isJump(instr):
            jmp = self.checkJump(ogOp)
            if not jmp:
                hex, = options.values()
                return hex, "Bad Address"

        if len(options.keys()) == 1:
            # INSTR_LIB[instr] = options
            hex, = options.values()
            return hex, ""
        else:
            # INSTR_LIB[instr] = options
            # Analyze op to get format
            modeBytes = re.sub(r'\W+', '', mode.split(",")[0])
            format = "acc"
            if mode[0] == "#":
                format = "im"
            else:
                if len(modeBytes) == 2:
                    format = "zp"
                elif len(modeBytes) == 4:
                    format = "ab"
                if mode[0] == "(":
                    format = "in"

                if ",X" in mode:
                    format += "x"
                if ",Y" in mode:
                    format += "y"

            return options[format], ""

    def getOpHex(self, op):
        arithmatic = False
        logical = False
        isLabeled = False
        isVar = False
        if "+" in op:
            arithmatic = True
        if "-" in op:
            arithmatic = True
        if "/" in op:
            arithmatic = True
        if "*" in op:
            arithmatic = True
        if "!" in op:
            logical = True
        if "." in op:
            logical = True
        if "&" in op:
            logical = True

        list = re.findall(r'[+-/*!.&#$%]|\w+|\W+', op)
        next = ""
        for item in list:
            for lab in self.labels:
                if item in lab.keys():
                    isLabeled = True
            for var in self.vars:
                if item in var.keys():
                    isVar = True
            if item == "%":
                next = "bin"
            elif item == "$":
                next = "hex"
            elif item == "(" or item == ")":
                continue
            elif item == "#" or item == "," or item == "X" or item == "Y":
                continue

            else:
                if not isLabeled and not isVar:
                    if next == "bin":
                        toHex = hex(int(item, base=2))[2:].upper()
                        return self.formatHex(toHex)
                    if next == "hex":
                        toHex = hex(int(item, base=16))[2:].upper()
                        return self.formatHex(toHex)
                    else:
                        toHex = hex(item)[2:].upper()
                        return self.formatHex(toHex)
                if isLabeled:
                    # print(self.labels)
                    addr = ""

                    ret = self.symbols.get(item)
                    if ret:
                        addr = ret
                    if addr < self.pc:
                        # Branching to prev declared
                        diff = self.pc - addr + 2
                        toHex = hex(int("ff", base=16) - int(str(diff), base=16))[2:].upper()
                        return self.formatHex(toHex)
                        # print(hex(opCode))
                    else:
                        # Branching to declared later
                        diff = addr - self.pc - 3
                        toHex = hex(int(str(diff), base=16))[2:].upper()
                        return self.formatHex(toHex)
                if isVar:
                    val = ""
                    for v in self.vars:
                        ret = v.get(item)
                        if ret:
                            ret = re.sub(r'\W+', '', ret.split(",")[0])
                            ret = hex(int(str(ret), base=16))[2:].upper()
                            return self.formatHex(ret)
        # print(list)
        return ""

    def formatHex(self, opCode):
        ret = opCode
        if len(opCode) < 2:
            ret = opCode.rjust(2, "0")
        if len(opCode) > 2:
            opCode = opCode.rjust(4, "0")
        if len(opCode) == 4:
            ret = opCode[2] + opCode[3] + " " + opCode[0] + opCode[1]

        # print(ret)
        return ret

    def getCheckSum(self):
        currChk = int("00", base=16)

        for item in self.allHex:
            byteItem = int(item, base=16)
            currChk = currChk ^ byteItem

        return self.formatHex(hex(currChk)[2:].upper())

    def isJump(self, instr):
        jmpList = ["JSR", "JMP"]
        if instr in jmpList:
            return True
        else:
            return False

    def isBranch(self, instr):
        brList = ["BCC", "BCS", "BEQ", "BIT", "BMI", "BNE", "BPL", "BVC", "BVS"]
        if instr in brList:
            return True
        else:
            return False

    def checkBranch(self, mode):
        # Here it is a branch, not a jump, but we need to check if the branch is good

        test = re.findall(r'[^(A-Za-z0-9]+', mode)
        if len(test) > 0:
            print("BA")
            return False, "Bad Address Mode"
        if mode in self.varList:
            return False, "Bad Branch"
        return True, ""

    def checkJump(self, mode):
        test = re.findall(r'[^(A-Za-z0-9]+', mode)
        if len(test) > 0:
            return False
        else:
            return True

    # def getOpSize(self, l):
    #     content = self.breakUp(l)
    #
    #     instr = content["instr"]
    #     op = content["op"]
    #     if isPseudoInstr(instr):
    #         return 0
    #     if l[0] == "*":
    #         return 0
    #     # verify = Line(l, 0, 0, self.symbols)
    #     # if verify.isErrored:
    #     #     return 0
    #     if self.isBranch(instr):
    #         return 2
    #     if self.isJump(instr):
    #         return 3
    #
    #     if op in self.labelList:
    #         print(op)
    #         return 2
    #     return content["bitLen"]


# class Line:
#     def __init__(self, lineStr, lineNumber, lineAddress, symbols):
#         self.symbols = symbols
#         self.label = ""
#         self.instr = ""
#         self.op = ""
#         self.OGLine = lineStr
#         self.opCode = ""
#         self.addr = lineAddress
#         self.addressMode = ""
#         self.lineNumber = lineNumber
#         self.isErrored = False
#         self.errors = []
#         self.breakUp(lineStr)
#
#         self.instructionCode = self.getInstructionCode()
#         self.opCode = self.getOpCode()
#
#     def __str__(self):
#         if self.instructionCode == "":
#             formattedStr = "{h:>7}{c:<3} {o:<5}{n:>3}  ".format(h="", c=self.instructionCode,
#                                                                 o="",
#                                                                 n=self.lineNumber)
#         else:
#             formattedStr = "{h:>5}: {c:<3} {o:<5}{n:>3}  ".format(h=hex(self.addr)[2:], c=self.instructionCode,
#                                                                   o=self.opCode,
#                                                                   n=self.lineNumber)
#         return formattedStr + self.OGLine.strip("\n")
#
#     def breakUp(self, line):
#         if line[0] == "*":
#             return
#         self.label = line[0:8].strip()
#         self.instr = line[9:13].strip()
#         self.op = line[14:24].strip()
#         # opBits = re.sub(r'\W+', '', op.split(",")[0])
#         # bytLen = 1 + int((len(opBits) / 2))
#
#     def getInstructionCode(self):
#         mode = self.getAddressingMode()
#         if self.instr != "":
#             if not isPseudoInstr(self.instr):
#                 options = INSTR_LIB[self.instr]
#                 retCode = options.get(mode)
#                 if not retCode:
#                     # print("Bad address mode in line: " + str(self.lineNumber))
#                     self.errors.append("Bad address mode in line: " + str(self.lineNumber))
#                     self.isErrored = True
#                     return ""
#                 return retCode
#         return ""
#
#     def getAddressingMode(self):
#         addrRegex = [
#             ("acc", r'[A]{1}'),
#             ("im", r'#[A-Z|a-z|0-9]{2}'),
#             ("ab", r'[A-Z|a-z|0-9]{4}'),
#             ("abx", r'[A-Z|a-z|0-9]{4}' + r',X'),
#             ("aby", r'[A-Z|a-z|0-9]{4}' + r',Y'),
#             ("zp", r'[\+\-\/\*\!\.\&\#\$\%][A-Z|a-z|0-9]{2}'),
#             ("zpx", r'[\+\-\/\*\!\.\&\#\$\%][A-Z|a-z|0-9]{2}' + r',X'),
#             ("zpy", r'[\+\-\/\*\!\.\&\#\$\%][A-Z|a-z|0-9]{2}' + r',Y'),
#             ("inx", r'\([A-Z|a-z|0-9]{2},X\)'),
#             ("iny", r'\([A-Z|a-z|0-9]{2}\),Y'),
#             ("in", r'\([A-Z|a-z|0-9]{4}\)'),
#             ("rel", r'/[A-Z|a-z|0-9]{2}/gm')
#         ]
#         if self.instr != "":
#             if not isPseudoInstr(self.instr):
#                 options = INSTR_LIB[self.instr]
#                 # print(str(options) + " " + self.op)
#                 mode = ""
#                 if self.op == "":
#                     mode = "imp"
#                 for type, reg in addrRegex:
#                     result = re.match(reg, self.op)
#                     # print(self.instr + " " + type + ": " + reg)
#                     if result:
#                         mode = type
#                 if len(options) == 1:
#                     if "in" not in mode:
#                         mode, = options.keys()
#                 return mode
#         return ""
#
#     def getOpCode(self):
#         if self.op == "":
#             return ""
#
#         list = re.findall(r'[+-/*!.&#$%]|\w+|\W+', self.op)
#         opCode = ""
#         next = ""
#         for item in list:
#             if item == "*":
#                 opCode += self.addr
#             elif next == "hex":
#                 opCode += hex(int(item, base=16))[2:]
#             elif next == "bin":
#                 opCode += hex(int(item, base=2))[2:]
#             elif item == "$":
#                 next = "hex"
#             elif item == "%":
#                 next = "bin"
#             elif re.match(r'[0-9]+', item):
#                 opCode += item
#             tmp = self.symbols.get(item)
#             if tmp:
#                 opCode += tmp
#         print(opCode)
#         return opCode
