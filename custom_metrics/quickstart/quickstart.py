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

import argparse
import time
import random

from opencensus.stats import aggregation
from opencensus.stats import measure
from opencensus.stats import stats
from opencensus.stats import view
from opencensus.stats.exporters import stackdriver_exporter
from opencensus.trace.exporters.transports.background_thread import BackgroundThreadTransport

from opencensus.tags import tag_key
from opencensus.tags import tag_value
from opencensus.tags import tag_map

# [START setup_exporter]
def initialize(project_id):
    key_method = tag_key.TagKey('kind')

    latency_measure = measure.MeasureFloat(
        'latency/process_step',
        'Process Step Latency in milliseconds',
        'ms'
    )

    # Track count of latency measures falling in each range
    latency_distribution = aggregation.DistributionAggregation(
        [0, 25, 50, 100, 200, 400, 800, 1600]
    )

    latency_view = view.View(
        'latency/process_step',
        'Processing time',
        [key_method],
        latency_measure,
        latency_distribution
    )

    statistics = stats.Stats()
    view_manager = statistics.view_manager
    recorder = statistics.stats_recorder
    exporter = stackdriver_exporter.new_stats_exporter(
        stackdriver_exporter.Options(project_id=project_id)
    )

    view_manager.register_exporter(exporter)
    view_manager.register_view(latency_view)

    return recorder, latency_measure, key_method
# [END setup_exporter]


def process(kind):
    # Simulated process randomly takes up to one second for 'normal' kinds of 
    # processesing, half a second more for 'extra' kinds
    sleep_time = random.random()
    if kind == 'extra':
        sleep_time += 0.5
    time.sleep(sleep_time)


def main(project_id, iteration_count):
    recorder, measure, key_method = initialize(project_id)

    tag_kind = tag_value.TagValue('simulation')
    key_map = tag_map.TagMap()
    key_map.insert(key_method, tag_kind)
    
    measure_map = recorder.new_measurement_map()

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
        milliseconds = int(round(1000.0 * duration))

        # Record the measurement
        measure_map.measure_int_put(measure, milliseconds)

        # TODO - remove debugging print statement
        print(milliseconds)

    measure_map.record(key_map)
    time.sleep(60)
# [END monitoring_opencensus_metrics_quickstart]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('project_id', help='Your Google Cloud Project ID.')
    parser.add_argument('iterations', type=int, help='Number of iterations')

    args = parser.parse_args()

    main(args.project_id, args.iterations)
