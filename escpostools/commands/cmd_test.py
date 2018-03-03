# -*- coding: utf-8 -*-
#
# escpostools/commands/cmd_test.py
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

from escpostools.aliases import resolve_alias
from escpostools.cli import pass_context

LONG_RULER = '....:....|' * 8

SHORT_RULER = '....:....|' * 4


@click.command('test', short_help='Runs tests against implementations.')
@click.argument('aliases', type=click.STRING)
@click.option('--all', is_flag=True, help='Run all predefined test sets')
@click.option('--align', is_flag=True, help='Run predefined alignment test set')
@click.option('--modes', is_flag=True, help='Run predefined modes test set')
@click.option('--rulers', is_flag=True, help='Run predefined rulers test set')
@pass_context
def cli(ctx, aliases, all, align, modes, rulers):
    """Runs predefined tests against one or more implementations, sending sets
    of commands to the printer(s) throught associated connection method(s).

    For this command to work you must assign at least one alias with an
    implementation and connection method. See help for "assign" command. For
    example, if you want to run "modes" and "align" tests against an
    implementation aliased as "tmt20" you type:

    \b
    $ escpos test tmt20 --align --modes

    Or you can run all predefined tests against three aliased implementations:

    \b
    $ escpos test rm22,tmt20,dr700 --all

    """
    impls = [resolve_alias(alias_id) for alias_id in aliases.split(',')]

    if all:
        align = True
        modes = True
        rulers = True

    for impl in impls:
        if align:
            _run_align(impl)

        if modes:
            _run_modes(impl)

        if rulers:
            _run_rulers(impl)


def _run_align(impl):
    impl.init()
    impl.text('[Aligment Tests]')
    impl.lf()

    impl.justify_right()
    impl.text('Right Aligned')

    impl.justify_center()
    impl.text('Centered Text')

    impl.justify_left()
    impl.text('Left Aligned')
    impl.lf(2)

    impl.text('This long text paragraph should be left aligned. The quick brown fox jumps over the lazy dog.')
    impl.lf()

    impl.justify_center()
    impl.text('This long text paragraph should be centered. The quick brown fox jumps over the lazy dog.')
    impl.lf()

    impl.justify_right()
    impl.text('This long text paragraph should be right aligned. The quick brown fox jumps over the lazy dog.')
    impl.lf()

    impl.justify_left()
    impl.lf(2)


def _run_modes(impl):
    impl.init()
    impl.text('[Modes]')
    impl.lf()

    impl.text('Just normal text.')
    impl.lf()

    impl.text('Entering condensed...')
    impl.set_condensed(True)
    impl.text('The quick brown fox jumps over the lazy dog.')
    impl.set_condensed(False)
    impl.text('Condensed mode OFF')
    impl.lf()

    impl.text('Entering expanded...')
    impl.set_expanded(True)
    impl.text('The quick brown fox jumps over the lazy dog.')
    impl.set_expanded(False)
    impl.text('Expanded mode OFF')
    impl.lf(2)


def _run_rulers(impl):
    impl.init()
    impl.text('[Rulers]')
    impl.lf()

    impl.text(LONG_RULER)
    impl.lf(2)

    impl.set_condensed(True)
    impl.text(LONG_RULER)
    impl.set_condensed(False)
    impl.lf(2)

    impl.set_expanded(True)
    impl.text(SHORT_RULER)
    impl.set_expanded(False)
    impl.lf(2)


