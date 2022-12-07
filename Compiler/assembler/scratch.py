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
    if instr == "JMP" or instr == "JSR":
        return True
    if instr[0] != "B":
        return False
    if instr == "BIT" or instr == "BRK":
        return False
    return True


def isLoadStore(instr):
    if instr[0] == "L" or instr[0] == "S":
        if "LD" in instr or "ST" in instr:
            return True
        else:
            return False
    else:
        return False


def scratch(lineList):
    lines = []
    labels = {}
    pc = int("0", base=16)

    for line in lineList:
        label = line[0:8].strip()
        instr = line[9:13].strip()
        op = line[14:24].strip()
        if instr == "EQU":
            labels[label] = op
            print(labels)
            continue
        if len(label) > 0:
            labels[label] = pc

    for line in lineList:

        if line[0] == "*":
            continue
        label = line[0:8].strip()
        instr = line[9:13].strip()
        op = line[14:24].strip()
        opBits = re.sub(r'\W+', '', op.split(",")[0])
        bytLen = 1 + int((len(opBits) / 2))

        if instr == "ORG":
            pc = int(opBits, base=16)
            continue
        if instr == "CHK":
            continue
        if instr == "END":
            break
        if instr == "EQU":
            continue
        opCode = ""
        # print(hex(pc))

        if isLoadStore(instr):
            if op[0] != "#" and op[0] != "$":
                op = labels[op]
                opCode = op

        opBits = re.sub(r'\W+', '', op.split(",")[0])
        bytLen = 1 + int((len(opBits) / 2))
        lines.append({"label": label, "instr": instr, "op": op, "bitlen": bytLen})
        pc += int(str(bytLen), base=16)
        format = "imp"
        if len(op) > 0:
            if op[0] == "#":
                format = "im"
            elif op[0] == "(":
                format = "in"
            elif bytLen == 2:
                format = "zp"
            elif bytLen == 3:
                format = "ab"
            if ",X" in op:
                format += "x"
            if ",Y" in op:
                format += "y"
            if isBranch(instr):
                format = "rel"

        instCode = INSTR_LIB[instr][format]

        if bytLen == 2:
            opCode = opBits
        if bytLen == 3:
            opCode = opBits[2:3] + opBits[0:1]
        if isBranch(instr):
            branchAddr = labels[op]
            if branchAddr < pc:
                # Branching to prev declared
                diff = pc - branchAddr - 2
                opCode = hex(int("ff", base=16) - int(str(diff), base=16))[2:].upper()
                # print(hex(opCode))
            else:
                # Branching to declared later
                diff = branchAddr - pc
                opCode = hex(int(str(diff), base=16))[2:].upper()

        # print(type(opCode))
        if opCode != "":
            assembly = instCode + opCode
        else:
            assembly = instCode
        assembly = ' '.join(assembly[i:i + 2] for i in range(0, len(assembly), 2))
        # print('L: {l:<6}I: {i:<4}O: {o:<10}F: {b:<10}C: {c:<10}'.format(l=label, i=instr, o=opBits, b=format, c=code))
        print(assembly)
    # print(lines)
    # print(labels)
