LAMBDA_DIRS=pong ping
TEST_DIRS=pong ping shared/code
STAGE=dev
REGIONS=us-east-1 us-west-2

deploy:
	for dir in $(LAMBDA_DIRS); do \
		for region in REGIONS; do \
			REGION=$$region $(MAKE) -C $$dir deploy; \
		done
	done

test:
	for dir in $(TEST_DIRS); do \
		$(MAKE) -C $$dir test; \
	done

package:
	for dir in $(LAMBDA_DIRS); do \
		$(MAKE) -C $$dir package; \
	done

destroy:
	for dir in $(LAMBDA_DIRS); do \
		for region in REGIONS; do \
			REGION=$$region $(MAKE) -C $$dir destroy; \
		done
	done
