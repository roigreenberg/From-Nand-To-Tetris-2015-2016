import re

__author__ = 'inbaravni'


#
#
# with open('/cs/stud/inbaravni/safe/NAND2tetris/ex10/List.jack', 'r') as self.f:
#         data = self.f.read().replace('\s', '')
#
# array = data.split('')
# print(array)

symbol_array = ['{', '}', '(', ')', '[', ']', '.', ',', ';',
                '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']


class Type:
    KEYWORD = 'keyword'
    SYMBOL = 'symbol'
    IDENTIFIER = 'identifier'
    INT_CONST = 'integerConstant'
    STRING_CONST = 'stringConstant'

keyword_array = ['class', 'constructor', 'function', 'method', 'field', 'static',
                 'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null',
                 'this', 'let', 'do', 'if', 'else', 'while', 'return']

# var_array = ['var', 'field', 'static']
# sub_array = ['constructor', 'function', 'method']
# type_array = ['int', 'char', 'boolean', 'void']
class Keyword:

    CLASS = 'class'
    CONSTRUCTOR = 'constructor'
    FUNCTION = 'function'
    METHOD = 'method'
    FIELD = 'field'
    STATIC = 'static'
    VAR = 'var'
    INT = 'int'
    CHAR = 'char'
    BOOLEAN = 'boolean'
    VOID = 'void'
    TRUE = 'true'
    FALSE = 'false'
    NULL = 'null'
    THIS = 'this'
    LET = 'let'
    DO = 'do'
    IF = 'if'
    ELSE = 'else'
    WHILE = 'while'
    RETURN = 'return'


class JackTokenizer:

    currentStringVal = ''

    # curDec = 'class'
    # varNames = []
    # subName = []
    # className = []

    def __init__(self, file_name):

        #
        with open(file_name, 'r') as self.f:
            text = self.f.read()
            # ftext = ''
            # in_c = 0
            # in_s = 0
            # for t in text:
            #     if in_c == 2:
            #     if t == '/':
            #         in_c = 1
            #     if t == '/' or t == '\*':
            #         in_c = 2;
            arr = re.split("(//)|(/\*)|(\*/)|(\")|(\n)", text)

            array = []

            for token in arr:
                if (token != '')  and (token is not None):
                    array.append(token)
            print(array)

            data = ''
            in_c = 0
            in_line_c = 0
            in_s = 0
            for token in array:
                if in_line_c == 1:
                    if token == '\n':
                        in_line_c = 0
                    continue
                if in_c == 1:
                    if token == '*/':
                        in_c = 0
                    continue
                if in_s == 1:
                    if token == '"':
                        in_s = 0
                    data+=token
                    continue
                if token == '//':
                    in_line_c = 1;
                    data+=" "
                    continue
                if token == '/*':
                    in_c = 1
                    data+=" "
                    continue
                if token == '"':
                    in_s = 1
                    data+=token
                    continue
                data+=token
            # print(data)



            # regex_space_comments = '((/\*.*?(\n.*?)*?\*/)|(//.*?\n)|[\n\t ]+)'
            # data = re.sub(regex_space_comments, ' ', self.f.read())
            # data = re.sub('([\n\t ]+)', ' ', data)
        symbols = r'(".*?")|([\[\];"(){}\.\,\-\+\*/&|<>~=])|[ \n\t]'

        self.arr = re.split(symbols, data)

        self.index = -1

        self.array = []

        for token in self.arr:
            if (token != '') and (token != ' ') and (token is not None):
                self.array.append(token)
        self.arraySize = len(self.array)
        print("********************************\n\n")
        print(self.array)
    def hasMoreTokens(self):

        if self.index + 1 <= self.arraySize - 1:
            return True
        return False

    def advance(self):
        self.index += 1
        # if self.array[self.index] == '"':
        #     self.createString()


        # if self.tokenType() == Type.SYMBOL:
        #     if (self.array[self.index] == ';'):
        #         self.curDec = ''
        #     elif (self.array[self.index] == ')'):
        #         self.curDec = ''
        # elif self.tokenType() == Type.KEYWORD:
        #     if (self.array[self.index] == 'class'):
        #         self.curDec = 'class'
        #     elif self.array[self.index] in var_array:
        #         self.curDec = 'var'
        #     elif self.array[self.index] in sub_array:
        #         self.curDec = 'sub'
        #     elif (self.curDec == 'var') & (self.array[self.index] in type_array):
        #         self.curDec = 'var_type'
        #     elif (self.curDec == 'sub') & (self.array[self.index] in type_array):
        #         self.curDec = 'sub_type'
        # elif self.tokenType() == Type.IDENTIFIER:
        #     if self.curDec == 'class':
        #         self.className.append(self.array[self.index])
        #         self.curDec = ''
        #     elif self.curDec == 'var':
        #         if self.array[self.index] not in self.className:

        #             self.className.append(self.array[self.index])
        #         self.curDec = 'var_type'
        #     elif self.curDec == 'sub':
        #         if self.array[self.index] not in self.className:
        #             print("      found class name")
        #             self.className.append(self.array[self.index])
        #         self.curDec = 'sub_type'
        #     elif self.curDec == 'var_type':
        #         print("      found var name")
        #         self.varNames.append(self.array[self.index])
        #         self.curDec = 'var'
        #     elif self.curDec == 'sub_type':
        #         print("      found sub name")
        #         self.subName.append(self.array[self.index])
        #         self.curDec = 'var'
        #
        # print("                                                        " + self.array[self.index])
        # print("                                        " + self.curDec)

    def tokenType(self):

        if self.array[self.index] in symbol_array:
            return Type.SYMBOL
        elif self.array[self.index] in keyword_array:
            return Type.KEYWORD
        elif self.representsInt(self.array[self.index]):
            return Type.INT_CONST
        elif self.array[self.index][0] == '"':
            return Type.STRING_CONST
        else:
            return Type.IDENTIFIER

    def keyWord(self):
        return self.array[self.index]

    def symbol(self):
        if self.array[self.index] == '<':
            return "lt"
        elif self.array[self.index] == '>':
            return "gt"
        # elif self.array[self.index] == '"':
        #     return "&quot;"
        # elif self.array[self.index] == "&":
        #     return "&amp;"
        else:
            return self.array[self.index]

    def identifier(self):
        return self.array[self.index]

    def intVal(self):
        return self.array[self.index]

    def stringVal(self):
        return self.array[self.index][1:-1]
        return self.currentStringVal

    def representsInt(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def createString(self):
        self.currentStringVal = ''
        self.index += 1
        if self.array[self.index] != '"':
            self.currentStringVal += (self.array[self.index])
            self.index += 1
        while self.array[self.index] != '"':
            self.currentStringVal += (" " + self.array[self.index])
            self.index += 1
