all: filters

filters: filters.py
	python -m compileall filters.py
	python -m compileall basic_tests.py

test: basic_tests.py
	python basic_tests.py -v

clean:
	rm *.pyc
