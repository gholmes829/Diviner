all:

install:
	pip3 install -r requirements.txt

clean:
	rm -rf __pycache__ **/__pycache__ *.pyc
