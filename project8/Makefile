###############################################################################
#
# Makefile for Python project
#
# Students:
# Roi Greenberg, ID 30557123, roi.greenberg@mail.huji.ac.il
# Inbar Avni, ID 201131760, inbar.avni@mail.huji.ac.il
#
###############################################################################



SRCS=*.py
EXEC=VMtranslator

TAR=tar
TARFLAGS=cvf
TARNAME=project8.tar
TARSRCS=$(SRCS) $(EXEC) README Makefile

all:
	chmod a+x $(EXEC)
tar:
	$(TAR) $(TARFLAGS) $(TARNAME) $(TARSRCS)

clean:
	rm -f *~

