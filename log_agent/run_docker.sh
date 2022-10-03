#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

${SCRIPT_DIR}/../_utils/docker-gui \
    -it \
    --rm \
    --net=host \
    --volume=${SCRIPT_DIR}/results:/workspace/results:rw \
    --env HOST_RESULTS_PATH=${SCRIPT_DIR}/results \
    --env DEBUG_CHALLENGE=1 \
    --env ROUTES_SUBSET=0 \
    log_agent:latest /bin/bash
