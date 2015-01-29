# Copyright 2014 Cloudera Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

import ibis.expr.base as api
import ibis.expr.base as ir

from ibis.expr.tests.mocks import MockConnection



class TestTimestamp(unittest.TestCase):

    def setUp(self):
        self.con = MockConnection()
        self.alltypes = self.con.table('alltypes')
        self.col = self.alltypes.i

    def test_field_select(self):
        assert isinstance(self.col, ir.TimestampArray)

    def test_string_cast_to_timestamp(self):
        casted = self.alltypes.g.cast('timestamp')
        assert isinstance(casted, ir.TimestampArray)

        string = api.literal('2000-01-01')
        casted = string.cast('timestamp')
        assert isinstance(casted, ir.TimestampScalar)

    def test_extract_fields(self):
        # type-size may be database specific
        cases = [
            ('year', ir.ExtractYear, ir.Int32Array),
            ('month', ir.ExtractMonth, ir.Int32Array),
            ('day', ir.ExtractDay, ir.Int32Array),
            ('hour', ir.ExtractHour, ir.Int32Array),
            ('minute', ir.ExtractMinute, ir.Int32Array),
            ('second', ir.ExtractSecond, ir.Int32Array)
        ]

        for attr, ex_op, ex_type in cases:
            result = getattr(self.col, attr)()
            assert isinstance(result, ex_type)
            assert isinstance(result.op(), ex_op)
