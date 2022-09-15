install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:
	black config models resources schemas *.py

lint:
	pylint --load-plugins pylint_flask_sqlalchemy pylint_flask\
		--disable=R,C,E1101,W0107 config models resources schemas *.py

# test:
# 	python -m pytest -vv test_app.py

# all: install format lint test
all: install format lint
