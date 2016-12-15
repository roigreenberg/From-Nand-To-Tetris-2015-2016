from io import *
from Parser import *

__author__ = 'roigreenberg'

class CodeWriter:

    fileName = ''
    functionName =''
    labelIndex = 0
    returnIndex = 0

    def __init__(self, fileName):
        self.w = open(fileName + ".asm", "w")



        self.w.write('@256\n')
        self.w.write('D=A\n')
        self.w.write('@SP\n')
        self.w.write('M=D\n')
        self.writeCall('Sys.init', 0)

    def setFileName(self, fileName):
        self.fileName = fileName

    def close(self):

        self.w.close()

    def pop(self):
        self.w.write('@SP\n')
        self.w.write('M=M-1\n')
        self.w.write('A=M\n')
        self.w.write('D=M\n')

    def pop2(self):
        self.pop()
        self.w.write('@R13\n')
        self.w.write('M=D\n')
        self.pop()

    def push(self):
        self.w.write('@SP\n')
        self.w.write('M=M+1\n')
        self.w.write('A=M-1\n')
        self.w.write('M=D\n')

    def compare(self, op):
        self.pop()
        self.w.write('@R14\n')
        self.w.write('M=D\n')
        self.pop()
        self.w.write('@R13\n')
        self.w.write('M=D\n')

        self.w.write('@R13\n')
        self.w.write('D=M\n')
        self.w.write('@Apos'+str(self.labelIndex)+'\n') #if A>=0
        self.w.write('D;JGE\n')
        self.w.write('@Aneg'+str(self.labelIndex)+'\n') #if A<0
        self.w.write('0;JMP\n')
        self.w.write('(Apos'+str(self.labelIndex)+')\n') #A >= 0

        self.w.write('@R14\n')
        self.w.write('D=M\n')
        self.w.write('@AposBpos'+str(self.labelIndex)+'\n') #if A>=0 && B>=0
        self.w.write('D;JGE\n')
        self.w.write('@AposBneg'+str(self.labelIndex)+'\n') #if A>=0 && B<0
        self.w.write('0;JMP\n')

        self.w.write('(AposBpos'+str(self.labelIndex)+')\n') # A >= 0, B >= 0
        self.w.write('@R13\n')
        self.w.write('D=M\n')
        self.w.write('@R14\n')
        self.w.write('D=D-M\n')
        self.w.write('@R15\n')
        self.w.write('M=D\n')
        self.w.write('@End'+str(self.labelIndex)+'\n') #if A<0 && B<0
        self.w.write('0;JMP\n')

        self.w.write('(AposBneg'+str(self.labelIndex)+')\n') # A >= 0, B < 0
        self.w.write('@R15\n')
        self.w.write('M=1\n')
        self.w.write('@End'+str(self.labelIndex)+'\n') # end
        self.w.write('0;JMP\n')

        self.w.write('(Aneg'+str(self.labelIndex)+')\n') #A < 0
        self.w.write('@R14\n')
        self.w.write('D=M\n')
        self.w.write('@AnegBpos'+str(self.labelIndex)+'\n') #if A<0 && B>=0
        self.w.write('D;JGE\n')
        self.w.write('@AnegBneg'+str(self.labelIndex)+'\n') #if A<0 && B<0
        self.w.write('0;JMP\n')

        self.w.write('(AnegBpos'+str(self.labelIndex)+')\n') # A < 0, B >= 0
        self.w.write('@R15\n')
        self.w.write('M=-1\n')
        self.w.write('@End'+str(self.labelIndex)+'\n') # end
        self.w.write('0;JMP\n')

        self.w.write('(AnegBneg'+str(self.labelIndex)+')\n') # A < 0, B < 0
        self.w.write('@R13\n')
        self.w.write('D=M\n')
        self.w.write('@R14\n')
        self.w.write('D=D-M\n')
        self.w.write('@R15\n')
        self.w.write('M=D\n')
        self.w.write('@End'+str(self.labelIndex)+'\n') # end
        self.w.write('0;JMP\n')

        self.w.write('(End'+str(self.labelIndex)+')\n') # end


        self.w.write('@R15\n')
        self.w.write('D=M\n')
        self.w.write('@True'+str(self.labelIndex)+'\n')
        self.w.write('D;'+ op +'\n')
        self.w.write('D=0\n')
        self.push()
        self.w.write('@Endcmp'+str(self.labelIndex)+'\n') # end
        self.w.write('0;JMP\n')
        self.w.write('(True'+str(self.labelIndex)+')\n')
        self.w.write('D=-1\n')
        self.push()
        self.w.write('(Endcmp'+str(self.labelIndex)+')\n') # end comparing

        self.labelIndex+=1

    def pushFrom(self, seg, i):
        self.w.write('@'+str(i)+'\n')
        if seg != '':
            self.w.write('D=A\n')
            self.w.write('@'+seg+'\n')
            self.w.write('A=D+M\n')
        self.w.write('D=M\n')

    def popTo(self, seg, i):
        if seg != '':
            self.w.write('@R13\n')
            self.w.write('M=D\n')

        self.w.write('@'+str(i)+'\n') #find and save memory address
        if seg != '':
            self.w.write('D=A\n')
            self.w.write('@'+seg+'\n')
            self.w.write('D=D+M\n')
            self.w.write('@R14\n')
            self.w.write('M=D\n')

            self.w.write('@R13\n') #set to  memory address
            self.w.write('D=M\n')
            self.w.write('@R14\n')
            self.w.write('A=M\n')
        self.w.write('M=D\n')

    def writeArithmetic(self, command):

        if command == 'add':
            self.pop2()
            self.w.write('@R13\n')
            self.w.write('D=D+M\n')
            self.push()
        elif command == 'sub':
            self.pop2()
            self.w.write('@R13\n')
            self.w.write('D=D-M\n')
            self.push()
        elif command == 'neg':
            self.pop()
            self.w.write('D=-D\n')
            self.push()
        elif command == 'eq':
            self.compare('JEQ')

        elif command == 'gt':
            self.compare('JGT')
        elif command == 'lt':
            self.compare('JLT')
        elif command == 'and':
            self.pop2()
            self.w.write('@R13\n')
            self.w.write('D=D&M\n')
            self.push()
        elif command == 'or':
            self.pop2()
            self.w.write('@R13\n')
            self.w.write('D=D|M\n')
            self.push()
        elif command == 'not':
            self.pop()
            self.w.write('D=!D\n')
            self.push()

    def writePushPop(self, command, segment, index):
        if command == Command.C_POP:
            self.pop()
            if segment == 'local':
                self.popTo('LCL', index)
            elif segment == 'argument':
                self.popTo('ARG', index)
            elif segment == 'this':
                self.popTo('THIS', index)
            elif segment == 'that':
                self.popTo('THAT', index)
            elif segment == 'static':
                self.popTo('',self.fileName+'.'+ str(index))
                #self.popTo(self.fileName+'.',int(index))
            elif segment == 'pointer':
                self.popTo('',3+int(index))
            elif segment == 'temp':
                self.popTo('',5+int(index))
        elif command == Command.C_PUSH:

            if segment == 'constant':
                self.w.write("@"+str(index)+"\n")
                self.w.write('D=A\n')
            elif segment == 'local':
                self.pushFrom('LCL', index)
            elif segment == 'argument':
                self.pushFrom('ARG', index)
            elif segment == 'this':
                self.pushFrom('THIS', index)
            elif segment == 'that':
                self.pushFrom('THAT', index)
            elif segment == 'static':
                self.pushFrom('',self.fileName+'.'+ str(index))
                #self.pushFrom(self.fileName+'.',int(index))
            elif segment == 'pointer':
                self.pushFrom('',3+int(index))
            elif segment == 'temp':
                self.pushFrom('',5+int(index))

            self.push()

    def writeLabel(self, label):
        self.w.write('(' + self.functionName +'$' + str(label) + ')\n')

    def writeGoto(self, label):
        self.w.write('@' + self.functionName +'$' + str(label) + '\n')
        self.w.write('0;JMP\n')

    def writeIf(self, label):
        self.pop()
        self.w.write('@' + self.functionName +'$' + str(label) + '\n')
        self.w.write('D;JNE\n')

    def writeCall(self, functionName, numArg):
        self.w.write('@Return$$' + str(self.returnIndex) + '\n')
        self.w.write('D=A\n')
        self.push()
        self.w.write('@LCL\n')
        self.w.write('D=M\n')
        self.push()
        self.w.write('@ARG\n')
        self.w.write('D=M\n')
        self.push()
        self.w.write('@THIS\n')
        self.w.write('D=M\n')
        self.push()
        self.w.write('@THAT\n')
        self.w.write('D=M\n')
        self.push()
        self.w.write('@SP\n')
        self.w.write('D=M\n')
        self.w.write('@LCL\n')
        self.w.write('M=D\n')
        self.w.write('@'+ str(int(numArg) + 5)+'\n')
        self.w.write('D=D-A\n')
        self.w.write('@ARG\n')
        self.w.write('M=D\n')
        self.w.write('@' + str(functionName) + '\n') # MISSING SOMETHING?
        self.w.write('0;JMP\n')
        self.w.write('(Return$$' + str(self.returnIndex) + ')\n')
        self.returnIndex+=1

    def writeReturn(self):

        self.pop()
        self.w.write('@R15\n')
        self.w.write('M=D\n')
        self.w.write('@LCL\n')  # set SP to LCL
        self.w.write('D=M\n')
        self.w.write('@SP\n')
        self.w.write('M=D\n')
        self.pop()                  # pop THAT
        self.w.write('@THAT\n')     # set THAT
        self.w.write('M=D\n')
        self.pop()                  # pop THIS
        self.w.write('@THIS\n')     # set THIS
        self.w.write('M=D\n')
        self.pop()                  # pop ARG
        self.w.write('@R13\n')      # save ARG in R13
        self.w.write('M=D\n')
        self.w.write('@ARG\n')      # save this ARG
        self.w.write('D=M\n')
        self.w.write('@R14\n')
        self.w.write('M=D\n')
        self.w.write('@R13\n')      # take ARG
        self.w.write('D=M\n')
        self.w.write('@ARG\n')      # set ARG
        self.w.write('M=D\n')

        self.pop()                  # pop LCL
        self.w.write('@LCL\n')      # set LCL
        self.w.write('M=D\n')
        self.pop()                  # pop ret
        self.w.write('@R13\n')      # save ret
        self.w.write('M=D\n')

        self.w.write('@R14\n')      # set SP to this ARG
        self.w.write('D=M\n')
        self.w.write('@SP\n')
        self.w.write('M=D\n')
        self.w.write('@R15\n')
        self.w.write('D=M\n')
        self.push()
        self.w.write('@R13\n')
        self.w.write('A=M\n')
        self.w.write('0;JMP\n')
        return

    def writeFunction(self, functionName, numLocals):
        self.functionName = functionName
        self.w.write('(' + str(functionName) + ')\n') # MISSING SOMETHING?
        for i in range(int(numLocals)):
            self.writePushPop(Command.C_PUSH, 'constant', 0)
#             self.writePushPop(Command.C_POP, 'local', i)
#
#
# w = CodeWriter('test')
# w.w.write('@START\n')
# w.w.write('0;JMP\n')
# w.writeFunction('z', '0')
# w.writePushPop(Command.C_PUSH, 'constant', 80)
# w.writePushPop(Command.C_PUSH, 'constant', 90)
# w.writePushPop(Command.C_POP, 'pointer', 0)
# w.writePushPop(Command.C_POP, 'pointer', 1)
# w.writePushPop(Command.C_PUSH, 'constant', 999)
#
# w.writeReturn()
# w.w.write('(START)\n')
# w.writePushPop(Command.C_PUSH, 'constant', 789)
# w.writePushPop(Command.C_PUSH, 'constant', 456)
# w.writePushPop(Command.C_PUSH, 'constant', 123)
# w.writeCall('z', '0')
# w.writePushPop(Command.C_PUSH, 'constant', 951)
#
#
#
#
# w.close()