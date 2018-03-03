# -*- coding: utf-8 -*-
#
# escpostools/commands/cmd_version.py
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

import click

from escpos import __version__ as pyescpos_version

from escpostools.cli import pass_context
from escpostools import __version__


@click.command('version', short_help='Display version information and exit.')
@pass_context
def cli(ctx):
    """Display version information and exit."""
    click.echo('PyESCPOS-CLI version {}'.format(__version__))
    ctx.vlog('PyESCPOS version {}'.format(pyescpos_version))
