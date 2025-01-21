# const
.DEFAULT_GOAL := install

# PROJECT DEPENDENCIES ########################################################

.PHONY: install
install: lock ## Install project dependencies
	@mkdir -p .cache
	uv venv
	uv pip install -r pyproject.toml


.PHONY: lock
lock: pyproject.toml
	uv lock

