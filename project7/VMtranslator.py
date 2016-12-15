__author__ = 'inbaravni'
from Parser import *
from codeWriter import *
import sys
import os



def main(argv):
    # file given
    if (os.path.isfile(argv[0])):
        parser = Parser(argv[0]);
        w = CodeWriter(parser.name);
        w.setFileName(parser.name.split('/')[-1])


        while (parser.hasMoreCommands()):
            parser.advance();
            # arithmetic
            if parser.commandType() is Command.C_ARITHMETIC:
                w.writeArithmetic(parser.arg1());
            # pop
            if parser.commandType() == Command.C_POP:
                w.writePushPop(Command.C_POP, parser.arg1(), parser.arg2());
            # push
            if parser.commandType() == Command.C_PUSH:
                w.writePushPop(Command.C_PUSH, parser.arg1(), parser.arg2());

        w.close();

    # directory given
    else:
        #path = os.path.abspath(argv[0])+'/'
        path = argv[0]
        if path[-1] != '/':
            path = path+'/'
        name = path + path.split('/')[-2];
        w = CodeWriter(name);

        for each_file in  os.listdir(argv[0]):
            if each_file.endswith(".vm"):

                parser = Parser(path+each_file);
                w.setFileName(parser.name.split('/')[-1])

                while (parser.hasMoreCommands()):
                    parser.advance();
                    # arithmetic
                    if parser.commandType() == Command.C_ARITHMETIC:
                        w.writeArithmetic(parser.arg1());
                    # pop
                    if parser.commandType() == Command.C_POP:
                        w.writePushPop(Command.C_POP, parser.arg1(), parser.arg2());

                    # push
                    if parser.commandType() == Command.C_PUSH:
                        w.writePushPop(Command.C_PUSH, parser.arg1(), parser.arg2());

        w.close();





if __name__ == "__main__":
    main(sys.argv[1:])






