from setuptools import find_packages, setup

setup(
    name='pipeline',
    version='0.1.0',
    packages=find_packages(exclude=['tests']),
    tests_require=[
        'tox',
    ],
)