from setuptools import find_packages, setup

setup(
    name='pipeline-scaling-ihr',
    version='0.1.0',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'Henson>=0.5.0',
        'pika',
        'python-dateutil',
        'python-decouple',
        'voluptuous',
    ],
    tests_require=[
        'tox',
    ],
)
