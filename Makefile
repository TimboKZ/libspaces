setup:
	pip install pipenv
	pipenv install --dev

test:
	pipenv run -- py.test tests -s -v

.PHONY: test
