SETPROC_VER:=1.1.10

build: deps
	@pip install --no-cache-dir --find-links=dist \
		setproctitle==${SETPROC_VER}
	@python setup.py bdist_wheel
	@cp requirements.txt dist

install: build
	@pip install --no-cache-dir dist/telemetry_exporter-*.whl

test:
	py.test -v -p no:warnings ./tests/

clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -f `find . -type f -name '@*' `
	rm -f `find . -type f -name '#*#' `
	rm -f `find . -type f -name '*.orig' `
	rm -f `find . -type f -name '*.rej' `
	rm -fr *.egg-info
	rm -f .coverage
	rm -rf .pytest_cache
	rm -rf build
	rm -rf cover
	rm -fr dist
	python setup.py clean

deps:
	@mkdir -p dist build
	@git clone https://github.com/dvarrazzo/py-setproctitle \
		-b version-${SETPROC_VER} build/py-setproctitle
	@cd build/py-setproctitle && python setup.py bdist_wheel
	@cp build/py-setproctitle/dist/*.whl dist/
	@pip install --no-cache-dir --find-links=dist -r requirements-dev.txt
