#!/usr/bin/env python3
#
# Copyright (C) 2021 The Android Open Source Project
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

__all__ = [
    "api_profiler_test",
    "annotate_test",
    "app_profiler_test",
    "app_test",
    "binary_cache_builder_test",
    "cpp_app_test",
    "debug_unwind_reporter_test",
    "etm_stack_test",
    "gecko_profile_generator_test",
    "inferno_test",
    "java_app_test",
    "kotlin_app_test",
    "pprof_proto_generator_test",
    "purgatorio_test",
    "report_etm_test",
    "report_html_test",
    "report_lib_test",
    "report_sample_test",
    "run_simpleperf_on_device_test",
    "sample_filter_test",
    "stackcollapse_test",
    "tools_test",
]

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# When running an atest we can't include do_test because it has dependency that
#  need to be installed with pip.
try:
    from .do_test import main
except ImportError:
    pass
