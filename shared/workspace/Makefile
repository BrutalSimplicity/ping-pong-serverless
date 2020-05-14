current_dir := $(shell pwd)
STAGE=dev
REGION=us-east-1

SLS=npx sls -s $(STAGE) -r $(REGION) -v

setup-env:
	PIPENV_VENV_IN_PROJECT=1 pipenv install --three -d

package:
	$(SLS) package

deploy:
	$(SLS) deploy
