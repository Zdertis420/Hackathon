
CXX = g++
PYSRCDIR = src/py
CXXSRCDIR = src/cpp
OBJDIR = build
VPATH = $(OBJDIR):$(PYSCRDIR):$(CXXSRCDIR)

.PHONY: clean

libvector.so: vector.*
	echo building libvector.so
	g++ -fPIC -shared -o $(OBJDIR)/libevector.so $^ 

hack: main.py processing.py
	echo building python

hack-ui: src/ui/*
	echo building UI

clean:
	echo cleaning build
	$(RM) -r $(OBJDIR)

