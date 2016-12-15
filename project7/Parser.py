__author__ = 'inbaravni'

import os


class Command:
    C_ARITHMETIC = 0
    C_PUSH = 1
    C_POP = 2
    C_LABEL = 3
    C_GOTO = 4
    C_IF = 5
    C_FUNCTION = 6
    C_RETURN = 7
    C_CALL = 8

class Parser:

   arithmetic = ['add','sub','neg','eq','gt','lt','and','or','not'];


   def __init__(self, input_file):

      self.inputFile = input_file;
      self.file = open(input_file, "r");
      #self.name = os.path.abspath(input_file).split('.')[0];
      self.name = (input_file).split('.')[0]
      self.curLine = '';
      self.nextLine = '';

   def hasMoreCommands(self):

       while True:
           self.nextLine = self.file.readline();
           # EOF case
           if not self.nextLine:
               return False;
           self.nextLine = self.nextLine.strip().split('/')[0]
           # the line is only whitespaces or a comment
           if not (self.nextLine) or (self.nextLine[0] == '/'):
               continue;
           else:
               return True;


   def advance(self):

       self.curLine = self.nextLine;


   def commandType(self):

       lines_words = self.curLine.split();

       if lines_words[0] in self.arithmetic:
           return Command.C_ARITHMETIC;

       elif (lines_words[0]) == 'push':
           return Command.C_PUSH;

       elif (lines_words[0]) == 'pop':
           return Command.C_POP;




   def arg1(self):

       lines_words = self.curLine.split();

       if self.commandType() == Command.C_ARITHMETIC:
           return lines_words[0];

       elif (self.commandType() == Command.C_PUSH) or (self.commandType() == Command.C_POP):
           return lines_words[1];




   def arg2(self):

       lines_words = self.curLine.split();

       if (self.commandType() == Command.C_PUSH) or (self.commandType() == Command.C_POP):
           return lines_words[2];



