MAKEFILE_DIRS = ping pong
STAGE=dev
REGION=us-east-1

deploy:
	for dir in $(MAKEFILE_DIRS); do \
		$(MAKE) -C $$dir deploy; \
	done
