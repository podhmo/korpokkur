pep8:
	(cd tmp && korpokkur create --config ../sample.json "package[pytest]")
	(cd tmp && korpokkur create --config ../sample2.json "nestedpackage[pytest]")
	find tmp -name "*.py" | xargs pep8 || echo "package"
