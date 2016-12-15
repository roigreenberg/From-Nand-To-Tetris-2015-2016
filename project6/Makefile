###############################################################################
#
# Makefile for Java project
#
# Students:
# Roi Greenberg, ID 30557123, roi.greenberg@mail.huji.ac.il
# Inbar Avni, ID 201131760, inbar.avni@mail.huji.ac.il
#
###############################################################################

JAVAC=javac
JAVACFLAGS=-g

SRCS=*.java
EXEC=Assembler

TAR=tar
TARFLAGS=cvf
TARNAME=project6.tar
TARSRCS=$(SRCS) $(EXEC) README Makefile

all: compile

compile:
	$(JAVAC) $(JAVACFLAGS) $(SRCS)
	chmod +x $(EXEC)

tar:
	$(TAR) $(TARFLAGS) $(TARNAME) $(TARSRCS)

clean:
	rm -f *.class *~

