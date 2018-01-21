###############################################################################
#
# Makefile for Python project
#
#
###############################################################################



SRCS=*.py
EXEC=JackCompiler

TAR=tar
TARFLAGS=cvf
TARNAME=project11.tar
TARSRCS=$(SRCS) $(EXEC) README Makefile

all:
	chmod +X $(EXEC)
tar:
	$(TAR) $(TARFLAGS) $(TARNAME) $(TARSRCS)

clean:
	rm -f *~

