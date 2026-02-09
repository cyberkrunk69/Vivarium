release:
\t@bump2version patch
\t@git push && git push --tags
.PHONY: bump-version
bump-version:
\tpython scripts/bump_version.py $(PART)