.PHONY: all zip pylint mypy check fix clean

all: zip

zip: aglish.ankiaddon

aglish.ankiaddon: src/*
	rm -f $@
	rm -rf src/__pycache__
	rm -f src/meta.json
	( cd src/; zip -r ../$@ * )

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
	rm -f src/meta.json
	rm -f aglish.ankiaddon
