from setuptools import find_packages, setup

setup(
    name='pipeline',
    version='2.5.0',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'Henson>=0.5.0',
        'python-dateutil',
        'python-decouple',
        'voluptuous',
    ],
    tests_require=[
        'tox',
    ],
)
