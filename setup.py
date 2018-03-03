# -*- coding: utf-8 -*-
#
# Copyright 2018 Base4 Sistemas Ltda ME
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import io
import os
import re

from setuptools import setup


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


def read_version():
    content = read(os.path.join('escpostools', '__init__.py'))
    return re.search(r"__version__ = '([^']+)'", content).group(1)


def read_install_requires():
    content = read(os.path.join('requirements', 'base.txt'))
    return content.strip().split(os.linesep)


setup(
        name='PyESCPOS-CLI',
        version=read_version(),
        description='PyESCPOS Command Line Interface',
        long_description=read('README.rst'),
        include_package_data=True,
        install_requires=read_install_requires(),
        packages=[
                'escpostools',
                'escpostools.commands',
            ],
        classifiers = [
                'Development Status :: 4 - Beta',
                'Environment :: Other Environment',
                'Intended Audience :: Developers',
                'Intended Audience :: Information Technology',
                'License :: OSI Approved :: Apache Software License',
                'Natural Language :: English',
                'Operating System :: OS Independent',
                'Programming Language :: Python',
                'Programming Language :: Python :: 2.7',
                'Topic :: Office/Business :: Financial :: Point-Of-Sale',
                'Topic :: Printing',
                'Topic :: Software Development :: Libraries :: Python Modules',
                'Topic :: Software Development :: Testing',
                'Topic :: Utilities',
            ],
        entry_points="""
            [console_scripts]
            escpos=escpostools.cli:cli
        """,
)
