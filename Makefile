# Using bash
SHELL := /bin/bash

# One worker at the time
MAKEFLAGS = --jobs=1

# https://stackoverflow.com/questions/2373081/assign-a-makefile-variable-value-to-a-bash-command-result
NOW = $(shell date +"%Y%m%d_%H%M%S")
FILENAME = $(shell basename -- ${target})
NAME = $(shell basename ${FILENAME} .j2)

.PHONY: build
build: ## build docker image
	docker build --rm -t yaml-generator .

.PHONY: yaml
yaml: ## generate yaml file
	docker run --rm -i -v ${PWD}:/data -w /data -e TZ="Asia/Taipei" .....

.PHONY: apply
apply: ## apply yaml into kubernetes
	kubectl apply -f ...

# Absolutely awesome: http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
