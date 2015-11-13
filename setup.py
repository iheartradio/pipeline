from setuptools import find_packages, setup

setup(
    name='pipeline',
    version='0.2.0',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'python-decouple',
        'voluptuous',
    ],
    tests_require=[
        'tox',
    ],
)
