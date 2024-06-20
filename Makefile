docs/_build/doc-coverage.json:
	make coverage -C docs

documentation-coverage-badge.json: docs/_build/doc-coverage.json
	python3 ci/parse_documentation_coverage.py docs/_build/doc-coverage.json > cpp/web/documentation-coverage-badge.json

version-badge.json:
	python3 ci/parse_version.py .bumpversion.cfg > cpp/web/version-badge.json

doto-badge.json:
	python3 ci/parse_dotos.py $$(./ci/grep_dotos.sh) > cpp/web/doto-badge.json

badges: documentation-coverage-badge.json version-badge.json doto-badge.json

clean:
	make clean -C cpp

.PHONY: tests clean test serve debug native web tests install-test-dependencies documentation-coverage documentation-coverage-badge.json version-badge.json doto-badge.json
