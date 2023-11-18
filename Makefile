
VENV ?= venv
PYINSTALLER := $(VENV)/bin/pyinstaller
PIP := $(VENV)/bin/pip
CXX ?= g++
PYSRCDIR := src/py
CXXSRCDIR := src/cpp
UISRCDIR := src/ui
OBJDIR := build
VPATH := $(OBJDIR):$(OBJDIR)/app:$(PYSRCDIR):$(CXXSRCDIR):$(UISRCDIR)
CXXFLAGS := -std=c++20 -O0 -shared -fPIC -Wall -Wextra -Werror

.PHONY: clean all remake run install

MODE ?= release

ifeq ($(MODE), debug)
	CXXFLAGS += -DDEBUG -g
endif


all: Makefile $(OBJDIR)/libvector.so $(OBJDIR)/app/hack $(OBJDIR)/app/hack-ui
	@echo MAKING ALL

venv: 
	@echo MAKING VIRTUAL ENVIRONMENT
	python3 -m venv $(VENV)

install: venv
	@echo INSTALLING DEPENDENCIES
	$(PIP) install -r requirements.txt

$(OBJDIR)/libvector.so: vector.cpp vector.hpp
	@echo BUILDING libvector.so
	mkdir -p $(OBJDIR)
	g++ $(CXXFLAGS) -o "$@" $<

$(OBJDIR)/app/hack: main.py process.py stopwords-ru.txt | install
	@echo BUILING CONSOLE APPLICATION
	mkdir -p $(OBJDIR)
	$(PYINSTALLER) --noconfirm --onefile --name hack --console 	\
		--distpath=build/app 					\
		--add-data="$(PYSRCDIR)/process.py:." 	 		\
		--add-data="src/py/stopwords-ru.txt:." 			\
		--hidden-import=pymorphy3 				\
		$(PYSRCDIR)/main.py
	cp $(OBJDIR)/libvector.so $(OBJDIR)/app
	cp $(PYSRCDIR)/stopwords-ru.txt $(OBJDIR)/app

$(OBJDIR)/app/hack-ui: $(UISRCDIR)/ui.py | install
	mkdir -p $(OBJDIR)
	@echo BUILDING UI
	$(PYINSTALLER) --noconfirm --onefile --name hack-ui	\
		--distpath=build/app			  	\
		--hidden-import=PyQt5				\
		$(UISRCDIR)/ui.py

remake:
	@echo REMAKING
	make clean
	make all

run: all
	@echo RUNNING
	$(OBJDIR)/app/hack --task 0 -i data/docs/utf8 -o data/output -t data/themes/utf8

clean:
	@echo CLEANING BUILD
	$(RM) -rf $(OBJDIR)
	$(RM) -rf $(VENV)

