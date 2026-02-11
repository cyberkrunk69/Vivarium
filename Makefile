release:
	@bump2version patch
	@git push && git push --tags

.PHONY: bump-version
bump-version:
	python scripts/bump_version.py $(PART)

.PHONY: diagrams-export
diagrams-export:
	./scripts/export_diagrams.sh

.PHONY: diagrams-validate
diagrams-validate:
	./scripts/validate_diagrams.py
