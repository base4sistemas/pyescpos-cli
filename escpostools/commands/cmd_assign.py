# -*- coding: utf-8 -*-
#
# escpostools/commands/cmd_assign.py
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

import re

import click

from escpostools import aliases
from escpostools import commons
from escpostools.cli import pass_context


_CONN_BLUETOOTH = 'bluetooth'
_CONN_DUMMY = 'dummy'
_CONN_FILE = 'file'
_CONN_NETWORK = 'network'
_CONN_SERIAL = 'serial'

_CONNECTION_TYPES = (
        (_CONN_BLUETOOTH, 'escpos.conn.bt.BluetoothConnection'),
        (_CONN_DUMMY, 'escpos.conn.dummy.DummyConnection'),
        (_CONN_FILE, 'escpos.conn.file.FileConnection'),
        (_CONN_NETWORK, 'escpos.conn.network.NetworkConnection'),
        (_CONN_SERIAL, 'escpos.conn.serial.SerialConnection'),
    )

_IDENTIFIER_RE = re.compile(r"^[^\d\W]\w*\Z", re.UNICODE)


def _validate_impl_fqname(ctx, param, value):
    try:
        impl_type = commons.validate_escpos_impl(value)
    except ImportError:
        raise click.BadParameter('Unknown ESC/POS implementation "{}"'.format(value))
    except ValueError:
        raise click.BadParameter('Implementation "{}" isn\'t a '
                'escpos.impl.epson.GenericESCPOS subclass'.format(value))
    return value


def _validate_conn_method(ctx, param, value):
    try:
        fqname = dict(_CONNECTION_TYPES)[value]
        conn_type = commons.import_type_from(fqname)
    except KeyError:
        raise click.BadParameter('Unknown connection implementation "{}"'.format(value))
    except ImportError:
        # its actually a bug, since there is an ID mapped to something that
        # cannot be imported
        raise RuntimeError('Connection implementation FQname <{}> is unknown'.format(fqname))
    return fqname


def _validate_alias_name(ctx, param, value):
    if not _IDENTIFIER_RE.match(value):
        raise click.BadParameter('Alias ID must be a valid Python identifier')
    return value


@click.command('assign', short_help='Assign aliases to ESC/POS implementations.')
@click.option('--impl',
        metavar='CLASSNAME',
        type=click.STRING,
        callback=_validate_impl_fqname,
        help='ESC/POS implementation fully qualified class name')
@click.option('--alias',
        metavar='ID',
        type=click.STRING,
        callback=_validate_alias_name,
        help='The actual alias (must be a valid python identifier).')
@click.option('--conn',
        metavar='METHOD',
        type=click.Choice([c for c, n in _CONNECTION_TYPES]),
        callback=_validate_conn_method,
        help='Connection method.')
@click.option('--settings',
        metavar='SETTINGS',
        type=click.STRING,
        help='Connection settings.')
@pass_context
def cli(ctx, impl, alias, conn, settings):
    """Assign aliases to ESC/POS implementations and connection methods.

    For example, if you want to assign an alias "tmt20" to Epson TM-T20
    implementation and with a network TCP/IP connection through IP 10.0.0.110
    on port 9100, you can type:

    \b
    $ escpos assign \\
        --impl escpos.impl.epson.TMT20 \\
        --alias tmt20 \\
        --conn network \\
        --settings "10.0.0.110:9100"

    """
    aliases.update_alias(alias, impl, conn, settings)
