#!/usr/bin/env python3
#
# Copyright (C) 2026 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import pathlib
from test.test_utils import TestBase, TestHelper, run_unit_tests


class TestReportETM(TestBase):
    def test_report_etm_success(self):
        perf_data = TestHelper.testdata_path('etm/perf_etm.data')
        symfs_dir = os.path.dirname(perf_data)

        # Build binary cache.
        self.run_cmd(['binary_cache_builder.py', '-i', perf_data, '-lib', symfs_dir, '--every'])

        # Verify binary_cache was created.
        self.check_exist(dirname='binary_cache')
        self.check_exist(filename='binary_cache/build_id_list')

        # Run report_etm.py.
        output = self.run_cmd(['report_etm.py', '-i', perf_data], return_output=True)

        # Verify output contains disassembly.
        self.assertIn('CPU7 /data/local/tmp/etm_test_loop: 0x1074 -> 0x1080', output)
        self.assertIn('ldr\tw8, [sp, #0xc]', output)
        self.assertIn('Total decoded instructions: 944', output)

    def test_report_etm_missing_binary(self):
        perf_data = TestHelper.testdata_path('etm/perf_etm.data')

        # Create empty binary cache directory.
        pathlib.Path('binary_cache').mkdir(exist_ok=True)

        # Run without building binary cache. It should not crash, but print ADDR_NACC.
        output = self.run_cmd(['report_etm.py', '-i', perf_data], return_output=True)

        # Verify it printed ADDR_NACC instead of disassembling.
        self.assertIn("ADDR_NACC: path /data/local/tmp/etm_test_loop cannot be decoded!", output)
        self.assertNotIn("TypeError", output)
        self.assertIn("Total decoded instructions: 0", output)


if __name__ == '__main__':
    run_unit_tests('report_etm_test')
