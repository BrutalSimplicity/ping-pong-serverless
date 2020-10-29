current_dir := $(shell pwd)

setup-env:
	PIPENV_VENV_IN_PROJECT=1 pipenv install --three -d

test:
	pipenv run pytest tests -s -vvv $(current_dir)/tests/
