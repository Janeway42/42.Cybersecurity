all:
	@if ! docker ps -a --format '{{.Names}}' | grep -wq onion; then \
		echo "\033[0;32mStarting layering the onion!\033[0m" ; \
		docker build -t onion ./srcs; \
		docker run -d --name onion onion; \
		echo "\033[0;32mOnion ready to stink up the place!\033[0m" ; \
	else \
		echo "\033[0;32mOnion is already stinking the place up!\033[0m" ; \
	fi

clean:
	@if docker ps -a --format '{{.Names}}' | grep -wq onion; then \
		docker stop $$(docker ps -qa) 2>/dev/null; \
		docker rm $$(docker ps -qa) 2>/dev/null || true; \
		docker image prune -a --force 2>/dev/null; \
		echo "\033[0;32mAll super squicky clean! No trace of onions here!\033[0m"; \
	else \
		echo "\033[0;32mOnion has already been removed!\033[0m"; \
	fi

status:
	docker ps -a

re:
	@$(MAKE) clean
	@$(MAKE) all

.PHONY: all clean re