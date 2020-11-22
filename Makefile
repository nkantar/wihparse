.DEFAULT_GOAL := help
.PHONY: help install update hide report export all shell


help: ## this help dialog
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


install: ## set up project locally (requires Python 3.6+ and Poetry)
	poetry install


update: ## update DB from API
	poetry run python wihparse.py update


hide: ## hide specific posts
	poetry run python wihparse.py hide $(ids)


report: ## generate report from DB
	poetry run python wihparse.py report


export: ## export report
	make report > report.txt


all: ## update and export
	make update && make export


shell: ## open Python REPL with application loaded
	poetry run python -i wihparse.py
