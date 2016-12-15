__author__ = 'inbaravni'



class SymbolTable:

    classTable = []
    routinTable = []
    count_static = 0
    count_field = 0
    count_arg = 0
    count_var = 0

    def __init__(self):
        self.classTable = {};
        self.count_static = 0;
        self.count_field = 0;


    def startSubroutine(self):
        self.routinTable = {};
        self.count_arg = 0;
        self.count_var = 0;


    def define(self, name, type, kind):
        #class scope
        # print("add to table: name: "+name +" type:" + type + " kind: " + kind)
        if (kind == "static"):
            self.classTable[name] = [type, kind, self.count_static]
            # print("add to class table: type:" + type + " kind: " + kind + " count: " + str(self.count_static))
            self.count_static+=1

        elif (kind == "field"):
            self.classTable[name] = [type, kind, self.count_field]
            # print("add to class table: type:" + type + " kind: " + kind + " count: " + str(self.count_field))
            self.count_field+=1
        #subroutine scope
        elif (kind == "ARG"):
            self.routinTable[name] = [type, kind, self.count_arg]
            # print("add to sub table: type:" + type + " kind: " + kind + " count: " + str(self.count_arg))
            self.count_arg+=1
        elif (kind == "VAR"):
            self.routinTable[name] = [type, kind, self.count_var]
            # print("add to class table: type:" + type + " kind: " + kind + " count: " + str(self.count_var))
            self.count_var+=1


    def varCount(self, kind):
        # print("V")
        if (kind == "STATIC"):
            return self.count_static
        elif (kind == "FIELD"):
            return self.count_field
        elif (kind == "ARG"):
            return self.count_arg
        elif (kind == "VAR"):
            return self.count_var


    def kindOf(self, name):
        #subroutine scope
        if (self.routinTable.get(name) != None):
            return self.routinTable[name][1];
        #class scope
        elif (self.classTable.get(name) != None):
            return self.classTable[name][1];
        #not found
        else:
            return None


    def typeOf(self, name):
        #subroutine scope
        if (self.routinTable.get(name) != None):
            return self.routinTable[name][0];
        #class scope
        elif (self.classTable.get(name) != None):
            return self.classTable[name][0];


    def indexOf(self, name):
        #subroutine scope
        if (self.routinTable.get(name) != None):
            return self.routinTable[name][2];
        #class scope
        elif (self.classTable.get(name) != None):
            return self.classTable[name][2];


