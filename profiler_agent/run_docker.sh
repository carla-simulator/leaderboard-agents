#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

docker run \
    -it \
    --rm \
    --privileged \
    --net=host \
    --volume=${SCRIPT_DIR}/results:/workspace/results:rw \
    --volume=${SCRIPT_DIR}/profiling:/workspace/profiling:rw \
    profiler_agent:latest /bin/bash
