#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

${SCRIPT_DIR}/docker-gui \
    -it \
    --rm \
    --net=host \
    --volume=${SCRIPT_DIR}/results:/workspace/results:rw \
    --volume=${SCRIPT_DIR}/run_evaluation.sh:/workspace/leaderboard/scripts/run_evaluation.sh:rw \
    --env HOST_RESULTS_PATH=${SCRIPT_DIR}/results \
    --env ROUTES=/workspace/leaderboard/data/routes_training.xml \
    --env DEBUG_CHALLENGE=1 \
    --env ROUTES_SUBSET=0 \
    log_agent:latest /bin/bash
