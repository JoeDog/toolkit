PACKAGE=toolkit
VERSION=1.1.10
PYV=py3

ifeq ($(BUILD), devl)
  SUFFIX = 'd'
else ifeq ($(BUILD), test)
  SUFFIX = 't'
else ifeq ($(BUILD), prod)
  SUFFIX = '3'
endif

ifndef BUILD
  SUFFIX='3'
endif


all:
	python$(SUFFIX) ./setup.py sdist bdist_wheel

test:  test1 test2 test3 test4 

test1: 
	python$(SUFFIX) tests/crypt.py

test2:
	python$(SUFFIX) tests/config.py

test3:
	python$(SUFFIX) tests/util.py

test4:
	python$(SUFFIX) tests/logger.py

install: 
	pip$(SUFFIX) install -U dist/$(PACKAGE)-$(VERSION)-$(PYV)-none-any.whl

uninstall:
	pip$(SUFFIX) uninstall $(PACKAGE)

clean:
	rm -Rf build dist $(PACKAGE).egg-info
	find . -name "*.pyc" -delete
	find . -name "_version.py" -delete
	find . -name "__pycache__" -delete
