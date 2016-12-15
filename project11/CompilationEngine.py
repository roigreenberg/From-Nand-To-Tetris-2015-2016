from JackTokenizer import *
from VMWriter import *
from SymbolTable import *
import inspect

__author__ = 'roigreenberg'


class Structure:
    CLASS = 'class'
    CLASSVARDEC = 'classVarDec'
    TYPE = 'type'
    SUBROUTINEDEC = 'subroutineDec'
    PARAM_LIST = 'parameterList'
    SUBROUTINEBODY = 'subroutineBody'
    VAR_DEC = 'varDec'
    STATEMENTS = 'statements'
    STATEMENT_LET = 'letStatement'
    STATEMENT_RETURN = 'returnStatement'
    STATEMENT_DO = 'doStatement'
    STATEMENT_IF = 'ifStatement'
    STATEMENT_WHILE = 'whileStatement'
    EXPRESSION_LIST = 'expressionList'
    EXPRESSION = 'expression'
    INTEGER_CONSTANT = 'integerConstant'
    STRING_CONSTANT = 'stringConstant'
    KEYWORD_CONSTANT = 'keywordConstant'
    TERM = 'term'
    
symbol = ['{', '}', '(', ')', '[', ']', '.', ', ', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']
subDec = ['constructor', 'function', 'method']
classDec = ['static', 'field']
types = ['int', 'char', 'boolean', 'void']
stat = ['let', 'if', 'while', 'do', 'return']
ops = ['+', '-', '*', '/', '&', '|', 'lt', 'gt', '=']
unaryOp = ['-', '~']
keywordConst = ['true', 'false', 'null', 'this']


class CompilationEngine:

    varNames = []
    subNames = []
    classNames = []
    whileI = 0
    ifI = 0

    def __init__(self, finput, foutput):

        self.w = VMWriter(foutput)  # open(output, "w")
        self.t = JackTokenizer(finput)
        self.s = SymbolTable()
        self.whileI = 0
        self.ifI = 0

        self.className = ''
        self.CompileClass()
        
    def CompileClass(self):
        # print (inspect.stack()[0][3])
        self.t.advance()  # class
        self.t.advance()  # class name
        self.className = self.t.identifier()
        if self.t.identifier() not in self.classNames:
            self.classNames.append(self.className)
        self.t.advance()  # '{'
        self.t.advance()

        while self.t.keyWord() in classDec:
            self.CompileClassVarDec()

        while self.t.keyWord() in subDec:
            self.CompileSubroutine()

        self.w.close()

    def CompileClassVarDec(self):
        # print(inspect.stack()[0][3])
        kind = self.t.keyWord()  # static|field

        self.t.advance()

        if self.t.tokenType() is Type.KEYWORD:
            typeV = self.t.keyWord()  # type
        else:
            typeV = self.t.identifier()  # type
            if type not in self.classNames:
                self.classNames.append(type)
        self.t.advance()
        name = self.t.identifier()  # varName
        self.varNames.append(name)
        self.s.define(name, typeV, kind)
        self.t.advance()
        while (self.t.tokenType() is Type.SYMBOL) & (self.t.symbol() == ','):
            self.t.advance()
            name = self.t.identifier()  # varName3
            # # print(name)
            self.varNames.append(name)
            # # print(name + " " + kind + " "+ typeV)
            self.s.define(name, typeV, kind)
            self.t.advance()

        self.t.advance()
        # # print("var added")
    def CompileSubroutine(self):
        # print(inspect.stack()[0][3])
        kind = self.t.keyWord()  # subDec
        self.t.advance()
        if self.t.tokenType() is not Type.KEYWORD:
            if self.t.identifier() not in self.classNames:
                self.classNames.append(self.t.identifier())
        self.t.advance()
        name = self.t.identifier()  # subName
        self.subNames.append(name)
        self.s.startSubroutine()
        if kind == 'method':
            self.s.define('instance', self.className, 'ARG')

        self.t.advance()
        self.t.advance()
        self.compileParameterList()
        self.t.advance()
        self.t.advance()
        while (self.t.tokenType() is Type.KEYWORD) & (self.t.keyWord() == 'var'):
            self.compileVarDec()

        fName = self.className + '.' + name

        numLocals = self.s.varCount('VAR')
        self.w.writeFunction(fName, numLocals)
        # # print("D")
        if kind == 'constructor':
            numFields = self.s.varCount('FIELD')
            self.w.writePush('CONST', numFields)
            self.w.writeCall('Memory.alloc', 1)
            self.w.writePop('POINTER', 0)
        elif kind == 'method':
            self.w.writePush('ARG', 0)
            self.w.writePop('POINTER', 0)

        self.compileStatements()
        self.t.advance()
    def compileParameterList(self):
        # print(inspect.stack()[0][3])
        if self.t.tokenType() != Type.SYMBOL:

            if self.t.tokenType() is Type.KEYWORD:
                varVype = self.t.keyWord()  # type
            else:
                varVype = self.t.identifier()  # type
                if self.t.identifier() not in self.classNames:
                    self.classNames.append(self.t.identifier())
            self.t.advance()
            name = self.t.identifier()  # varName
            self.varNames.append(self.t.identifier())
            self.s.define(name, varVype, 'ARG')
            self.t.advance()
            # # print("PP")
            while (self.t.tokenType() is Type.SYMBOL) & (self.t.symbol() == ','):
                self.t.advance()
                if self.t.tokenType() is Type.KEYWORD:
                    typeV = self.t.keyWord()  # type
                else:
                    typeV = self.t.identifier()  # type
                    if self.t.identifier() not in self.classNames:
                        self.classNames.append(self.t.identifier())
                self.t.advance()
                name = self.t.identifier()  # varName
                self.varNames.append(self.t.identifier())
                self.s.define(name, typeV, 'ARG')
                self.t.advance()
    def compileVarDec(self):
        # print(inspect.stack()[0][3])
        self.t.advance()
        if self.t.tokenType() is Type.KEYWORD:
            type = self.t.keyWord()  # type
        else:
            type = self.t.identifier()  # type
            if self.t.identifier() not in self.classNames:
                self.classNames.append(self.t.identifier())
        self.t.advance()
        name = self.t.identifier()  # varName
        self.s.define(name, type, 'VAR')
        self.varNames.append(self.t.identifier())
        self.t.advance()
        while (self.t.tokenType() is Type.SYMBOL) & (self.t.symbol() == ','):
            self.t.advance()
            name = self.t.identifier()  # varName
            self.s.define(name, type, 'VAR')
            self.varNames.append(self.t.identifier())
            self.t.advance()

        self.t.advance()
    def compileStatements(self):
        # print(inspect.stack()[0][3])
        while (self.t.tokenType() is Type.KEYWORD) & (self.t.keyWord() in stat):
            if self.t.keyWord() == 'let':
                self.compileLet()
            elif self.t.keyWord() == 'if':
                self.compileIf()
            elif self.t.keyWord() == 'while':
                self.compileWhile()
            elif self.t.keyWord() == 'do':
                self.compileDo()
            elif self.t.keyWord() == 'return':
                self.compileReturn()

    def compileDo(self):
        # print(inspect.stack()[0][3])
        self.t.advance()

        self.compileSubCall()
        self.w.writePop('TEMP', 0)
        self.t.advance()

    def compileLet(self):
        # print(inspect.stack()[0][3])
        self.t.advance()
        name = self.t.keyWord()  # varName
        kind = self.s.kindOf(name)
        index = self.s.indexOf(name)
        self.t.advance()

        if self.t.symbol() == '[':
            self.t.advance()
            self.compileExpression()

            self.w.writePush(kind, index)
            self.w.writeArithmetic('add')

            self.t.advance()
            self.t.advance()

            self.compileExpression()
            self.w.writePop('TEMP', 0)

            self.t.advance()

            self.w.writePop('POINTER', 1)
            self.w.writePush('TEMP', 0)

            self.w.writePop('THAT', 0)

            return

        self.t.advance()
        self.compileExpression()
        self.w.writePop(kind, index)

        self.t.advance()

    def compileWhile(self):
        # print(inspect.stack()[0][3])
        whileIndex = self.whileI
        self.whileI += 1

        self.w.writeLabel('WHILE_START.' + str(whileIndex))

        self.t.advance()

        self.t.advance()
        self.compileExpression()

        self.w.writeArithmetic('not')
        self.w.writeIf('WHILE_END.' + str(whileIndex))
        self.t.advance()

        self.t.advance()
        self.compileStatements()

        self.w.writeGoto('WHILE_START.' + str(whileIndex))
        self.w.writeLabel('WHILE_END.' + str(whileIndex))

        self.t.advance()

        

    def compileReturn(self):
        # print(inspect.stack()[0][3])
        self.t.advance()

        if not ((self.t.tokenType() is Type.SYMBOL) and (self.t.symbol() == ';')):
            self.compileExpression()
        else:
            self.w.writePush('CONST', 0)

        self.t.advance()

        self.w.writeReturn()

    def compileIf(self):
        # print(inspect.stack()[0][3])
        
        ifIndex = self.ifI
        self.ifI += 1
        self.t.advance()

        self.t.advance()
        self.compileExpression()
        # print("in num: "+ str(ifIndex))
        self.w.writeIf('IF_TRUE.' + str(ifIndex))
        self.w.writeGoto('IF_FALSE.' + str(ifIndex))
        self.w.writeLabel('IF_TRUE.' + str(ifIndex))

        self.t.advance()

        self.t.advance()
        self.compileStatements()

        self.w.writeGoto('IF_END.' + str(ifIndex))
        self.w.writeLabel('IF_FALSE.' + str(ifIndex))

        self.t.advance()

        if (self.t.tokenType() is Type.KEYWORD) & (self.t.keyWord() == 'else'):
            self.t.advance()
            self.t.advance()
            self.compileStatements()

            self.t.advance()

        self.w.writeLabel('IF_END.' + str(ifIndex))

        self.ifI += 1

    def compileExpression(self):
        # print(inspect.stack()[0][3])
        self.compileTerm()

        while (self.t.tokenType() is Type.SYMBOL) & (self.t.symbol() in ops):

            opr = self.t.symbol()  # 'op'

            self.t.advance()
            self.compileTerm()

            if opr == '*':
                self.w.writeCall('Math.multiply', 2)
            elif opr == '/':
                self.w.writeCall('Math.divide', 2)
            else:
                self.w.writeArithmetic(opr)

    def compileTerm(self):
        # print(inspect.stack()[0][3])
        # # print ("Term: " + self.t.tokenType() + " PP " + self.t.symbol())
        if self.t.tokenType() == Type.STRING_CONST:

            string = self.t.stringVal()  # string
            self.w.writePush('CONST', len(string))
            self.w.writeCall('String.new', 1)

            for st in string:
                self.w.writePush('CONST', ord(st))
                self.w.writeCall('String.appendChar', 2)

            self.t.advance()

        elif self.t.tokenType() == Type.INT_CONST:

            intV = self.t.intVal()  # int
            self.w.writePush('CONST', intV)
            self.t.advance()

        elif (self.t.tokenType() is Type.KEYWORD) & (self.t.keyWord() in keywordConst):

            keyword = self.t.keyWord()  # keyboard const
            if keyword == 'this':
                self.w.writePush('POINTER', 0)
            else:
                self.w.writePush('CONST', 0)
                if keyword == 'true':
                    self.w.writeArithmetic('not')

            self.t.advance()

        elif (self.t.tokenType() is Type.IDENTIFIER) & (self.t.identifier() in self.varNames):

            var = self.t.identifier()  # var name
            kind = self.s.kindOf(var)
            index = self.s.indexOf(var)
            typeVar = self.s.typeOf(var)
            argNum = 0

            self.t.advance()
            if (self.t.tokenType() is Type.SYMBOL) & (self.t.symbol() == '['):

                self.t.advance()
                self.compileExpression()

                self.w.writePush(kind, index)
                self.w.writeArithmetic('add')
                self.w.writePop('POINTER', 1)
                self.w.writePush('THAT', 0)

                self.t.advance()
            elif self.t.symbol() == '.':
                self.t.advance()

                subName = self.t.identifier()  # subName

                self.w.writePush(kind,index)  #TODO

                funName = typeVar + '.' + subName
                argNum += 1

                self.t.advance()

                self.t.advance()
                argNum += self.compileExpressionList()
                self.w.writeCall(funName, argNum)
                self.t.advance()
            else:
                self.w.writePush(kind,index)

        elif (self.t.tokenType() is Type.SYMBOL) & (self.t.symbol() == '('):

            self.t.advance()
            self.compileExpression()
            self.t.advance()
        elif (self.t.tokenType() is Type.SYMBOL) & (self.t.symbol() in unaryOp):

            uOp = self.t.symbol()  # unary op
            self.t.advance()
            self.compileTerm()
            self.w.writeArithmetic("u"+uOp)
        else:  # (self.t.tokenType() is Type.IDENTIFIER) & (self.t.identifier() in self.subName):

            self.compileSubCall()

    def compileExpressionList(self):
        # print(inspect.stack()[0][3])
        countArg = 0

        if not ((self.t.tokenType() is Type.SYMBOL) & (self.t.symbol() == ')')):
            self.compileExpression()
            countArg += 1

            while ((self.t.tokenType() is Type.SYMBOL) & (self.t.symbol() == ',')):
                self.t.advance()
                self.compileExpression()
                countArg += 1

        return countArg
    
    def compileSubCall(self):
        # print(inspect.stack()[0][3])
        idnt = self.t.identifier()  # sub/class/
        kind = self.s.kindOf(idnt)
        index = self.s.indexOf(idnt)
        typeVar = self.s.typeOf(idnt)
        argNum = 0
        self.t.advance()
        # # print(typeVar)
        # # print("S " + self.t.symbol())
        if self.t.symbol() == '.':
            self.t.advance()

            subName = self.t.identifier()  # subName

            # print("F  " + idnt + " "+ subName + " " + str(typeVar))
            if typeVar == None:
                funName = idnt + '.' + subName
            else:
                self.w.writePush(kind, index)
                funName = typeVar + '.' + subName
                argNum += 1

            self.t.advance()
            #
            # self.t.advance()
            # argNum += self.compileExpressionList()
            # self.w.writeCall(funName, argNum)
            # self.t.advance()
        else:
            # # print("L")
            funName = self.className + '.' + idnt
            argNum += 1
            self.w.writePush('POINTER', 0)

        # self.t.advance()
        self.t.advance()

        # print("O " + funName + "   " + self.t.identifier())
        argNum += self.compileExpressionList()
        # # print("P " + funName + " " + str(argNum))
        self.w.writeCall(funName, argNum)

        self.t.advance()
