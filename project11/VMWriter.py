__author__ = 'inbaravni'

from SymbolTable import *
op = ['+','-','&','>','<','|','=']
uop = ['u~','u-']
ARITHMETIC = {
    '+': 'add',
    '-': 'sub',
    '&': 'and',
    '>': 'gt',
    '<': 'lt',
    '|': 'or',
    '=': 'eq',
  }

UOP = {
    'u~': 'not',
    'u-': 'neg'
}

seg = ['THAT','THIS','TEMP','STATIC','FIELD','field','VAR','var','ARG','CONST','POINTER']
KIND_TO_SEG = {
    'THAT': 'that',
    'THIS': 'this',
    'TEMP': 'temp',
    'STATIC': 'static',
    'FIELD': 'this',
    'field': 'this',
    'VAR': 'local',
    'var': 'local',
    'ARG': 'argument',
    'POINTER': 'pointer',
    'CONST': 'constant'
  }

class VMWriter:

    outputFile = ''

    def __init__(self, outputFileName):
        # print(outputFileName)
        # try:
        #     self.outputFile = open(outputFileName+'.vm', 'w+')
        # except:
        #     print("Can\'t create a .vm file")
        self.outputFile = outputFileName

    def writePush(self, segment, index):
        # print("E " + str(segment) + " "+ str(index))
        if segment in seg:
            self.outputFile.write("push " + KIND_TO_SEG[segment] + " " + str(index) + "\n")
        else:
            self.outputFile.write("push " + segment + " " + str(index) + "\n")
        # print("D")
    def writePop(self, segment, index):
        if segment in seg:
            self.outputFile.write("pop " + KIND_TO_SEG[segment] + " " + str(index) + "\n")
        else:
            self.outputFile.write("pop " + segment + " " + str(index) + "\n")

    def writeArithmetic(self, command):
        if command in op:
            self.outputFile.write(ARITHMETIC[command] + "\n")
        elif command in uop:
            self.outputFile.write(UOP[command] + "\n")
        else:
            self.outputFile.write(command + "\n")

    def writeLabel(self, label):
        self.outputFile.write("label " + label + "\n")

    def writeGoto(self, label):
        self.outputFile.write("goto " + label + "\n")

    def writeIf(self, label):
        self.outputFile.write("if-goto " + label + "\n")

    def writeCall(self, name, nArgs):
        self.outputFile.write("call " + name + " " + str(nArgs) + "\n")
        # print("call " + name + " " + str(nArgs))

    def writeFunction(self, name, nArgs):
        self.outputFile.write("function " + name + " " + str(nArgs) + "\n")

    def writeReturn(self):
        self.outputFile.write("return" + "\n")

    def close(self):
        self.outputFile.close()








