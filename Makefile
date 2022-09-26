install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:
	black config models resources schemas tests *.py

lint:
	pylint --load-plugins pylint_flask_sqlalchemy pylint_flask\
		--disable=R,C,E1101,W0107 config models resources schemas tests *.py

test:
	pytest -v tests/

all_no_test: install format lint

all: install format lint test
