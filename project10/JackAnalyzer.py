__author__ = 'inbaravni'

from JackTokenizer import *
from CompilationEngine import *
import sys
import os



def main(argv):
    # file given
    if (os.path.isfile(argv[0])):
        try:
            file = open(argv[0].split('.')[-2] + '.xml','w')   # Trying to create a new file
            CompilationEngine(argv[0], file)
            file.close()
        except:
            print('Can\'t create xml file')




    # directory given
    else:
        #path = os.path.abspath(argv[0])+'/'
        path = argv[0]
        if path[-1] != '/':
            path = path+'/'
        name = path + path.split('/')[-2]
        for each_file in os.listdir(argv[0]):
            if each_file.endswith(".jack"):
                try:
                    file = open((path+each_file).split('.')[-2] + '.xml','w')   # Trying to create a new file
                    CompilationEngine((path+each_file), file)
                    file.close();
                except:
                    print('Can\'t create an xml file')


        





if __name__ == "__main__":
    main(sys.argv[1:])

