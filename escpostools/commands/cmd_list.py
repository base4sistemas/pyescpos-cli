# -*- coding: utf-8 -*-
#
# escpostools/commands/cmd_list.py
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

from escpos import helpers

from escpostools.cli import pass_context

@click.command('list', short_help='List available implementations.')
@click.option('--sort', type=click.Choice(['name', 'vendor']), default='name',
        help='Sort listing by specific field')
@pass_context
def cli(ctx, sort):
    """List available implementations."""
    for impl in helpers.find_implementations(sort_by='model.{}'.format(sort)):
        click.echo('{:.<25} {}'.format(impl.model.name, impl.fqname))
    click.echo()
