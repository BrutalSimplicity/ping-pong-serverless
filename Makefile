LAMBDA_DIRS=pong ping
TEST_DIRS=pong ping shared/code
STAGE=dev
REGIONS=us-east-1 us-west-2

setup-env:
	for dir in $(TEST_DIRS); do \
		$(MAKE) -C $$dir setup-env; \
	done

deploy:
	for dir in $(LAMBDA_DIRS); do \
		for region in $(REGIONS); do \
			STAGE=$(STAGE) REGION=$$region $(MAKE) -C $$dir deploy; \
		done \
	done

test:
	for dir in $(TEST_DIRS); do \
		$(MAKE) -C $$dir test; \
	done

package:
	for dir in $(LAMBDA_DIRS); do \
		STAGE=$(STAGE) $(MAKE) -C $$dir package; \
	done

destroy:
	for dir in $(LAMBDA_DIRS); do \
		for region in $(REGIONS); do \
			STAGE=$(STAGE) REGION=$$region $(MAKE) -C $$dir destroy; \
		done \
	done
