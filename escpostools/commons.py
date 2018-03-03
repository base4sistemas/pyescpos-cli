# -*- coding: utf-8 -*-
#
# escpostools/commons.py
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

import importlib

from escpos.impl.epson import GenericESCPOS


def import_type_from(fq_name):
    names = fq_name.split('.') # eg: "escpos.conn.serial.SerialConnection"
    module = importlib.import_module('.'.join(names[:-1]))
    # eg: for <fq_name> "escpos.conn.serial.SerialConnection", result
    # the <SerialConnection> type, not an instance
    return getattr(module, names[-1])


def validate_escpos_impl(fq_name):
    impl_type = import_type_from(fq_name)
    if not issubclass(impl_type, GenericESCPOS):
        raise ValueError('FQname {!r} isn\'t a '
                'escpos.impl.epson.GenericESCPOS subclass'.format(fq_name))
    return impl_type
