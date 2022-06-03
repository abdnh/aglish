.PHONY: all zip pylint mypy check fix clean

all: zip

zip: aglish.ankiaddon

aglish.ankiaddon: src/*
	rm -f $@
	rm -rf src/__pycache__
	rm -rf src/meta.json
	( cd src/; zip -r ../$@ * )

# Install in a testing profile
install:
	rm -rf src/__pycache__
	rm -rf src/meta.json
	cp -r src/. ankiprofile/addons21/aglish

fix:
	python -m black src
	python -m isort src

check:
	python -m black --diff --color src
	python -m isort --diff --color src

mypy:
	python -m mypy src

pylint:
	python -m pylint src

clean:
	rm -f src/__pycache__
	rm -rf src/meta.json
	rm -f aglish.ankiaddon
