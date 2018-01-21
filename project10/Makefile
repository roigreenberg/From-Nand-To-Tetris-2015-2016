###############################################################################
#
# Makefile for Python project
#
#
###############################################################################



SRCS=*.py
EXEC=JackAnalyzer

TAR=tar
TARFLAGS=cvf
TARNAME=project10.tar
TARSRCS=$(SRCS) $(EXEC) README Makefile

all:
	chmod a+x $(EXEC)
tar:
	$(TAR) $(TARFLAGS) $(TARNAME) $(TARSRCS)

clean:
	rm -f *~

