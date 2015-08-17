from setuptools import find_packages, setup

setup(
    name='pipeline',
    version='0.1.2',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'voluptuous',
    ],
    tests_require=[
        'tox',
    ],
)
