#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

${SCRIPT_DIR}/../_utils/docker-gui \
    -it \
    --rm \
    --net=host \
    --volume=${SCRIPT_DIR}/results:/workspace/results:rw \
    --volume=${SCRIPT_DIR}/team_code/carla_data_provider.py:/workspace/scenario_runner/srunner/scenariomanager/carla_data_provider.py:rw \
    --volume=${SCRIPT_DIR}/team_code/route_scenario.py:/workspace/leaderboard/leaderboard/scenarios/route_scenario.py:rw \
    --env HOST_RESULTS_PATH=${SCRIPT_DIR}/results \
    --env DEBUG_CHALLENGE=2 \
    --env ROUTES_SUBSET=0 \
    log_agent:latest /bin/bash
