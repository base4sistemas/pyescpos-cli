# -*- coding: utf-8 -*-
#
# escpostools/aliases.py
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

"""Handles the aliases file.

Aliases are stored in a JSON file located at ``~/.escpos/aliases.json`` whose
content looks like:

.. sourcecode:: json

    {
        "elgin": {
            "impl": "escpos.impl.elgin.ElginRM22",
            "conn": "escpos.conn.bt.BluetoothConnection",
            "settings": "00:01:02:03:04:05"
        }.
        "dr700": {
            "impl": "escpos.impl.daruma.DR700",
            "conn": "escpos.conn.serial.SerialConnection",
            "settings": "/dev/ttyS5:9200:8:1:N:RTSCTS"
        }
    }

"""

import codecs
import json
import os

from escpostools import commons


ESCPOS_DIR = os.path.join(os.path.expanduser('~'), '.escpos')
ALIASES_FILE = os.path.join(ESCPOS_DIR, 'aliases.json')


def get_alias(alias_id):
    data = load_aliases()
    return data[alias_id]


def load_aliases():
    data = None
    if os.path.isfile(ALIASES_FILE):
        with codecs.open(ALIASES_FILE, 'r') as fp:
            data = json.load(fp)
    return data or {}


def save_aliases(data):
    if not os.path.isdir(ESCPOS_DIR):
        os.makedirs(ESCPOS_DIR)
    with codecs.open(ALIASES_FILE, 'w') as fp:
        json.dump(data, fp, indent=4)


def update_alias(alias_id, impl, conn, settings):
    data = load_aliases()
    data.update({
            alias_id: {
                    'impl': impl,
                    'conn': conn,
                    'settings': settings,}})
    save_aliases(data)
