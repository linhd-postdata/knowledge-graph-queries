#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import io
from os.path import dirname
from os.path import join

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with io.open(
            join(dirname(__file__), *names),
            encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()


setup(
    name='knowledge_graph_queries',
    version='0.0.1',
    license='Apache Software License 2.0',
    description="Software for embedding the SPARQL queries to POSTDATA knowledge graph and parse the response from Stardog.",
    author='LINHD POSTDATA Project',
    author_email='info@linhd.uned.es',
    url='https://github.com/linhd-postdata/knowlege-graph-queries',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    python_requires='>3.6',
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov', 'snapshottest'],
    install_requires=read('requirements.txt').splitlines()
)
