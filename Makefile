
CXX = g++
PYSRCDIR = src/py
CXXSRCDIR = src/cpp
OBJDIR = build
VPATH = $(OBJDIR):$(PYSRCDIR):$(CXXSRCDIR)
CXXFLAGS = -std=c++20 -O2 -shared -fPIC -Wall -Wextra

.PHONY: clean 

MODE ?= release

ifeq ($(MODE), debug)
	CXXFLAGS += -DDEBUG -g
endif

all: $(OBJDIR)/libvector.so hack hack-ui
	mkdir -p $(OBJDIR)

$(OBJDIR)/libvector.so: vector.cpp vector.hpp
	echo building libvector.so
	mkdir -p $(OBJDIR)
	g++ $(CXXFLAGS) -o "$(OBJDIR)/libvector.so" $< 

$(OBJDIR)/hack: $(PYSRCDIR)/main.py 
	echo building python
	echo "#!/home/main/coding/py/venv/bin/python3" > $@
	cat $< >> $@
	chmod +x $@

$(OBJDIR)/hack-ui: src/ui/*
	echo building UI

run: all
	build/hack --task 0 -i 00 -o -

clean:
	echo cleaning build
	$(RM) -rf $(OBJDIR)

