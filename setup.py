#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = []

setup_requirements = [
    'pytest-runner',
    'celery>=5.0.5',
    'redis>=3.5.3'
]

test_requirements = ['pytest>=3', ]

setup(
    author="S-Mann",
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Celery workflows and scenarios",
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='celery_scenarios',
    name='celery_scenarios',
    packages=find_packages(include=['celery_scenarios', 'celery_scenarios.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/S-Mann/celery_scenarios',
    version='0.1.0',
    zip_safe=False,
)
