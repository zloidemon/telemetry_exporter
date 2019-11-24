import os
import re
from setuptools import setup, find_packages


def read_version():
    regexp = re.compile(r"^__version__\W*=\W*'([\d.]+)'")
    init_py = os.path.join(
        os.path.dirname(__file__),
        'telemetry_exporter', '__init__.py')
    with open(init_py, encoding="utf-8") as fp:
        for line in fp:
            match = regexp.match(line)
            if match is not None:
                return match.group(1)
        else:
            raise RuntimeError('Cannot find version')


def read(f):
    return open(os.path.join(
        os.path.dirname(__file__), f), encoding="utf-8"
    ).read().strip()


install_requires = [
    'aiokafka',
    'aiofiles',
    'asyncpg',
    'msgpack',
    'arun',
]


setup(
    name='telemetry_exporter',
    scripts=['bin/tesextractd', 'bin/tesworkerd'],
    version=read_version(),
    packages=find_packages(),
    install_requires=install_requires,
    author='Veniamin Gvozdikov',
    author_email='g.veniamin@googlemail.com',
    description=('Telemetry Service'),
    long_description='\n\n'.join((
        read('README.rst'),
        read('CHANGES.txt'),
        read('AUTHORS.rst'),
    )),
    keywords='telemetry',
    platforms=['any'],
    url='https://github.com/zloidemon/telemetry_exporter/',
    license='BSD',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP'],
    include_package_data=True)
