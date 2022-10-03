#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

docker run \
    -it \
    --rm \
    --net=host \
    --volume=${SCRIPT_DIR}/results:/workspace/results:rw \
    --env ROUTES=/workspace/leaderboard/data/routes_training.xml \
    --env DEBUG_CHALLENGE=1 \
    --env ROUTES_SUBSET=0 \
    map_agent:latest /bin/bash
