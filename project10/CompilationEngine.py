from JackTokenizer import *

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
op = ['+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '=']
unaryOp = ['-', '~']
keywordConst = ['true', 'false', 'null', 'this']


class CompilationEngine:

    varName = []
    subName = []
    className = []

    def __init__(self, finput, foutput):

        # self.fin = open(input, "r")
        self.fout = foutput  # open(output, "w")
        self.t = JackTokenizer(finput)
        self.CompileClass()

    def writeO(self, t):
        self.fout.write(" <" + t + "> \n")

    def writeC(self, t):

        self.fout.write(" </" + t + "> \n")

    def writeOC(self, t, c):

        self.fout.write(" <" + t + "> " + c + " </" + t + "> \n")

    def CompileClass(self):
        self.writeO(Structure.CLASS)
        # self.t = ; #get type
        self.writeOC(self.t.tokenType(), self.t.keyWord()) # class
        self.t.advance()
        self.writeOC(self.t.tokenType(), self.t.identifier()) # class name
        if self.t.identifier() not in self.className:
            self.className.append(self.t.identifier())
        self.t.advance()
        self.writeOC(self.t.tokenType(), self.t.symbol()) # '{'
        self.t.advance()

        while self.t.keyWord() in classDec:
            self.CompileClassVarDec()

        while self.t.keyWord() in subDec:
            self.CompileSubroutine()

        self.writeOC(self.t.tokenType(), self.t.symbol()) # '}'

        self.writeC(Structure.CLASS)








    def CompileClassVarDec(self):
        self.writeO(Structure.CLASSVARDEC)
        self.writeOC(self.t.tokenType(), self.t.keyWord())  # static|field
        self.t.advance()

        if self.t.tokenType() is Type.KEYWORD:
            self.writeOC(self.t.tokenType(), self.t.keyWord())  # type
        else:
            self.writeOC(self.t.tokenType(), self.t.identifier())  # type
            if self.t.identifier() not in self.className:
                self.className.append(self.t.identifier())
        self.t.advance()
        self.writeOC(self.t.tokenType(), self.t.identifier())  # varName
        self.varName.append(self.t.identifier())
        self.t.advance()
        while (self.t.tokenType() is Type.SYMBOL) & (self.t.symbol() == ','):
            self.writeOC(self.t.tokenType(), self.t.symbol())  # ','
            self.t.advance()
            self.writeOC(self.t.tokenType(), self.t.identifier())  # varName3
            self.varName.append(self.t.identifier())
            self.t.advance()

        self.writeOC(self.t.tokenType(), self.t.symbol())  # ';'
        self.t.advance()
        self.writeC(Structure.CLASSVARDEC)

    def CompileSubroutine(self):
        self.writeO(Structure.SUBROUTINEDEC)

        self.writeOC(self.t.tokenType(), self.t.keyWord())  # subDec
        self.t.advance()
        if self.t.tokenType() is Type.KEYWORD:
            self.writeOC(self.t.tokenType(), self.t.keyWord())  # type
        else:
            self.writeOC(self.t.tokenType(), self.t.identifier())  # type
            if self.t.identifier() not in self.className:
                self.className.append(self.t.identifier())
        self.t.advance()
        self.writeOC(self.t.tokenType(), self.t.identifier())  # subName
        self.subName.append(self.t.identifier())
        self.t.advance()
        self.writeOC(self.t.tokenType(), self.t.symbol())  # '('
        self.t.advance()
        self.compileParameterList()
        self.writeOC(self.t.tokenType(), self.t.symbol())  # ')'
        self.t.advance()
        self.writeO(Structure.SUBROUTINEBODY)
        self.writeOC(self.t.tokenType(), self.t.symbol())  # '{'
        self.t.advance()
        while (self.t.tokenType() is Type.KEYWORD) & (self.t.keyWord() == 'var'):
            self.compileVarDec()
        self.compileStatements()
        self.writeOC(self.t.tokenType(), self.t.symbol())  # '}'
        self.writeC(Structure.SUBROUTINEBODY)

        self.t.advance()
        self.writeC(Structure.SUBROUTINEDEC)

    def compileParameterList(self):
        self.writeO(Structure.PARAM_LIST)

        if self.t.tokenType() != Type.SYMBOL:
            if self.t.tokenType() is Type.KEYWORD:
                self.writeOC(self.t.tokenType(), self.t.keyWord())  # type
            else:
                self.writeOC(self.t.tokenType(), self.t.identifier())  # type
                if self.t.identifier() not in self.className:
                    self.className.append(self.t.identifier())
            self.t.advance()
            self.writeOC(self.t.tokenType(), self.t.identifier())  # varName
            self.varName.append(self.t.identifier())
            self.t.advance()
            while (self.t.tokenType() is Type.SYMBOL) & (self.t.symbol() == ','):
                self.writeOC(self.t.tokenType(), self.t.symbol())  # ','
                self.t.advance()
                if self.t.tokenType() is Type.KEYWORD:
                    self.writeOC(self.t.tokenType(), self.t.keyWord())  # type
                else:
                    self.writeOC(self.t.tokenType(), self.t.identifier())  # type
                    if self.t.identifier() not in self.className:
                        self.className.append(self.t.identifier())
                self.t.advance()
                self.writeOC(self.t.tokenType(), self.t.identifier())  # varName
                self.varName.append(self.t.identifier())
                self.t.advance()
        self.writeC(Structure.PARAM_LIST)

    def compileVarDec(self):
        self.writeO(Structure.VAR_DEC)

        self.writeOC(self.t.tokenType(), self.t.keyWord())  # var
        self.t.advance()
        if self.t.tokenType() is Type.KEYWORD:
            self.writeOC(self.t.tokenType(), self.t.keyWord())  # type
        else:
            self.writeOC(self.t.tokenType(), self.t.identifier())  # type
            if self.t.identifier() not in self.className:
                self.className.append(self.t.identifier())
        self.t.advance()
        self.writeOC(self.t.tokenType(), self.t.identifier())  # varName
        self.varName.append(self.t.identifier())
        self.t.advance()
        while (self.t.tokenType() is Type.SYMBOL) & (self.t.symbol() == ','):
            self.writeOC(self.t.tokenType(), self.t.symbol())  # ','
            self.t.advance()
            self.writeOC(self.t.tokenType(), self.t.identifier())  # varName
            self.varName.append(self.t.identifier())
            self.t.advance()

        self.writeOC(self.t.tokenType(), self.t.symbol())  # ';'
        self.t.advance()
        self.writeC(Structure.VAR_DEC)

    def compileStatements(self):
        self.writeO(Structure.STATEMENTS)
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

        self.writeC(Structure.STATEMENTS)

    def compileDo(self):
        self.writeO(Structure.STATEMENT_DO)

        self.writeOC(self.t.tokenType(), self.t.keyWord())  # stat
        self.t.advance()

        self.compileSubCall()

        self.writeOC(self.t.tokenType(), self.t.symbol())  # ';'
        self.t.advance()

        self.writeC(Structure.STATEMENT_DO)

    def compileLet(self):
        self.writeO(Structure.STATEMENT_LET)

        self.writeOC(self.t.tokenType(), self.t.keyWord())  # stat
        self.t.advance()
        self.writeOC(self.t.tokenType(), self.t.keyWord())  # varName
        self.t.advance()

        if self.t.symbol() == '[':
            self.writeOC(self.t.tokenType(), self.t.symbol())  # '['
            self.t.advance()
            self.compileExpression()
            self.writeOC(self.t.tokenType(), self.t.symbol())  # ']'
            self.t.advance()

        self.writeOC(self.t.tokenType(), self.t.symbol())  # '='
        self.t.advance()
        self.compileExpression()
        self.writeOC(self.t.tokenType(), self.t.symbol())  # ';'
        self.t.advance()

        self.writeC(Structure.STATEMENT_LET)

    def compileWhile(self):
        self.writeO(Structure.STATEMENT_WHILE)

        self.writeOC(self.t.tokenType(), self.t.keyWord())  # stat
        self.t.advance()

        self.writeOC(self.t.tokenType(), self.t.symbol())  # '('
        self.t.advance()
        self.compileExpression()
        self.writeOC(self.t.tokenType(), self.t.symbol())  # ')'
        self.t.advance()

        self.writeOC(self.t.tokenType(), self.t.symbol())  # '{'
        self.t.advance()
        self.compileStatements()
        self.writeOC(self.t.tokenType(), self.t.symbol())  # '}'
        self.t.advance()

        self.writeC(Structure.STATEMENT_WHILE)

    def compileReturn(self):
        self.writeO(Structure.STATEMENT_RETURN)

        self.writeOC(self.t.tokenType(), self.t.keyWord())  # stat
        self.t.advance()

        if not ((self.t.tokenType() is Type.SYMBOL) and (self.t.symbol() == ';')):
            self.compileExpression()

        self.writeOC(self.t.tokenType(), self.t.symbol())  # ';'
        self.t.advance()

        self.writeC(Structure.STATEMENT_RETURN)

    def compileIf(self):
        self.writeO(Structure.STATEMENT_IF)

        self.writeOC(self.t.tokenType(), self.t.keyWord())  # stat
        self.t.advance()

        self.writeOC(self.t.tokenType(), self.t.symbol())  # '('
        self.t.advance()
        self.compileExpression()
        self.writeOC(self.t.tokenType(), self.t.symbol())  # ')'
        self.t.advance()

        self.writeOC(self.t.tokenType(), self.t.symbol())  # '{'
        self.t.advance()
        self.compileStatements()
        self.writeOC(self.t.tokenType(), self.t.symbol())  # '}'
        self.t.advance()

        if (self.t.tokenType() is Type.KEYWORD) & (self.t.keyWord() == 'else'):
            self.writeOC(self.t.tokenType(), self.t.keyWord())  # else
            self.t.advance()
            self.writeOC(self.t.tokenType(), self.t.symbol())  # '{'
            self.t.advance()
            self.compileStatements()
            self.writeOC(self.t.tokenType(), self.t.symbol())  # '}'
            self.t.advance()

        self.writeC(Structure.STATEMENT_IF)

    def compileExpression(self):
        self.writeO(Structure.EXPRESSION)
        self.compileTerm()

        while (self.t.tokenType() is Type.SYMBOL) & (self.t.symbol() in op):

            self.writeOC(self.t.tokenType(), self.t.symbol())  # 'op'
            self.t.advance()
            self.compileTerm()

        self.writeC(Structure.EXPRESSION)

    def compileTerm(self):
        self.writeO(Structure.TERM)
        if self.t.tokenType() == Type.STRING_CONST:

            self.writeOC(self.t.tokenType(), self.t.stringVal())  # string
            self.t.advance()
        elif self.t.tokenType() == Type.INT_CONST:

            self.writeOC(self.t.tokenType(), self.t.intVal())  # int
            self.t.advance()
        elif (self.t.tokenType() is Type.KEYWORD) & (self.t.keyWord() in keywordConst):

            self.writeOC(self.t.tokenType(), self.t.keyWord())  # keyboard const
            self.t.advance()
        elif (self.t.tokenType() is Type.IDENTIFIER) & (self.t.identifier() in self.varName):

            self.writeOC(self.t.tokenType(), self.t.identifier())  # var name
            self.t.advance()
            if (self.t.tokenType() is Type.SYMBOL) & (self.t.symbol() == '['):

                self.writeOC(self.t.tokenType(), self.t.symbol())  # '['
                self.t.advance()
                self.compileExpression()
                self.writeOC(self.t.tokenType(), self.t.symbol())  # ']'
                self.t.advance()
            elif self.t.symbol() == '.':
                self.writeOC(self.t.tokenType(), self.t.symbol())  # '.'
                self.t.advance()
                self.writeOC(self.t.tokenType(), self.t.identifier())  # subName
                self.t.advance()

                self.writeOC(self.t.tokenType(), self.t.symbol())  # '('
                self.t.advance()
                self.compileExpressionList()
                self.writeOC(self.t.tokenType(), self.t.symbol())  # ')'
                self.t.advance()

        elif (self.t.tokenType() is Type.SYMBOL) & (self.t.symbol() == '('):

            self.writeOC(self.t.tokenType(), self.t.symbol())  # '('
            self.t.advance()
            self.compileExpression()
            self.writeOC(self.t.tokenType(), self.t.symbol())  # ')'
            self.t.advance()
        elif (self.t.tokenType() is Type.SYMBOL) & (self.t.symbol() in unaryOp):

            self.writeOC(self.t.tokenType(), self.t.symbol())  # unary op
            self.t.advance()
            self.compileTerm()
        else:# (self.t.tokenType() is Type.IDENTIFIER) & (self.t.identifier() in self.subName):

            self.compileSubCall()

        self.writeC(Structure.TERM)

    def compileExpressionList(self):
        self.writeO(Structure.EXPRESSION_LIST)

        if not ((self.t.tokenType() is Type.SYMBOL) & (self.t.symbol() == ')')):
            self.compileExpression()

            while ((self.t.tokenType() is Type.SYMBOL) & (self.t.symbol() == ',')):
                self.writeOC(self.t.tokenType(), self.t.symbol())  # ','
                self.t.advance()
                self.compileExpression()

        self.writeC(Structure.EXPRESSION_LIST)

    def compileSubCall(self):
        self.writeOC(self.t.tokenType(), self.t.identifier())  # sub/class/varName
        self.t.advance()

        if self.t.symbol() == '.':
            self.writeOC(self.t.tokenType(), self.t.symbol())  # '.'
            self.t.advance()
            self.writeOC(self.t.tokenType(), self.t.identifier())  # subName
            self.t.advance()

        self.writeOC(self.t.tokenType(), self.t.symbol())  # '('
        self.t.advance()
        self.compileExpressionList()
        self.writeOC(self.t.tokenType(), self.t.symbol())  # ')'
        self.t.advance()
