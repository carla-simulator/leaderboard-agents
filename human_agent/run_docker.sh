#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

${SCRIPT_DIR}/docker-gui \
    -it \
    --rm \
    --net=host \
    --volume=${SCRIPT_DIR}/../submodules/leaderboard:/workspace/leaderboard:rw \
    --volume=${SCRIPT_DIR}/../submodules/scenario_runner:/workspace/scenario_runner:rw \
    --volume=${SCRIPT_DIR}/team_code:/workspace/team_code:rw \
    --volume=${SCRIPT_DIR}/results:/workspace/results:rw \
    --env ROUTES=/workspace/leaderboard/data/new_routes_training.xml \
    --env DEBUG_CHALLENGE=2 \
    --env DEBUG_CHECKPOINT_ENDPOINT=/workspace/results/live_results.txt \
    --env ROUTES_SUBSET=0-1 \
    human_agent:latest /bin/bash
