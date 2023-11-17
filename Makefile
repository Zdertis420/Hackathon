
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

all: Makefile $(OBJDIR)/libvector.so hack hack-ui
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

$(OBJDIR)/app/hack: $(PYSRCDIR)/main.py $(PYSRCDIR)/task1.py install
	echo building python
	$(PYINSTALLER) --noconfirm --onefile --console --distpath=build/app --add-data="$(PYSRCDIR)/task1.py:build" --add-data="$(PYSRCDIR)/stopwords-ru.txt:build" --hidden-import=pymorphy3 $(PYSRCDIR)/main.py
	cp $(OBJDIR)/libvector.so $(OBJDIR)/app
#
#	echo "#!/home/main/coding/py/venv/bin/python3" > $@
#	cat $< >> $@
#	cp $(PYSRCDIR)/task1.py $(OBJDIR)
#	cp $(PYSRCDIR)/stopwords-ru.txt $(OBJDIR)
#	chmod +x $@

$(OBJDIR)/hack-ui: src/ui/*
	echo building UI

remake:
	make clean
	make all

run: all
	build/hack --task 0 -i 00 -o -

clean:
	echo cleaning build
	$(RM) -rf $(OBJDIR)

