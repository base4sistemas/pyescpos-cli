# -*- coding: utf-8 -*-
#
# escpostools/cli.py
#
# Copyright 2018 Base4 Sistemas Ltda ME
#
# PyESCPOS-CLI is based on Armin Roacher's "complex example" from the "click
# project", which can be found at https://github.com/pallets/click/.
#
# Copyright (c) 2014-2018 by Armin Ronacher. All rights reserved.
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

import os
import sys

import click


CONTEXT_SETTINGS = dict(auto_envvar_prefix='ESCPOS')


class Context(object):

    def __init__(self):
        self.verbose = False

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)


pass_context = click.make_pass_decorator(Context, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'commands'))


class PyESCPOSCLI(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py') and filename.startswith('cmd_'):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            mod = __import__('escpostools.commands.cmd_' + name, None, None, ['cli'])
        except ImportError:
            raise RuntimeError('Cannot import command name: {!r}'.format(name))
        return mod.cli


@click.command(cls=PyESCPOSCLI, context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode.')
@pass_context
def cli(ctx, verbose):
    """PyESCPOS Command Line Interface (development and testing utility).

    To be useful, you must assign at least one alias with an implementation and
    a connection method, thus you can easily run tests and arbitrary scripts
    against one or more implementations. See help for "assign" and other
    commands, for example:

    \b
    $ escpos assign --help

    """
    ctx.verbose = verbose
