# Makefile to packageing with Travis-CI
.PHONY: default
default: clean install copy zip

.PHONY: install
install: build_path
	pip install -r requirements.txt -t build

.PHONY: build_path
build_path: build
build:
	mkdir build

.PHONY: build_dist
build_dist: dist
dist:
	mkdir dist

.PHONY: copy
copy:
	cp -R src/* build/

.PHONY: zip
zip: build_dist test
	cd build && zip -r ../dist/lambda.zip .

.PHONY: clean
clean:
	rm -rf build
	rm -rf dist

.PHONY: test
test:
	PYTHONPATH=src py.test -vv -r sxX tests 
