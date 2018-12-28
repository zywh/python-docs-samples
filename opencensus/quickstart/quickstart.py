 Copyright 2018 Google LLC
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

from opencensus.stats import aggregation
from opencensus.stats import measure
from opencensus.stats import stats
from opencensus.stats import view

from opencensus.trace.exporters import stackdriver_exporter

import opencensus.trace.tracer


# Create the measure to track
latency_measure = measure.MeasureFloat('latency', 'Latency in ms')

recorder = stats.Stats().stats_recorder

distribution = aggregation.DistributionAggregation(
    [0, 25, 50, 75, 100, 200, 400, 600, 800, 1000, 2000, 4000, 6000]
)

latency_view = view.View("demo/latency", "The distribution of the latencies",
    [key_method, key_status, key_error],
    latency_measure,
    distribution)

# [START monitoring_opencensus_metrics_quickstart]

# [START setup_exporter]

# [END setup_exporter]

# [END monitoring_opencensus_metrics_quickstart]
