current_dir := $(shell pwd)
SLS=npx sls -s $(STAGE) -r $(REGION) -v

setup-env:
	PIPENV_VENV_IN_PROJECT=1 pipenv install --three -d
	npm install

package:
	$(SLS) package

test:
	pipenv run pytest tests -s -vvv $(current_dir)/tests/

deploy:
	$(SLS) deploy

destroy:
	$(SLS) destroy
