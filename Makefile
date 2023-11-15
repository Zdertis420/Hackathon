
CXX = g++
PYSRCDIR = src/py
CXXSRCDIR = src/cpp
OBJDIR = build
VPATH = $(OBJDIR):$(PYSCRDIR):$(CXXSRCDIR)

.PHONY: clean CXXSRCDIR/libvector.so

all: $(OBJDIR)/libvector.so hack hack-ui

$(OBJDIR)/libvector.so: vector.cpp vector.hpp
	echo building libvector.so
	mkdir -p $(OBJDIR)
	g++ -shared -fPIC -O2 -o "$(OBJDIR)/libevector.so" $< 

hack: $(PYSRCDIR)/main.py $(PYSRCDIR)/processing.py
	echo building python

hack-ui: src/ui/*
	echo building UI

clean:
	echo cleaning build
	$(RM) -rf $(OBJDIR)

