
VENV ?= venv
PYINSTALLER := $(VENV)/bin/pyinstaller
PIP := $(VENV)/bin/pip
CXX ?= g++
PYSRCDIR = src/py
CXXSRCDIR = src/cpp
OBJDIR = build
VPATH = $(OBJDIR):$(OBJDIR)/app:$(PYSRCDIR):$(CXXSRCDIR)
CXXFLAGS = -std=c++20 -O2 -shared -fPIC -Wall -Wextra -Werror

.PHONY: clean all remake run install

MODE ?= release

ifeq ($(MODE), debug)
	CXXFLAGS += -DDEBUG -g
endif


all: Makefile $(OBJDIR)/libvector.so $(OBJDIR)/app/hack $(OBJDIR)/app/hack-ui
	echo Make all
	mkdir -p $(OBJDIR)


venv: 
	python3 -m venv $(VENV)

install: venv
	$(PIP) install -r requirements.txt


$(OBJDIR)/libvector.so: vector.cpp vector.hpp
	echo building libvector.so
	mkdir -p $(OBJDIR)
	g++ $(CXXFLAGS) -o "$@" $<


$(OBJDIR)/app/hack: main.py process.py stopwords-ru.txt | install
	echo building python
	$(PYINSTALLER) --noconfirm --onefile --name hack --console 	\
		--distpath=build/app 					\
		--add-data="$(PYSRCDIR)/process.py:." 	 		\
		--add-data="src/py/stopwords-ru.txt:." 			\
		--hidden-import=pymorphy3 				\
		$(PYSRCDIR)/main.py
	\
	cp $(OBJDIR)/libvector.so $(OBJDIR)/app
	cp $(PYSRCDIR)/stopwords-ru.txt $(OBJDIR)/app


$(OBJDIR)/hack-ui: src/ui/*
	echo building UI


remake:
	make clean
	make all


run: all
	$(OBJDIR)/app/hack --task 0 -i 00 -o -


clean:
	echo cleaning build
	$(RM) -rf $(OBJDIR)
	$(RM) -rf $(VENV)

