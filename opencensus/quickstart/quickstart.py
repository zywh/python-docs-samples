# Copyright 2018 Google LLC
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

# [START monitoring_opencensus_metrics_quickstart]

import time
import random

from opencensus.stats import aggregation
from opencensus.stats import measure
from opencensus.stats import stats
from opencensus.stats import view
#import opencensus.tags

from opencensus.stats.exporters import stackdriver_exporter

# [START setup_exporter]
# Set up the metric to be tracked

# Latency of two kinds of simulated operations, "normal" and "extra"
#latency_key = opencensus.tags.tag_key.TagKey('kind')

# Measure in milliseconds
latency_measure = measure.MeasureFloat('latency', 'Latency in ms', 'ms')

# Break into buckets of increasing size
latency_distribution = aggregation.DistributionAggregation(
    [0, 25, 50, 100, 200, 400, 800, 1600]
)

latency_view = view.View(
    'latency',
    'Processing time',
#    [latency_key],
    [],
    latency_measure,
    latency_distribution
)

# Initialization

statistics = stats.Stats()

view_manager = statistics.view_manager
recorder = statistics.stats_recorder
exporter = stackdriver_exporter.new_stats_exporter(
    stackdriver_exporter.Options(project_id='engelke-tracing')
)

view_manager.register_exporter(exporter)
view_manager.register_view(latency_view)
# [END setup_exporter]


def process(kind):
    sleep_time = random.random() ** 2  # More interesting than just linear
    if kind == 'extra':
        sleep_time += 0.5
    time.sleep(sleep_time)


def main(iteration_count):
    measure_map = recorder.new_measurement_map()
    #tag_map = opencensus.tags.TagMap()

    # Simulated processing normally takes up to 1000 ms, randomly distributed.
    # Ten percent of the time, simulated "extra" processing adds 500ms
    for i in range(iteration_count):
        # Randomly pick a kind of processing
        if random.random() <= 0.5:
            kind = 'extra'
        else:
            kind = 'normal'

        # Perform processing
        start_time = time.time()
        process(kind)
        duration = time.time() - start_time

        # Record the measurement
        measure_map.measure_float_put(latency_measure, duration)
        #tag_map.insert(latency_key, opencensus.tags.tag_value.TagValue(kind))
        print(duration)

    measure_map.record()
    time.sleep(60)
# [END monitoring_opencensus_metrics_quickstart]


if __name__ == '__main__':
    main(100)
