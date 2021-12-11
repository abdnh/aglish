.PHONY: all zip format checkformat typecheck lint check clean

all: zip

zip: aglish.ankiaddon

aglish.ankiaddon: src/*
	rm -f $@
	rm -f src/meta.json
	rm -rf src/__pycache__
	( cd src/; zip -r ../$@ * )

format:
	python -m black src

checkformat:
	python -m black --diff --color src

typecheck:
	python -m mypy src

lint:
	python -m pylint src

check: lint typecheck checkformat

clean:
	rm -f *.pyc
	rm -f src/*.pyc
	rm -f src/__pycache__
	rm -f aglish.ankiaddon
